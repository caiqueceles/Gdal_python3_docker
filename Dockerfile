FROM osgeo/gdal
# # FROM python:3

RUN apt-get update
RUN apt install -y python3-pip
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ADD src /app
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN pip install debugpy -t /tmp
RUN pip install jupyter
CMD "sh"