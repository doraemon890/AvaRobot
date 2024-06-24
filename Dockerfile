FROM python:3.10.11

WORKDIR /root/Ava

COPY . .

RUN pip3 install --upgrade pip setuptools

RUN pip install -U -r requirements.txt

CMD bash start
