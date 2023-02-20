# team-card

## Prerequisites
- GNU Make
- Docker (tbd)

#### Create and activate virtual environment

```
make create-virtualenv
source .venv/bin/activate
```

## The disinformation detection model API

### Running the API

Use the command `make setup-local-api` to run the API locally. The API is available at: http://127.0.0.1/ . Besides the default GET request, the API has one POST request `check_fake/`, which tests the given article and determines if it is disinformation:

http://127.0.0.1/check_fake/

This request requires a json input file. The example json:
```json
{"article_text": "The contents of the article"}
```

The expected result is a list with recommended products and their scores:
```json
{"result": false}
```


### Testing the API

The test file can be found in `tests/test_api.py`. You can run these tests using command: `make run-tests`. If everything is ok, you should see "2 passed" in the output.

### Input query variables

The input query variables have the following types:

- "article_text": str



