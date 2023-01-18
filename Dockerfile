FROM python:3.8

EXPOSE 3111

COPY techtrends /app

WORKDIR /app

RUN pip install -r requirements.txt && python init_db.py

CMD ["python", "app.py"]