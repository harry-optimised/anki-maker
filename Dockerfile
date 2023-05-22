# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

WORKDIR /app

# Install Dependencies
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt

# Launch the app
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
