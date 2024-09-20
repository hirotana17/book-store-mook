FROM python:3.12
COPY requirements.txt /userapp/requirements.txt
WORKDIR /userapp
RUN pip install -r requirements.txt
COPY . /userapp
ENTRYPOINT ["python"]
CMD ["app.py"]
