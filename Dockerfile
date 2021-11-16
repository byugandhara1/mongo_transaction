FROM python:3.9-slim

# upgrade pip to the latest version.
RUN pip install --upgrade pip

# Set the working directory to /code
WORKDIR /code/

COPY requirements.txt requirements.txt

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt


COPY app app/


ENV PYTHONPATH $PYTHONPATH:/code

EXPOSE 9001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001", "--reload"]

# uvicorn app.main:app --host 0.0.0.0 --port 9001 --reload
