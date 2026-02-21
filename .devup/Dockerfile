FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt* .
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
COPY . .
COPY .devup/shim.py /app/sitecustomize.py
EXPOSE 8000
ENV PYTHONPATH=/app:$PYTHONPATH
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]
