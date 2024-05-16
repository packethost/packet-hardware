FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

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
    util-linux \
    wget

# Install mstflint
ARG MSTFLINT_RELEASE=4.14.0-1
ARG MSTFLINT_SHA512=965b25141d1b960bb575fc9fb089e912b0408af72919d23f295c6a8e8650c95c9459cb496171dca7f818252a180bd85bee8ed0f876159279013828478a0c2101
ARG MSTFLINT_BASEURL=https://github.com/Mellanox/mstflint/releases/download/

RUN curl -Lo mstflint.tar.gz "${MSTFLINT_BASEURL}/v${MSTFLINT_RELEASE}/mstflint-${MSTFLINT_RELEASE}.tar.gz" && \
    tar -zxvf mstflint.tar.gz && \
    cd mstflint-*/ && \
    apt install -y \
        g++ \
        libibmad-dev \
        libssl-dev \
        make \
        zlib1g-dev && \
    ./configure && \
    make -j"$(nproc)" && \
    make install

# Install smartmontools

ARG SMARTMONTOOLS_RELEASE=RELEASE_7_1
ARG SMARTMONTOOLS_TARNAME=smartmontools-7.1
ARG SMARTMONTOOLS_SHA512=440b2a957da10d240a8ef0008bd3358b83adb9eaca0f8d3e049b25d56a139c61dcd0bb4b27898faef6f189a27e159bdca3331e52e445c0eebf35e5d930f9e295
ARG SMARTMONTOOLS_BASEURL=https://github.com/smartmontools/smartmontools/releases/download/

RUN curl -sL "${SMARTMONTOOLS_BASEURL}/${SMARTMONTOOLS_RELEASE}/${SMARTMONTOOLS_TARNAME}.tar.gz" >smartmontools.tar.gz && \
      echo "${SMARTMONTOOLS_SHA512}  smartmontools.tar.gz" | sha512sum -c && \
      tar -zxvf smartmontools.tar.gz && \
      cd "$SMARTMONTOOLS_TARNAME" && \
      ./configure && \
      make -j"$(nproc)" && \
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

# Install racadm
RUN apt-get update && apt-get install -y alien && \
    rpm --import http://linux.dell.com/repo/pgp_pubkeys/0x1285491434D8786F.asc && \
    wget -U "Mozilla" \
      https://dl.dell.com/FOLDER05920767M/1/DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz \
      http://linux.dell.com/repo/community/openmanage/940/bionic/pool/main/s/srvadmin-omilcore/srvadmin-omilcore_9.4.0_amd64.deb && \
    tar -xvf DellEMC-iDRACTools-Web-LX-9.4.0-3732_A00.tar.gz && \
    alien -i iDRACTools/racadm/RHEL8/x86_64/*.rpm && \
    dpkg -i *.deb && \
    rm -r *.tar.gz iDRACTools *.deb

COPY ./ /opt/packet-hardware/
# Install packet-hardware
RUN apt update && \
    apt install -y git python3 python3-pip && \
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
    echo "Inserting dchipm.ini" && \
        cp /bin/src/dchipm.ini /opt/dell/srvadmin/etc/srvadmin-hapi/ini/ && \
    echo "Installing ironlib getbiosconfig" && \
        install -m 755 /bin/src/getbiosconfig /usr/bin/ && \
    rm -rf /bin/src

ENTRYPOINT ["packet-hardware"]
