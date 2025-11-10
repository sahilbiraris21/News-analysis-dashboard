FROM python

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 8001

CMD ["/app/startup.sh"]