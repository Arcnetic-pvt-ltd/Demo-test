# Use the official Playwright image as a base image
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

#setting working directory inside the container
WORKDIR /app

#copying the requirements file to the working directory
COPY requirements.txt .

#installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

#copying the rest of the application code
COPY . .

#running the script
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]