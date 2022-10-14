FROM python:3.9

RUN pip install pandas geopandas shapely sqlalchemy flask werkzeug psycopg2 waitress geoalchemy2 --upgrade pip

RUN mkdir /app

RUN mkdir /csv

WORKDIR /app

COPY . /app

CMD ["python3","app.py"]
