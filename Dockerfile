# ----------- Builder Stage -----------
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ----------- Final Stage -----------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Create a non-root user
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

# Copy only installed packages from builder stage
COPY --from=builder /install /usr/local
COPY app/ .

# Adjust permissions
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE ${PORT}
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
