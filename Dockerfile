# using an officialpython runtime as a parent image
FROM python:3.8-slim

# Setting the working directory

WORKDIR /App

# Copying the current directory contents into the container at /App

COPY . /App

# Install any needed dependencies or libraries needed in requirements.txt

RUN pip install --no-cache-dir -r requirements.txt 

# Run the script when the container launches

CMD ["python", "EquityIndexScraper.py"]


