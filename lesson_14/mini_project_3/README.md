# Mini project 3

## create virtual environment
```sh
python3 -m venv venv
```

## activate virtual environment
```sh
source ./venv/bin/activate
```

## install dependencies
```sh
pip install -U pip setuptools wheel
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## run application
```sh
uvicorn app.main:create_app --factory --host=0.0.0.0 --port=8000 --reload
```

## run tests
```sh
pytest .
```
