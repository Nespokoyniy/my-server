FROM python:3.14.0b3-alpine3.21

LABEL owner="r0maf"

WORKDIR /backend

COPY ./backend/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./backend .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host 0.0.0.0", "--port", "8000"]