FROM python

RUN apt-get update \
  && apt-get install -y default-libmysqlclient-dev gcc \
  && rm -rf /var/lib/apt/lists/

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python","app.py" ]