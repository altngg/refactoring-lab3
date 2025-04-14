# chessAPI

Python FastAPI small chess project

# Run without docker

Execute:

pip install -r requirements.txt

uvicorn app.main:app --reload

Acesse:

http://127.0.0.1:8000/docs

# Run with docker

docker-compose build

docker-compose up

http://127.0.0.1:8000/docs
