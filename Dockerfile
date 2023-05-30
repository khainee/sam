FROM khainezayye/rcmltb

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

COPY . .

CMD ["bash","start.sh"]
