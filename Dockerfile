FROM python:3.9

# set up a working directory
WORKDIR /app

# install virtual environment
RUN pip install virtualenv

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code into the container
COPY . .

# Expose the port that your FastAPI app listens on
EXPOSE 8000

# Define the command to run your app
CMD ["uvicorn", "main.main:app", "--host", "0.0.0.0", "--port", "8000"]