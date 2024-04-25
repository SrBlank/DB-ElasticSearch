FROM docker.elastic.co/elasticsearch/elasticsearch:8.4.3

# Set environment variables for Elasticsearch configuration
ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV xpack.security.http.ssl.enabled=false

# Expose Elasticsearch port
EXPOSE 9200

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Copy the Python script and CSV data to the container
COPY moveCSVtoDB.py /usr/share/elasticsearch/
COPY lyrics.csv /usr/share/elasticsearch/

# Install Python Elasticsearch client
RUN pip3 install elasticsearch

# Switch to elasticsearch user before running Elasticsearch
USER elasticsearch

# Command to run Elasticsearch
CMD ["elasticsearch"]
