FROM python:3.7-stretch
RUN apt-get update -y
RUN apt-get install python-pip python-dev build-essential
COPY . /portable-fridge-python
WORKDIR /portable-fridge-python
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["init.py"]
