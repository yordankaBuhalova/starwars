FROM python:3-alpine

# set container working dir
WORKDIR /code

# copy requirements.txt in code dir
COPY code/requirements.txt /code
COPY entrypoint.sh /

# install python packages
RUN pip install -r requirements.txt

ENTRYPOINT /entrypoint.sh
