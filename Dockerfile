# Use an official Python image compatible with arm64 architecture
FROM --platform=linux/arm64 python:3.12-slim

# Set environment variables
ENV POETRY_VERSION=1.8.1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="pytest-python-selenium-framework"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR pytest-python-selenium-framework

# Copy the poetry files to the container
COPY pyproject.toml poetry.lock* ./

# Install the dependencies using Poetry
RUN poetry install --no-root --only main  # Use --only main to skip dev dependencies

# Copy the rest of the application code
COPY . .

# Specify the command to run the tests
CMD ["poetry", "run", "pytest"]
