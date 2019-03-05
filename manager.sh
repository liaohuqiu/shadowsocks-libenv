#!/bin/bash

set -e

prj_path=$(cd $(dirname $0); pwd -P)

ss_image='boris1993/shadowsocks-v2ray-docker:v3.2.4-1.1.0'
ss_port=8080
ss_container='ss'
ss_v2ray_container='ss-v2ray'

simple_obfs_image=liaohuqiu/simple-obfs
simple_obfs_port=8443
simple_obfs_container=simple-obfs
password='123466'

function stop() {
    stop_container $ss_container
    stop_container $simple_obfs_container
}

function run() {
    run_ss
    # run_simple_obsf
}

function run_ss() {
    # disable acl
    # _run_ss_container "ss-server -p 8388 -m aes-128-cfb -k $password -u --acl=/etc/local.acl"
    # _run_ss_container "ss-server -p 8388 -m aes-128-cfb -k $password -u"
    _run_ss_container "ss-server -s 0.0.0.0 -p 8388 -m aes-128-cfb -k $password -u --plugin v2ray-plugin --plugin-opts server"
}

function run_simple_obsf() {
    local docker0_ip=$(docker0_ip)
    _run_simple_obsf_container "obfs-server -p $simple_obfs_port --obfs tls -r $docker0_ip:$ss_port"
}

function _run_ss_container() {
    local cmd=$1
    local args="--restart=always"
    args="$args -p $ss_port:8388/tcp"
    args="$args -p $ss_port:8388/udp"
    args="$args -v $prj_path/config/local.acl:/etc/local.acl"
    run_cmd "docker run -it $args --name $ss_container $ss_image $cmd"
}

function _run_simple_obsf_container() {
    local cmd=$1
    local args="--restart=always"
    args="$args -p $simple_obfs_port:$simple_obfs_port"
    run_cmd "docker run -d $args --name $simple_obfs_container $simple_obfs_image $cmd"
}

function restart() {
    stop
    run
}

function run_cmd() {
    local t=`date`
    echo "$t: $1"
    eval $1
}

function stop_container() {
    local container_name=$1
    local cmd="docker ps -a -f name='^/$container_name$' | grep '$container_name' | awk '{print \$1}' | xargs -I {} docker rm -f --volumes {}"
    run_cmd "$cmd"
}

function docker0_ip() {
    local host_ip=$(ip addr show docker0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | awk '{print $1}' | head  -1)
    echo $host_ip
}

function help() {
	cat <<-EOF
    
	    Valid options are:

            run
            stop
            restart

            -h                      show this help message and exit

EOF
}

action=${1:-help}
$action "$@"
