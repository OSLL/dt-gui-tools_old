import argparse
import os
import platform
import socket
import subprocess

import docker
from dt_shell import DTCommandAbs, DTShell, dtslogger
from dt_shell.env_checks import check_docker_environment
from utils.cli_utils import start_command_in_subprocess
from utils.docker_utils import remove_if_running, pull_if_not_exist
from utils.networking_utils import get_duckiebot_ip


AUTOCALIBRATE_COMMAND = "roslaunch extrinsic_autocalibration extrinsic_autocalibration.launch veh:={veh}"
BRANCH = "daffy"
#GUI_ARCH = "amd64"
#ARCH = "arm32v7"
#GUI_DEFAULT_IMAGE = "duckietown/dt-gui-tools:" + BRANCH + "-" + GUI_ARCH
#CLI_DEFAULT_IMAGE = "duckietown/dt-gui-tools:" + BRANCH + "-" + ARCH
AVAHI_SOCKET = "/var/run/avahi-daemon/socket"


class DTCommand(DTCommandAbs):
    @staticmethod
    def command(shell: DTShell, args):
        prog = "dts duckiebot autocalibrate_extrinsic DUCKIEBOT_NAME"
        usage = """

    %(prog)s
"""
        parser = argparse.ArgumentParser(prog=prog, usage=usage)
        parser.add_argument("--network", default="host", help="Name of the network to connect to")
        parser.add_argument(
            "--image",
       
            help="The base image for running",
        )
        parser.add_argument("hostname", default=None, help="Name of the Duckiebot to control")
        parsed_args = parser.parse_args(args)
        
        duckiebot_ip = get_duckiebot_ip(duckiebot_name=parsed_args.hostname)
        network_mode = parsed_args.network
        run_controller(
                parsed_args.hostname, parsed_args.image, duckiebot_ip, network_mode
            )


def run_controller(hostname, image, duckiebot_ip, network_mode):
    container_name = "autocalibration_%s" % hostname
    client = check_docker_environment()
    #duckiebot_client = docker.DockerClient("tcp://" + duckiebot_ip + ":2375")
    remove_if_running(client, container_name)
    env = set_default_env(hostname, duckiebot_ip)

    dtslogger.info("Running %s on localhost with environment vars: %s" % (container_name, env))

    params = {
        "image": image,
        "name": container_name,
        "network_mode": network_mode,
        "environment": env,
        "privileged": True,
        "stdin_open": True,
        "tty": True,
        "command": AUTOCALIBRATE_COMMAND.format(veh=hostname),
        "detach": True,
    }

    #pull_if_not_exist(client, params["image"])
    client.containers.run(**params)

    cmd = "docker attach %s" % container_name
    dtslogger.info("attach command: %s" % cmd)
    start_command_in_subprocess(cmd)


def set_default_env(hostname, ip):
    env = {
        "ROS_HOSTNAME": "10.135.4.51",
        "ROS_MASTER": hostname,
        "VEHICLE_NAME": hostname,
        "VEHICLE_IP": ip,
        "ROS_MASTER_URI": "http://%s:11311" % ip,
    }
    return env

'''
def run_controller(hostname, image, duckiebot_ip, network_mode):
    container_name = "autocalibration_%s" % hostname
    duckiebot_client = docker.DockerClient("tcp://" + duckiebot_ip + ":2375")
    remove_if_running(duckiebot_client, container_name)
    env = set_default_env(hostname, duckiebot_ip)

    dtslogger.info("Running %s on localhost with environment vars: %s" % (container_name, env))

    params = {
        "image": image,
        "name": container_name,
        "network_mode": network_mode,
        "environment": env,
        "privileged": True,
        "stdin_open": True,
        "tty": True,
        "command": AUTOCALIBRATE_COMMAND.format(veh=hostname),
        "detach": True,
    }

    pull_if_not_exist(duckiebot_client, params["image"])
    duckiebot_client.containers.run(**params)

    cmd = "docker %s attach %s" % ("-H %s.local" % hostname, container_name)
    dtslogger.info("attach command: %s" % cmd)
    start_command_in_subprocess(cmd)


def set_default_env(hostname, ip):
    env = {
        "ROS_HOSTNAME": "localhost",
        "ROS_MASTER": hostname,
        "VEHICLE_NAME": hostname,
        "VEHICLE_IP": ip,
        "ROS_MASTER_URI": "http://%s:11311" % ip,
    }
    return env
'''
