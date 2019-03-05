#!/usr/bin/env python
import os
import sys
import socket
from ruamel import yaml

from cpbox.tool import dockerutil
from cpbox.tool import functocli
from cpbox.tool import template

from cpbox.app.devops import DevOpsApp

class App(DevOpsApp):

    def __init__(self, **kwargs):
        DevOpsApp.__init__(self, 'ss')

        self.ss_image = 'liaohuqiu/ss'
        self.ss_v2ray_container = 'ss-v2ray'
        self.ss_obfs_container = 'ss-obfs'

    def stop_ss_v2ray(self):
        self.remove_container(self.ss_v2ray_container, force=True)

    def start_ss_v2ray(self):
        cmd = "ss-server -s 0.0.0.0 -p 8388 -m aes-128-cfb -k 123466 -u --plugin v2ray-plugin --plugin-opts server --acl=/etc/local.acl"
        ports = ['9443:8388/tcp', '9443:8388/udp']
        self._run_container(self.ss_v2ray_container, cmd, '-it', ports=ports)

    def stop_ss_obfs(self):
        self.remove_container(self.ss_obfs_container, force=True)

    def start_ss_obfs(self):
        cmd = "ss-server -s 0.0.0.0 -p 8388 -m aes-128-cfb -k 123466 -u --plugin obfs-server --plugin-opts 'obfs=tls' --acl=/etc/local.acl"
        ports = ['8443:8388/tcp', '8443:8388/udp']
        self._run_container(self.ss_obfs_container, cmd, '-d', ports=ports)

    def restart_ss_v2ray(self):
        self.stop_ss_v2ray()
        self.start_ss_v2ray()

    def restart_ss_obfs(self):
        self.stop_ss_obfs()
        self.start_ss_obfs()

    def build_image(self):
        cmd = 'docker build -t %s %s/docker' % (self.ss_image, self.root_dir)
        self.shell_run(cmd)

    def cli(self):
        container_name = 'ss-cli'
        self.remove_container(container_name, force=True)
        cmd = 'sh'
        self._run_container(container_name, cmd, '-it')

    def _run_container(self, container_name, cmd, run_mod='d', ports=[]):
        envs = []
        volumes = {
                self.app_config_dir + '/local.acl': '/etc/local.acl'
                }
        args = dockerutil.base_docker_args(container_name=container_name, envs=envs, ports=ports, volumes=volumes)
        cmd_data = {}
        cmd_data['image'] = self.ss_image
        cmd_data['args'] = args
        cmd_data['cmd'] = cmd
        cmd_data['run_mod'] = run_mod
        cmd = template.render_str('docker run {{ run_mod }} -u root --restart always {{ args }} {{ image }} sh -c "{{ cmd }}"', cmd_data)
        self.shell_run(cmd)

if __name__ == '__main__':
    functocli.run_app(App)
