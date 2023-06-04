FROM python:3.8

EXPOSE 80

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt


RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
COPY . /app

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
