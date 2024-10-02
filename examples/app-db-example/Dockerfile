FROM python:3.9-slim

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

RUN python -m pip install --no-cache-dir -r /src/requirements.txt

COPY ./app /src/app

EXPOSE 80

CMD ["fastapi", "run", "app/main.py", "--port", "80"]