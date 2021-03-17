FROM python:3

ADD app.py requirements.txt /app/
ADD rblchecker/__init__.py rblchecker/listing.py rblchecker/probe.py /app/rblchecker/
RUN pip3 install -r /app/requirements.txt
ENV PYTHONUNBUFFERED=1

ENTRYPOINT python3 /app/app.py