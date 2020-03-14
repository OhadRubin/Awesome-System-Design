FROM python:3.8-slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#WORKDIR /advanced-system-design
COPY asd asd
COPY wait-for-it.sh wait-for-it.sh
#COPY asd_db.sqlite asd_db.sqlite
RUN chmod  a+rx wait-for-it.sh
CMD ["bash"]
#CMD ["python" ,"-m" ,"asd.server" ,"run-server" ,"-h", "127.0.0.1" ,"-p" ,"8000" ,"rabbitmq"]