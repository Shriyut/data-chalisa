FROM --platform=linux/amd64 python:3.9-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY . /main
WORKDIR /main
ENTRYPOINT ["python3"]
CMD ["main.py"]