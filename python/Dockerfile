from python:2-onbuild


RUN mkdir /app

WORKDIR /app

COPY settings.py /app/settings.py
COPY run.py /app/run.py


CMD ["python", "run.py"]
