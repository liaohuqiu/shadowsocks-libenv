#!/usr/bin/env python
import os
import sys
import socket
from ruamel import yaml

from cpbox.tool import dockerutil
from cpbox.tool import functocli
from cpbox.tool import file
from cpbox.tool import template
from cpbox.tool import utils

from cpbox.app.devops import DevOpsApp

APP_NAME = 'ss'
bypass_ipset_name = 'ss_spec_wan_bypass'
forward_ipset_name = 'ss_spec_wan_fw'

ss_image = 'docker-genesis.yizhoucp.cn/boris1993/shadowsocks-v2ray-docker:v3.2.4-1.1.0'
# ss_image = 'docker-genesis.yizhoucp.cn/easypi/shadowsocks-libev'
ss_container = 'ss'

obfs_image = 'docker-genesis.yizhoucp.cn/liaohuqiu/simple-obfs'
obfs_container = 'obfs'

chinadns_image = 'docker-genesis.yizhoucp.cn/liaohuqiu/chinadns'
chinadns_container = 'chinadns'

ss_image='boris1993/shadowsocks-v2ray-docker:v3.2.4-1.1.0'
ss_port=8080
ss_container='ss'
ss_v2ray_container='ss-v2ray'

class App(DevOpsApp):

    def __init__(self, **kwargs):
        DevOpsApp.__init__(self, 'ss')
        file.ensure_dir(self.app_config_dir)
        file.ensure_dir(self.app_templates_dir)

        self.ss_image = 'liaohuqiu/ss'
        self.ss_v2ray_container = 'ss-v2ray'
        self.simple_obfs_container = 'ss-obfs'

    def stop(self):
        self.stop_container(self.ss_v2ray_container)
        self.stop_container(self.simple_obfs_container)

    def run_ss(self):
        # _run_ss_container "ss-server -p 8388 -m aes-128-cfb -k $password -u --acl=/etc/local.acl"
        # _run_ss_container "ss-server -p 8388 -m aes-128-cfb -k $password -u"
        cmd = "ss-server -s 0.0.0.0 -p 8388 -m aes-128-cfb -k $password -u --plugin v2ray-plugin --plugin-opts server"
        self._run_ss_container(cmd)

    def build_image(self):
        cmd = 'docker build -t %s %s/docker' % (self.ss_image, self.root_dir)
        self.shell_run(cmd)

    def run_obfs(self):
        pass

    def _run_container(self, image_name, container_name, cmd, run_mod='d'):
        envs = []
        ports = []
        volumes = {
                self.app_config_dir + '/local.acl': '/etc/local.acl'
                }
        args = dockerutil.base_docker_args(container_name=container_name, envs=envs, ports=ports, volumes=volumes)
        cmd_data = {}
        cmd_data['image'] = image_name
        cmd_data['args'] = args
        cmd_data['cmd'] = cmd
        cmd_data['run_mod'] = run_mod
        cmd = template.render_str('docker run {{ run_mod }} -u root --restart always {{ args }} {{ image }} sh -c "{{ cmd }}"', cmd_data)
        self.shell_run(cmd)

if __name__ == '__main__':
    functocli.run_app(App)
