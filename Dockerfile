FROM python:3
COPY . /home/lucas/Documents/app/
WORKDIR /home/lucas/Documents/app/
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]