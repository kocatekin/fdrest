FROM python:3.10.0-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
RUN pip freeze > installed_packages.txt
CMD ["python", "restapi.py"]
