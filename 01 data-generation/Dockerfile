FROM  python:3.13

RUN pip install pandas sqlalchemy psycopg2 pyarrow

# Set the working directory inside the container to /app
WORKDIR /app

COPY load-data.py load-data.py

ENTRYPOINT ["python", "load-data.py"]