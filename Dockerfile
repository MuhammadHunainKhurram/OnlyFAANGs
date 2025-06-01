# ➊ Use the slim Python 3.11 image as the base OS
FROM python:3.11-slim

# ➋ Set working directory inside the container
WORKDIR /app

# ➌ Copy only requirements first (good for caching)
COPY requirements.txt .

# ➍ Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# ➎ Copy the rest of your source code
COPY . .

# ➏ Container must expose the port FastAPI listens on
ENV PORT=8080

EXPOSE 8080

# ➐ Command to start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
