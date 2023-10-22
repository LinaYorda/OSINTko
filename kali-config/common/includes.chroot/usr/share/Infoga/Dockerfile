FROM python:alpine

ENV APP_HOME /usr/src/app

WORKDIR $APP_HOME
ADD . $APP_HOME

RUN python setup.py install
RUN chmod +x infoga.py

ENTRYPOINT ["python","infoga.py"]
