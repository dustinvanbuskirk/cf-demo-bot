FROM python:3.6.4-alpine3.7

ENV LANG C.UTF-8

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        git \
        nodejs && \
    npm install codefresh -g

COPY lib/cf-demo-bot.py /cf-demo-bot.py

ENTRYPOINT ["python", "/cf-demo-bot.py"]
CMD ["run"]