# Anki Card Maker

## Introduction

The Anki Card Maker is a web-based application that automates the process of creating Anki flashcards. Given the URL of an online article, it parses the article text and generates a specified number of flashcards, which are then presented to the user in the application's user interface. The system uses the OpenAI API to generate the flashcards, with GPT-3.5-turbo as the underlying model. 

## Running with a Virtual Environment

Follow these steps to set up and run the application using a Python virtual environment.

1. First, ensure you have Python 3.9 installed on your system.

2. Next, clone the repository and navigate to the directory:

    ```
    git clone https://github.com/<your-username>/anki-card-maker.git
    cd anki-card-maker
    ```

3. Create a Python virtual environment and activate it:

    ```
    python3.9 -m venv venv
    source venv/bin/activate
    ```

4. Install the necessary Python packages using pip:

    ```
    pip install -r requirements.txt
    ```

5. Run the application with uvicorn:

    ```
    uvicorn main:app --reload
    ```

6. You can now access the application at http://localhost:8000 in your web browser.

## Running with Docker

Follow these steps to set up and run the application using Docker.

1. Ensure you have Docker installed on your system.

2. Clone the repository and navigate to the directory:

    ```
    git clone https://github.com/<your-username>/anki-card-maker.git
    cd anki-card-maker
    ```

3. Build the Docker image:

    ```
    docker build -t anki-card-maker .
    ```

4. Run the Docker container:

    ```
    docker run -p 80:80 anki-card-maker
    ```

5. You can now access the application at http://localhost in your web browser.
