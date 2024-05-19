# Voice to Text System

A simple voice to text system built with FastAPI, AssemblyAI, MongoDB and Beanie!

## Objective

Create a RESTful API for a simple voice to text system. The system should allow users to upload mp3 format audio file and return the audioʼs transcript as response. Use NoSQL database to store the data.
Public available packages or tools are free to use. You can choose any packages or tools that make sense to help you complete the task.

## Setup

In a fresh environment (I use conda, but any should work).

```bash
pip install -r requirements.txt
```

Create a `.env` file at the root of the project, and include your Assembly AI key and your MongoDB Atlas Connection String. The `.env` file should look like this:

```bash
MONGO_CONNECTION_STRING="mongodb+srv://<DB_USERNAME>:<DB_PASWORD>@<CLUSTER>....mongodb.net..."
ASSEMBLY_AI_API_KEY="<YOUR ASSEMBLY AI API KEY>"
```

To start the API server locally, use the following command (from the project root):

```bash
uvicorn src.main:app --reload
```

To test, head to `localhost:8000` in your browser, and you should see the following:

```
{"message": "hello world"}
```

## Using the API

After starting the server, we can use the endpoints as intended.
To transcribe a file, the easiest ways are to either use the interactive docs (available at `localhost:8000/docs`) or to use the example notebook provided.

### Using the example notebook

Open the example notebook (`example.ipynb`) and follow the instructions to interact with the API.

### Using the interactive docs

## Running the tests

From the root, simply run:

```bash
pytest
```

If using VSCode, test should be discoverable by the built in test runner (see below). Make sure to configure as per the instructions.

![testing screenshot](/examples/test-screenshot.png)

## Extensions and improvements

This was a quick and simple approach, but some possible extensions and improvements could include;

- Add caching to avoid repeating (potentially expensive) transcriptions
- Add authentication + authorization system to track, manage and restrict usage
- Add rate limiting to protect resources and avoid malicious usage
- Extended functionality for retrieving transcriptions (by keyword / audio source / user etc.)
