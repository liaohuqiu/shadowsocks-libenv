FROM shadowsocks/shadowsocks-libev:v3.2.4

MAINTAINER Leo <liaohuqiu@gmail.com>

USER root

RUN set -ex \
 && apk add --no-cache --virtual .build-deps tar \
 && wget -cq -O /root/v2ray-plugin.tar.gz https://github.com/shadowsocks/v2ray-plugin/releases/download/v1.1.0/v2ray-plugin-linux-amd64-v1.1.0.tar.gz \
 && tar xvzf /root/v2ray-plugin.tar.gz -C /root \
 && mv /root/v2ray-plugin_linux_amd64 /usr/local/bin/v2ray-plugin \
 && rm -f /root/v2ray-plugin.tar.gz \
 && apk del .build-deps

ENV SIMPLE_OBFS_VER 0.0.5
ENV SIMPLE_OBFS_URL https://github.com/shadowsocks/simple-obfs/archive/v$SIMPLE_OBFS_VER.tar.gz
ENV SIMPLE_OBFS_DIR simple-obfs-$SIMPLE_OBFS_VER

RUN set -ex \
    && apk add --no-cache libcrypto1.0 \
                          libev \
                          libsodium \
                          mbedtls \
                          pcre \
                          udns \
    && apk add --no-cache \
               --virtual TMP autoconf \
                             automake \
                             build-base \
                             curl \
                             gettext-dev \
                             libev-dev \
                             libsodium-dev \
                             libtool \
                             linux-headers \
                             mbedtls-dev \
                             openssl-dev \
                             pcre-dev \
                             tar \
                             udns-dev \
    && curl -sSL $SIMPLE_OBFS_URL | tar xz \
    && cd $SIMPLE_OBFS_DIR \
        && ./autogen.sh \
        && ./configure --disable-documentation \
        && make install \
    && apk del TMP
