FROM quay.io/nushell/nu:devel
LABEL Maintainer vsochat@stanford.edu
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install nushell
WORKDIR /code
COPY nu_plugin_hello /usr/local/bin/nu_plugin_hello
ENTRYPOINT ["/bin/bash"]
