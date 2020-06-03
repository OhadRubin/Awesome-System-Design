FROM python:3.8-slim
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# COPY asd asd
COPY /scripts/wait-for-it.sh wait-for-it.sh
RUN chmod  a+rx wait-for-it.sh
CMD ["bash"]
