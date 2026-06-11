# RAG Candidate Search (Proof-of-Concept)
An AI tool that provides users the ability to search through (synthetic) data with natural language. 
This project is a proof-of-concept designed for Pro-Act IT, a consultancy company with a huge database of 
consultants. However, querying over the database is very time-consuming and inefficient in many 
cases. Therefore, I developed this project, which provides workers the ability to quickly retrieve 
relevant data.

## Requirements
The only requirement is [Docker](https://www.docker.com/get-started/). Everything else (Python, 
Ollama, Typesense, PostgreSQL) runs inside Docker containers.

If you want to develop or run tests locally outside of Docker, you will also need 
[Python 3.13](https://www.python.org/downloads/) and [Poetry](https://python-poetry.org/docs/).

## Running the Application

Make sure Docker is running, then start all services:

```
docker compose up --build
```

The first boot could take a few minutes. Docker will build the images and Ollama will download the 
`llama3.2` model (~2 GB). Wait until all containers show as healthy before continuing.

Once everything is up, seed the database with sample data:

```
curl -X POST http://localhost:8000/seed
```

The dashboard is now available at [http://localhost:8501](http://localhost:8501).

The next you're starting up the application, simply run `docker compose up`

## Resetting Everything

To wipe all data and start fresh:

```
docker compose down -v
```

Then run `docker compose up --build` and re-seed as described above.

## Local Development

If you want to work on the code outside of Docker, set up a local virtual environment using 
[Poetry](https://python-poetry.org/docs/):

```
pip install poetry
```

Move to the project directory:

```
cd ~/path/to/semantic_search
```

Create the virtual environment:

```
poetry install
```

Activate it:

```
$(poetry env activate) # for macOS or Linux
poetry env activate # for Windows
```

Or use `poetry shell` as an alternative.