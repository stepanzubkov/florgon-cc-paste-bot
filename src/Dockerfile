# syntax=docker/dockerfile:1
FROM python:3.11.5-alpine

# Disable python buffering and bytecode *.pyc compiling. 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Project directory on the container.
WORKDIR /srv

# Copy file for requirements
COPY pyproject.toml /srv

# Install requirements.
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-ansi --no-interaction

# Copy whole project to the container.
COPY . /srv/

# Run project after building.
CMD ["poetry", "run", "python", "main.py"]
