FROM python:3.12.10-slim-bookworm

RUN mkdir /apps

WORKDIR /apps

RUN apt update

RUN apt install tree -y

COPY . .

RUN pip3 install -r requirements.txt --break-system-packages

RUN tree

CMD ["python3", "app.py"]
