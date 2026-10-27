# Step 1: Use an official lightweight Python base runtime image
FROM python:3.11-slim

# Step 2: Set the internal system working directory inside the container
WORKDIR /app

# Step 3: Copy only your package tracking document first to optimize layers
COPY requirements.txt .

# Step 4: Install your application's external Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your main source script and system configuration parameters into the container
COPY automation.py .

# Step 6: Inform Docker that the system inside will listen on network port 8000
EXPOSE 8000

# Step 7: Define the startup instruction to run your Uvicorn API server engine automatically
CMD ["uvicorn", "automation:app", "--host", "0.0.0.0", "--port", "8000"]
