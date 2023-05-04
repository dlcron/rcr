# Use the official Python 3.10 image as the base image
FROM python:3.10-slim as base

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy application code and the poetry files
WORKDIR /app
COPY poetry.lock pyproject.toml README.md /app/
COPY src /app/src/

# Copy the rest of the application files
COPY bin /opt/bin/

FROM base as app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

# Expose the port the app runs on
EXPOSE 80

# Start the application
CMD ["/opt/bin/start-app.sh"]


FROM base as dev

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

