FROM ubuntu:18.04

LABEL maintainer="jwilson@hurricanelabs.com"

ENV CUCKOO_REPO=https://github.com/cuckoosandbox/cuckoo \
    TAG=2.0.7 \
    CUCKOO_DIR=/opt/cuckoo
ENV CUCKOO=$CUCKOO_DIR/.cuckoo \
    VIRTUAL_ENV=$CUCKOO_DIR/venv

# Update the image to the latest packages
RUN apt-get update && \
    apt-get install --no-install-recommends -yqq \
# Install Essentials
    build-essential git netcat tcpdump libcap2-bin supervisor virtualenv python-dev libpq-dev python-magic libffi-dev libssl-dev libjpeg-dev zlib1g-dev \
# Install M2Crypto dependecies
    swig \
# Install Guacd
    libguac-client-rdp0 guacd && \
# Cleanup
    rm -rf /var/lib/apt/lists/*

COPY files/conf/config.json /tmp/config.json

# Clone Repo and add AWS configs and VirtualEnv
RUN cd /opt && git clone -b $TAG --single-branch $CUCKOO_REPO && \
    sed -i '/import\ re/a import\ traceback' $CUCKOO_DIR/cuckoo/common/config.py && \
    sed -i '/configuration = {/r /tmp/config.json' $CUCKOO_DIR/cuckoo/common/config.py && \
    cd $CUCKOO_DIR && virtualenv venv && useradd -ms /bin/bash cuckoo && \
    echo '\n\
*         hard    nofile      500000\n\
*         soft    nofile      500000\n\
cuckoo      hard    nofile      500000\n\
cuckoo      soft    nofile      500000' >> /etc/security/limits.conf

WORKDIR $CUCKOO_DIR
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create Cuckoo User and set permissions
RUN chown -R cuckoo:cuckoo . && \
# Setup TCPDump
    groupadd pcap && usermod -a -G pcap cuckoo && \
    chgrp pcap /usr/sbin/tcpdump && setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump

USER cuckoo
# Install Boto3 Requirement
RUN pip install boto3 configparser psycopg2 m2crypto

# Copy Files
COPY files/conf/aws.conf $CUCKOO_DIR/cuckoo/private/cwd/conf/aws.conf
COPY files/machinery/aws.py $CUCKOO_DIR/cuckoo/machinery/aws.py

# Obtain matching monitoring binaries from the community repo
RUN python stuff/monitor.py && \
## Install cuckoo as DEV mode
    python setup.py sdist develop && \
## Build Config Files
    cuckoo -d

COPY files/entrypoint.sh files/update_conf.py /

ENTRYPOINT ["/entrypoint.sh"]
CMD ["--help"]