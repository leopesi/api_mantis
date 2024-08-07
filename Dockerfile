# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh and fix line endings (if needed)
RUN apt-get update && apt-get install -y netcat
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /app/entrypoint.sh  # Corrigido o caminho para /app
RUN chmod +x /app/entrypoint.sh          # Corrigido 

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]         # Corrigido
