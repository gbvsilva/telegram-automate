FROM python:3.7-buster

RUN mkdir /opt/telegram-automate
COPY . /opt/telegram-automate

WORKDIR /opt/telegram-automate

RUN apt update
RUN apt install nocache -y python3-pip git
RUN pip install -r requirements.txt

RUN git clone https://github.com/gbvsilva/Telethon.git
RUN cd Telethon && python setup.py install

CMD [ "/opt/telegram-automate/main.py" ]
ENTRYPOINT [ "python3" ]