# ---- Stage 1: The Builder ----
# Use a full Python image to build our dependencies
FROM python:3.11 as builder

WORKDIR /usr/src/app

# Install dependencies into a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ---- Stage 2: The Final Image ----
# Use a slim image for a smaller footprint
FROM python:3.11-slim-buster

WORKDIR /usr/src/app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code
COPY app.py .

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app runs on
EXPOSE 5000

# The command to run the application
CMD ["python", "app.py"]