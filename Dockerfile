# Dockerfile

# Temel imaj olarak Python kullanıyoruz
FROM python:3.9

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Gereksinimleri yüklemek için requirements.txt dosyasını kopyalıyoruz
COPY requirements.txt requirements.txt

# Bağımlılıkları yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyalıyoruz
COPY . .

EXPOSE 8000

# Django'nun çalışması için komutu belirliyoruz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

