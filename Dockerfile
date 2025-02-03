# Base image
FROM ubuntu:20.04



# Set working directory
WORKDIR /app

# Copy all project files to the container
COPY . /app
COPY . /scripts
COPY ./scripts /app/scripts


# Set up a new sources.list with trusted sources
RUN echo "deb https://archive.ubuntu.com/ubuntu/ focal main universe restricted multiverse" > /etc/apt/sources.list && \
    echo "deb https://archive.ubuntu.com/ubuntu/ focal-updates main universe restricted multiverse" >> /etc/apt/sources.list && \
    echo "deb https://archive.ubuntu.com/ubuntu/ focal-backports main universe restricted multiverse" >> /etc/apt/sources.list && \
    echo "deb https://security.ubuntu.com/ubuntu focal-security main universe restricted multiverse" >> /etc/apt/sources.list

# Set untrusted certificate flag temporarily (use cautiously in production)
RUN echo 'Acquire::https::Verify-Peer "false";' > /etc/apt/apt.conf.d/99untrusted

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive


# Set DNS server
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf

# Update and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-nmap \
    nmap \
    nano \
    net-tools \
    git \
    iputils-ping \
    wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Go 1.21.1
RUN wget https://go.dev/dl/go1.21.1.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz && \
    rm go1.21.1.linux-amd64.tar.gz && \
    ln -s /usr/local/go/bin/go /usr/bin/go && \
    ln -s /usr/local/go/bin/gofmt /usr/bin/gofmt

# Remove the untrusted certificate flag after installation
RUN rm -f /etc/apt/apt.conf.d/99untrusted

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

#Install shodan
RUN pip3 install shodan

#RUN rm -f /app/hive/python/in/shodan.py 
#RUN rm -f /scripts/hive/python/in/shodan.py

# Install Nuclei (run in a clean temporary directory)
RUN mkdir -p /tmp/nuclei-install && \
    cd /tmp/nuclei-install && \
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && \
    ln -s /root/go/bin/nuclei /usr/local/bin/nuclei && \
    rm -rf /tmp/nuclei-install && \
    nuclei -version


# Nuclie
# Install Nuclei
RUN go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    

# Verify Nuclei Installation
RUN nuclei -version

# Starting Nuclei Installation
RUN nuclei 

# Default command
CMD ["python3", "app.py"]
