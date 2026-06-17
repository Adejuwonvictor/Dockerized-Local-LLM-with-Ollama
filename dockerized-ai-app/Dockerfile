FROM python:3.11-slim
WORKDIR /app-container
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
RUN chown -R appuser:appgroup /app-container

USER appuser

EXPOSE 8000
CMD [ "sh", "entrypoint.sh" ]

