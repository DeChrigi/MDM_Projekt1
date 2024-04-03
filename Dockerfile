FROM python:3.12.1

# Installieren von ODBC-Treibern
RUN apt-get update
RUN apt-get install -y curl gnupg
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copy Files
WORKDIR /usr/src/app
COPY . .
# Install
RUN pip install -r requirements.txt
# Docker Run Command
EXPOSE 80
ENV FLASK_APP=/usr/src/app/my_flask_app/Frontend.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]