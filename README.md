# Team CARD: infodesic

## Prerequisites
- GNU Make
- Docker
- docker-compose

#### Create and activate virtual environment

```
make create-virtualenv
source .venv/bin/activate
```

## Running the program

To deploy the software, in the server terminal run the command:
```
docker-compose up
```

This command will build a composition of docker containers, which make up the disinformation detection tool.

## API documentation

The disinformation detection tool consists of several APIs, which are being used by the infodesic dashboard.

### Desinformation detection API

The desinformation detection API uses a deep learning model to determine if the given article is disinformation. The API is available at: http://127.0.0.1:11111/check_fake/ .

This request requires a json input file. The example json:
```json
{"article_text": "The contents of the article"}
```

The expected result is a dictionary depicting if the article is disinformation and the model explanation information:
```json
{"result": true,
 "explanation": [["war",0.29], ["desinformation",0.16]]}
```

where the `result` field indicated whether the article is disinformation (true) or not (false). The `explanation` field returns a list of words, which influenced the model's solution the most.

### The disinformation cases matching API

The disinformation cases matching API uses a database of known disinformation cases (from https://euvsdisinfo.eu/) and matches the given message to the closest disinformation cases using distance measures and deep learning methods. The API is available at: http://127.0.0.1:22222/match_fake/ .

This request requires a json input file. The example json:
```json
{"message_text": "The contents of the message"}
```

The expected result is a list of the closes disinformation cases with their certainty scores and contents:
```json
[{"score": 0.9,
 "title": "The title of the disinformation case",
 "content": "The description of the disinformation case"}]
```

where the `score` field shows the certainty of the method that the given message is the disinformation case, `title` is the title of the disinformation case and `content` is the description of the disinformation case.


### Testing the API

The test file can be found in `tests/test_api.py`. You can run these tests using command: `make run-tests`. If everything is ok, you should see "2 passed" in the output.

### Input query variables

The input query variables have the following types:

- "article_text": str
- "message_text": str



