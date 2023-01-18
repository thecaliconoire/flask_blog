FROM python:3.8

EXPOSE 3111

COPY . /techtrends

WORKDIR /techtrends

RUN pip3 install -r requirements.txt && python init_db.py

CMD ["python", "app.py"]