#!bin/sh

echo "Waiting for Ollama to be ready"

#keep pinging until ollama responds

until curl -s http://ollama:11434 > /dev/null 2>&1; do
    echo "Ollama is not ready yet....Retrying in 3s"
    sleep 3
done

echo "Ollama is ready"

#pull the image if it isnt there

curl -s -X POST http://ollama:11434/api/pull \
    -H "Content-Type: application/json" \
    -d '{"name": "llama3.2:1b"}' > /dev/null 2>&1

echo "Model ready. Starting FastAPI..."

exec uvicorn main:app --host 0.0.0.0 --port 8000