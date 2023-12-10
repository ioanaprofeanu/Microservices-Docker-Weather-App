FROM python:3.10

# set work directory
WORKDIR /app

# copy and install dependencies
COPY requirements.txt /app/
RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy api files
COPY . /app/

# expose port
EXPOSE 6000

# command for running the server
CMD ["python", "server.py"]

