FROM python:3.12-bookworm
WORKDIR /app

# Install ODBC driver
RUN apt-get update && apt-get install -y curl gnupg unixodbc-dev
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null
RUN curl -sSL https://packages.microsoft.com > /etc/apt/sources.list.d/mssql-release.list
# Accept the EULA and install the driver
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]