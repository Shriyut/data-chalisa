FROM python:3.10-slim
WORKDIR /app
COPY sample_script.py /app/
COPY requirements.txt /app/
COPY deidentify-request.json /app/
COPY reidentify-request.json /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "sample_script:app", "--host", "0.0.0.0", "--port", "8080"]