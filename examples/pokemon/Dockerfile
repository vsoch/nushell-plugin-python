FROM quay.io/nushell/nu:devel
LABEL Maintainer vsochat@stanford.edu
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install pokemon nushell
WORKDIR /code
COPY nu_plugin_pokemon /usr/local/bin/nu_plugin_pokemon
ENTRYPOINT ["/bin/bash"]
