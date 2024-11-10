# Utiliser l'image de base Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY ./LocalShare /app
COPY ./requirements.txt /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

#RUN apt-get update && apt-get install -y libpq-dev gcc

# Créer un utilisateur non-root pour exécuter l'application
RUN groupadd -r django && useradd -r -g django django
USER django

# Exposer le port 8000 pour l'application
EXPOSE 8000

# Lancer Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "root.wsgi:application"]
