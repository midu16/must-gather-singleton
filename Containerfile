# Use a base image
FROM registry.access.redhat.com/ubi8-minimal

ARG TITLE="must-gather-singleton"
ARG DESCRIPTION="Collecting entire cluster stack data in a compact aggregated must-gather file"
ARG AUTHORS="midu@redhat.com"
ARG LICENSE="Apache-2.0"
ARG URL="https://github.com/midu16/must-gather-singleton"
ARG SOURCE="https://github.com/midu16/must-gather-singleton/Containerfile"

COPY scripts/* /opt/

#RUN microdnf update -y; microdnf upgrade -y; 
RUN microdnf -y install python3 tar gzip; microdnf clean all; pip3 install -r /opt/requirements.txt ; mkdir -p /apps/must-gather ; curl -L https://mirror.openshift.com/pub/openshift-v4/clients/ocp/4.14.10/openshift-client-linux-4.14.10.tar.gz | tar -xz -C /bin/

# Set environment variable
ENV KUBECONFIG=/apps/kubeconfig

# Create a directory in the container

# Mount volume from operating system to /apps/must-gather directory inside the container
VOLUME /apps/must-gather

# Specify the command to run when the container starts
CMD  ["/usr/bin/python3", "/opt/must-gather-singleton.py"]
