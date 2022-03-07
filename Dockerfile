FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app

EXPOSE 80

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y automake make bash git curl sudo

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]