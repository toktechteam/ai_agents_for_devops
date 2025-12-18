FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app /app

RUN chown -R appuser:appuser /app
USER appuser

# Default command: run the batch job
CMD ["python", "batch_job.py"]
