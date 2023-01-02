FROM python:3.9

RUN apt update && apt install -y \
    redis

COPY grease/requirements.txt /grease/

RUN pip install -r /grease/requirements.txt

COPY grease/ /grease/

CMD bash /grease/setup.sh && python -u /grease/app/main.py