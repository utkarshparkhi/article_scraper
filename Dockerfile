# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /usr/src/article_scraper

# copy the dependencies file to the working directory
COPY ./article_scraper/requirements.txt .
# install dependencies
RUN pip install -r requirements.txt


