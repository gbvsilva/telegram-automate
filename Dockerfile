FROM alpine

RUN mkdir /opt/telegram-automate
COPY . /opt/telegram-automate

WORKDIR /opt/telegram-automate

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN apk add --no-cache git
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools && pip3 install -r requirements.txt

RUN git clone https://github.com/gbvsilva/Telethon.git
RUN cd Telethon && python setup.py install

CMD [ "/opt/telegram-automate/main.py" ]
ENTRYPOINT [ "python3" ]