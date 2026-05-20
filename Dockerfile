FROM python:3.9-slim

# Create a non-root user for Security Hardening (Phase 5 requirement)
RUN useradd -m -s /bin/bash erpuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership
RUN chown -R erpuser:erpuser /app
USER erpuser

EXPOSE 80

CMD ["python", "app.py"]