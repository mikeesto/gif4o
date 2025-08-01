FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
  pip install gunicorn && pip install -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["gunicorn", "-b", "0.0.0.0:3000", "--log-level=debug", "--timeout", "120", "app:app"]