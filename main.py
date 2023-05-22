from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bs4 import BeautifulSoup
import requests
import openai
import textwrap
import os
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory=".")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class FlashcardForm(BaseModel):
    url: str
    api_key: Optional[str] = None
    num_cards: int


def make_cards(api_key: str, article_text: str, num_cards: int) -> str:
    prompt = f"""Create Anki flash cards based on the provided text. For example, given the text "Scaling laws generally only predict a model’s pretraining test loss, which measures the model’s ability to correctly predict how an incomplete piece of text will be continued.1 While this measure is correlated with how useful a model will be on average across many practical tasks (Radford et al., 2019), it is largely not possible to predict when models will start to show specific skills or become capable of specific tasks (see Figure 2; Steinhardt, 2021; Ganguli et al., 2022a; Wei et al., 2022a)."

You would generate the following output, note the format of the answer:

question: State one disadvantage of scaling laws, with respect to their predictive power.
answer: They are not able to predict emergent capabilities.

question: What are the pros and cons of scaling laws?
answer: Pros are that they are easy to use and can be applied to many different models. Cons are that they are not able to predict emergent capabilities.

The first flash card is good because it guides the student to the answer without giving it away.
The second flash card is bad because it is too open-ended and the student will not know what to answer.

Requirements:
 - The flashcards should be appropriate for learning the content of the article. 
 - Each flashcard should capture just one concept.
 - Each answer should be short and to the point, ideally just a few words.
 - Do not provide any other text in your answer, just the list of flashcards.
 - Delimit each flashcard with a blank line.
 - For each flashcard, answer in the following format:
    - question: ...
    - answer: ...

Please now generate {num_cards} flashcards based on the following text: 

{article_text}
"""

    messages = [
        {"role": "system", "content": "You are an helpful assistant that generates flashcards."},
        {
            "role": "user",
            "content": prompt,
        },
    ]

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"model": "gpt-3.5-turbo", "messages": messages},
    )

    if response.status_code != 200:
        raise Exception(
            f"OpenAI API call failed with status code {response.status_code}, error: {response.text}"
        )

    return response.json()["choices"][0]["message"]["content"]


@app.post("/generate_flashcards", response_class=HTMLResponse)
async def generate_flashcards(request: Request):
    form_data = await request.form()
    url = form_data.get("url")
    api_key: str = form_data.get("api_key") or os.getenv("OPENAI_API_KEY", "")  # type: ignore
    num_cards = int(form_data.get("num_cards"))  # type: ignore

    # Extract text from article
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article_content = " ".join([p.text for p in soup.find_all("p")]).strip()
    article_content = os.linesep.join([s for s in article_content.splitlines() if s])

    # Split text into chunks if it's more than 1000 words
    words = article_content.split()
    chunks = [" ".join(words[i : i + 2000]) for i in range(0, len(words), 2000)]

    messages: list[str] = []
    for chunk in chunks:
        print("Generate flashcards for chunk...")
        messages.append(make_cards(api_key, chunk, num_cards))

    model_output = "\n\n".join(messages)

    # Go through model output, for all lines greater than 100 characters, split them into smaller lines.
    model_output = os.linesep.join(
        [
            os.linesep.join(textwrap.wrap(line, width=120)) if len(line) > 120 else line
            for line in model_output.splitlines()
        ]
    )

    return templates.TemplateResponse(
        "index.html", {"model_output": model_output, "request": request}
    )
