
FROM python:3.12.10-slim-bookworm

RUN mkdir /apps

RUN mkdir /kubeconf

ENV PYTHONUNBUFFERED=1

WORKDIR /apps

RUN apt update

RUN apt install tree -y

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --break-system-packages

RUN rm requirements.txt

COPY . .

RUN tree

ENTRYPOINT ["uvicorn", "app:APP", "--host", "0.0.0.0", "--port", "8000"]
