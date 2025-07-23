FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Add /app to Python path
ENV PYTHONPATH=/app

# Install dependencies
COPY messaging_app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY messaging_app/ messaging_app/
COPY chats/ chats/
COPY manage.py .

# Expose Django's default port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
