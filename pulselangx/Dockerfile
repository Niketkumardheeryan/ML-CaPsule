FROM python:3.8-slim

RUN apt-get update

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3","-m","streamlit","run","welcome_👋️.py"]
