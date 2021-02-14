FROM python:3

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY run_me.sh /app
COPY . /app

CMD [ "./run_me.sh" ]
