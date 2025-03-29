# Use Python slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /frontend

# Copy all frontend files
COPY . .

# Expose port 3000
EXPOSE 3000

# Start Python HTTP server
CMD ["python", "-m", "http.server", "3000"]
