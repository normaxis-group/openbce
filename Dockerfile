# Moteur openbce : API HTTP (openbce.api) dans un conteneur minimal.
# Les données météo conventionnelles (donnees/meteo_re2020.npz) ne sont pas dans le dépôt public : les monter en volume.
#   docker build -t openbce .
#   docker run --rm -p 8765:8765 -v /chemin/donnees:/app/donnees:ro openbce
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY openbce ./openbce
COPY banc ./banc
RUN pip install --no-cache-dir numpy
ENV OPENBCE_HOTE=0.0.0.0 OPENBCE_PORT=8765 PYTHONUNBUFFERED=1
EXPOSE 8765
CMD ["python", "-m", "openbce.api"]
