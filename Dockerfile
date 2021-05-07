FROM python:3.6.4-alpine3.7

ENV LANG C.UTF-8

# Install GIT/NODEJS
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        git \
        nodejs \
        build-base \
        python3-dev \
        libffi-dev \
        openssl-dev

# Install Codefresh CLI
RUN npm install codefresh

# Install Python GitHub module
RUN pip install PyGithub

COPY lib/cf-demo-bot.py /cf-demo-bot.py

ENTRYPOINT ["python", "/cf-demo-bot.py"]
CMD [""]
