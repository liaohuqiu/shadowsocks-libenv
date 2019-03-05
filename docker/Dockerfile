FROM shadowsocks/shadowsocks-libev:v3.2.4

MAINTAINER Leo <liaohuqiu@gmail.com>

USER root

RUN set -ex \
 && apk add --no-cache --virtual .build-deps tar \
 && apk del .build-deps

RUN apk update \
    && apk add ca-certificates wget \
    && update-ca-certificates \
    && apk add --no-cache --virtual TMP build-base git autoconf automake gettext pcre-dev libtool asciidoc xmlto udns-dev c-ares-dev libev-dev libsodium-dev mbedtls-dev linux-headers tar \
    && wget -cq -O /root/v2ray-plugin.tar.gz https://github.com/shadowsocks/v2ray-plugin/releases/download/v1.1.0/v2ray-plugin-linux-amd64-v1.1.0.tar.gz \
    && tar xvzf /root/v2ray-plugin.tar.gz -C /root \
    && mv /root/v2ray-plugin_linux_amd64 /usr/local/bin/v2ray-plugin \
    && rm -f /root/v2ray-plugin.tar.gz \
    && git clone https://github.com/shadowsocks/simple-obfs.git /tmp/simple-obfs \
    && cd /tmp/simple-obfs && git submodule update --init --recursive \
    && ./autogen.sh && ./configure && make && make install  \
    && apk del TMP \
    && rm -rf /tmp/simple-obfs
