FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mypy .

# jwt_secret token not being availbale crashes tests
# need to get env vars initialised before this
# RUN pytest app/tests

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload", "--reload-dir", "app"]