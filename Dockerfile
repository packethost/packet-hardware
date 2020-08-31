FROM ubuntu:16.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

ARG MSTFLINT_RELEASE=4.14.0-1
ARG MSTFLINT_SHA512=965b25141d1b960bb575fc9fb089e912b0408af72919d23f295c6a8e8650c95c9459cb496171dca7f818252a180bd85bee8ed0f876159279013828478a0c2101
ARG MSTFLINT_BASEURL=https://github.com/Mellanox/mstflint/releases/download/

# Install tools
RUN apt update && apt install -y \
    curl \
    dmidecode \
    ethtool \
    hdparm \
    ipmitool \
    lshw \
    pciutils \
    smartmontools \
    util-linux

# Install mstflint
RUN curl -kLo mstflint.tar.gz "${MSTFLINT_BASEURL}/v${MSTFLINT_RELEASE}/mstflint-${MSTFLINT_RELEASE}.tar.gz" && \
    tar -zxvf mstflint.tar.gz && \
    cd mstflint-*/ && \
    apt install -y \
        g++ \
        libibmad-dev \
        libssl-dev \
        make \
        zlib1g-dev && \
    ./configure && \
    make && \
    make install && \
    apt purge -y \
        g++ \
        libibmad-dev \
        libssl-dev \
        make \
        zlib1g-dev && \
    apt autoremove -qy && \
    apt clean -yq && \
    rm -rf /var/lib/apt/lists/*

RUN if [ $(uname -m) != 'aarch64' ]; then \
      apt-get update && \
      apt-get install gnupg -y && \
      echo 'deb http://linux.dell.com/repo/community/ubuntu trusty openmanage' \
      | tee /etc/apt/sources.list.d/linux.dell.com.sources.list && \
      gpg --keyserver pool.sks-keyservers.net --recv-key 1285491434D8786F && \
      gpg -a --export 1285491434D8786F | apt-key add - && \
      apt-get update && \
      apt-get -y install srvadmin-base srvadmin-storageservices srvadmin-idrac7 && \
      rm /etc/apt/sources.list.d/linux.dell.com.sources.list && \
      apt-get -qy autoremove && \
      apt-get -qy clean ; \
    fi

COPY ./ /opt/packet-hardware/
# Install packet-hardware
RUN apt update && \
    apt install -y git python3 python3-distutils && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 && \
    pip3 install --no-cache-dir /opt/packet-hardware && \
    apt clean -qy && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /opt/packet-hardware

# Install tools
COPY binsrc/ /bin/src
RUN echo "Installing mlxup..." && \
        install -m755 -D /bin/src/mlxup-$(uname -m) /usr/bin/mlxup && \
    echo "Installing MegaCli..." && \
        tar -xvC / -f /bin/src/megacli-noarch-bin.tar && \
        ln -nsf /opt/MegaRAID/MegaCli/MegaCli64 /usr/bin/ && \
    echo "Installing PercCli..." && \
        tar -zxvC / -f /bin/src/perccli-*.tar.gz && \
        ln -nsf /opt/MegaRAID/perccli/perccli /usr/bin/ && \
    echo "Installing IPMICfg..." && \
        install -m 755 /bin/src/ipmicfg /usr/bin/ipmicfg && \
    rm -rf /bin/src

ENTRYPOINT ["packet-hardware"]
