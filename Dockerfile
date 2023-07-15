# ./Dockerfile
FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && apt-get -y install vim && apt-get clean
RUN mkdir /girlfriend_gpt
ADD . /girlfriend_gpt

WORKDIR /girlfriend_gpt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]