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


AUTOCALIBRATE_COMMAND = "roslaunch intrinsic_autocalibration intrinsic_autocalibration.launch veh:={veh} vel:={vel}"
AVAHI_SOCKET = "/var/run/avahi-daemon/socket"


class DTCommand(DTCommandAbs):
    @staticmethod
    def command(shell: DTShell, args):
        prog = "dts duckiebot intrinsic_autocalibration DUCKIEBOT_NAME"
        usage = """

    %(prog)s
"""
        parser = argparse.ArgumentParser(prog=prog, usage=usage)
        parser.add_argument("--network", default="host", help="Name of the network to connect to")
        parser.add_argument(
            "--image",
            help="The base image for running"
        )
        parser.add_argument("hostname", default=None, help="Name of the Duckiebot to control")
        parser.add_argument(
            "--vel",
            default=0.4,
            help="Velocity for wheels"
        )
        parser.add_argument(
            "--img_num",
            default=150,
            help="Number correct images for calibration"
        )
        parsed_args = parser.parse_args(args)
        duckiebot_ip = get_duckiebot_ip(duckiebot_name=parsed_args.hostname)
        network_mode = parsed_args.network
        velocity = float(parsed_args.vel)
        img_num = parsed_args.img_num
        run_controller(
                parsed_args.hostname, parsed_args.image, duckiebot_ip, network_mode, velocity, img_num
            )


def run_controller(hostname, image, duckiebot_ip, network_mode, velocity, img_num):
    container_name = "autocalibration_%s" % hostname
    client = check_docker_environment()
    remove_if_running(client, container_name)
    host_ip = subprocess.run(["hostname", "-I"], capture_output=True, text=True)
    host_ip = str(host_ip.stdout).split()[0]
    env = set_default_env(hostname, duckiebot_ip, host_ip)
    env["DISPLAY"] = os.environ["DISPLAY"]
    env["VELOCITY"] = velocity
    env["IMG_NUM"] = img_num 
    volumes = {"/tmp/.X11-unix": {"bind": "/tmp/.X11-unix", "mode": "rw"}}

    dtslogger.info("Running %s on localhost with environment vars: %s" % (container_name, env))

    params = {
        "image": image,
        "name": container_name,
        "network_mode": network_mode,
        "environment": env,
        "privileged": True,
        "stdin_open": True,
        "tty": True,
        "command": AUTOCALIBRATE_COMMAND.format(veh=hostname, vel=velocity),
        "detach": True,
        "volumes": volumes
    }

    #pull_if_not_exist(client, params["image"])
    client.containers.run(**params)

    cmd = "docker attach %s" % container_name
    dtslogger.info("attach command: %s" % cmd)
    start_command_in_subprocess(cmd)


def set_default_env(hostname, ip, host_ip):
    env = {
        "ROS_HOSTNAME": host_ip,
        "ROS_MASTER": hostname,
        "VEHICLE_NAME": hostname,
        "VEHICLE_IP": ip,
        "ROS_MASTER_URI": "http://%s:11311" % ip,
    }
    return env
