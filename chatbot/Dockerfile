FROM langchain/langchain

WORKDIR /usr/src/app

# Install system dependencies in a single RUN instruction to minimize layers
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy all the necessary files in one layer to optimize build
COPY requirements.txt app.py tools.py chainlit.md .env startup.sh startup.py bf_questions.json ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt

# Expose port 8000 for the application
EXPOSE 8000

RUN chmod +x startup.sh
CMD ["./startup.sh"]