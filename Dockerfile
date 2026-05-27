# AutoShield QA Platform — Docker
# Base image: official Playwright Python image (browsers pre-installed)
FROM mcr.microsoft.com/playwright/python:v1.59.0-jammy

# Set working directory
WORKDIR /app

# Install Python dependencies first (cached layer — only rebuilds if requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Create reports directory for output
RUN mkdir -p reports/screenshots reports/logs

# Default command — runs UI + API tests on Chromium, headless
# Override at runtime: docker run autoshield pytest api_tests/ -v
CMD ["pytest", "tests/", "api_tests/", \
     "--browser", "chromium", \
     "--html=reports/report_docker.html", \
     "--self-contained-html", \
     "-v"]