FROM python:3.6-alpine
EXPOSE 8080
RUN apk add ca-certificates
RUN pip install pipenv
COPY . /app
WORKDIR /app
RUN pipenv install --system --deploy
CMD ["waitress-serve", "app:app"]
