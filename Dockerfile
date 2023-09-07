FROM --platform=linux/amd64 python:3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app

ENTRYPOINT [ "python", "/app/funcs/func.py" ]
