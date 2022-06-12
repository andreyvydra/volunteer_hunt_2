FROM python
ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .


CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]