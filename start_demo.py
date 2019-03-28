#!/usr/bin/python3
# Start a demo machine

import argparse
import configparser
import os

sys_root = None

def start_demo(config_file):
  try:
    cfg_file = open(config_file, "r")
    cfg = configparser.ConfigParser()
    cfg.read_file(cfg_file)
    cfg_file.close()

    sys_root = cfg["PATHS"]["sys_image_root"]
  except:
    print("Failed to load configuration - run builder.py first.")
    return

  qemu_params = ["qemu-system-x86_64",
                 "-drive file=fat:rw:fat-type=16:{root},format=raw",
                 "-no-reboot",
                 "-smp cpus=2",
                 "-cpu Haswell,+x2apic",
                 "-serial stdio", # Could change this to -debugcon stdio to put the monitor on stdio.
                 "-device nec-usb-xhci",
                 "-kernel {root}/kernel64.sys",

                 # The following arguments are simply a reminder of useful options for temporary use while debugging.
                 #"-D /tmp/qemu.log",
                 #"-d int,pcall",
                 #"--trace events=/tmp/trcevents",
                 #"-device usb-kbd",
                 #"-hda kernel_disc_image_nonlive.vdi",
                ]

  qemu_cmd = " ".join(qemu_params)
  qemu_cmd = qemu_cmd.format(**{'root' : sys_root})
  os.system(qemu_cmd)

if __name__ == "__main__":
  argp = argparse.ArgumentParser(description = "Project Azalea Builder helper")
  argp.add_argument("--config_file", type = str, default = "config/saved_config.ini", help = "Config file location")
  args = argp.parse_args()

  start_demo(args.config_file)