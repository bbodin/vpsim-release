import sys
import os

def launch_vpsim(conf):
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundled executable
        base_dir = sys._MEIPASS
    else:
        # If the application is run as a normal Python script
        base_dir = os.path.dirname(os.path.realpath(__file__))

    vpsim_directory = base_dir
    sys.path.append(f"{vpsim_directory}")
    sys.path.append(f"{vpsim_directory}/Python")
    sys.path.append(f"{vpsim_directory}/Python/Libs")
    sys.path.append(f"{vpsim_directory}/Python/Platforms")

    # Launch VPSim
    from armv8_platform import FullSystem
    full_sys = FullSystem(conf)
    full_sys.build(simulate=True,wait=True,silent=False,)
