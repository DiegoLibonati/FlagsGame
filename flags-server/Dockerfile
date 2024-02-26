FROM python:3.9

WORKDIR /home/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/app.py"]
