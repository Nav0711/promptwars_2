FROM python:3.11-slim

WORKDIR /app

# System deps for PyMuPDF and other native libs
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Cloud Run uses PORT env var; default to 8000
ENV PORT=8000

# On Cloud Run: ADC (Application Default Credentials) is used automatically.
# No SA key file needed in production.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
