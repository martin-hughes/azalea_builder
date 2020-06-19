#!/usr/bin/python3
# Project Azalea build assistance script.
#
# The idea of this script is to contain all of the steps needed to build all of the libraries and executables needed
# for a complete Azalea system.

from contextlib import contextmanager
import os
import configparser
import shutil
import argparse

def main(config):

  # Job list:
  # 1 - Install kernel headers
  # 2 - Build + install libc
  # 3 - Build + install libc++
  # 4 - Build + install ACPICA
  # 5 - Build + install kernel + user mode tools
  # 6 - Copy in timezone data

  sys_image_root = config["PATHS"]["sys_image_root"]

  simple_build("INSTALL KERNEL HEADERS",
               config["PATHS"]["kernel_base"],
               "scons install-headers sys_image_root='%s'" % sys_image_root)

  simple_build("MAKE LIBC",
               config["PATHS"]["libc_base"],
               "scons sys_image_root='%s'" % sys_image_root,
               "scons install")

  simple_build("MAKE LIBC++",
               config["PATHS"]["kernel_base"],
               ("python3 build_support/cxx_builder.py --sys_image_root='%s' --llvm_base='%s' --kernel_base='%s'" %
                (sys_image_root, config["PATHS"]["llvm_base"], config["PATHS"]["kernel_base"])))

  simple_build("MAKE ACPICA",
               config["PATHS"]["acpica_base"],
               "scons sys_image_root='%s'" % sys_image_root,
               "scons install")

  simple_build("MAKE KERNEL",
               config["PATHS"]["kernel_base"],
               "scons sys_image_root='%s'" % sys_image_root)

  tz_path = os.path.abspath(os.path.join(sys_image_root, "system", "data", "timezones"))
  if not os.path.exists(tz_path):
    # Assume that if the path exists then timezone data has already been installed.
    print ("")
    print ("Copying timezone information. This can take a minute or two.")
    shutil.copytree("/usr/share/zoneinfo", tz_path)

# An easy way to wrap CD calls so they get reverted upon exiting or exceptions.
#
# Cheekily taken from this Stack Overflow answer:
# https://stackoverflow.com/questions/431684/how-do-i-change-directory-cd-in-python/24176022#24176022
@contextmanager
def cd(newdir):
  prevdir = os.getcwd()
  os.chdir(os.path.abspath(os.path.expanduser(newdir)))
  try:
    yield
  finally:
    os.chdir(prevdir)

def simple_build(name, path, *commands):
  print("")
  print(name)
  print(len(name) * "-")
  with cd(path):
    for c in commands:
      if os.system(c) != 0:
        raise ChildProcessError("Failed to execute '" + name + "'")

def regenerate_config(config, cmd_line_args):
  args_dict = vars(cmd_line_args)

  if "PATHS" not in cfg.sections():
    cfg["PATHS"] = { }

  paths = config["PATHS"]

  populate_field(paths, args_dict, "kernel_base", "Kernel source base directory")
  populate_field(paths, args_dict, "libc_base", "Azalea Libc source base directory")
  populate_field(paths, args_dict, "llvm_base", "LLVM source base directory")
  populate_field(paths, args_dict, "acpica_base", "Azalea ACPICA source base directory")
  populate_field(paths, args_dict, "sys_image_root", "Azalea system image root directory")

def populate_field(config_section, args_dict, cfg_name, human_name):
  if args_dict[cfg_name]:
    config_section[cfg_name] = args_dict[cfg_name]
  if cfg_name not in config_section:
    config_section[cfg_name] = prompt_for_value(human_name)

def prompt_for_value(field_name):
  prompt_str = "Enter the following: " + field_name + "\n"
  return input(prompt_str)

if __name__ == "__main__":
  try:
    argp = argparse.ArgumentParser(description = "Project Azalea Builder helper")
    argp.add_argument("--kernel_base", type = str, help = "Location of the base of the Azalea kernel source code tree")
    argp.add_argument("--libc_base", type = str, help = "Location of the base of the Azalea Libc source code tree")
    argp.add_argument("--llvm_base", type = str, help = "Location of LLVM source code tree")
    argp.add_argument("--acpica_base", type = str, help = "Location of the base of the Azalea ACPICA source code tree")
    argp.add_argument("--sys_image_root", type = str, help = "Root of the Azalea system image's filesystem")
    argp.add_argument("--config_file", type = str, default = "config/saved_config.ini", help = "Config file location")
    args = argp.parse_args()

    flags = "r" if os.path.exists(args.config_file) else "a+"
    try:
      cfg_file = open(args.config_file, flags)
    except (OSError, IOError):
      print ("Unable to open file ", args.config_File, ". Check intermediate folders created.")
      exit()

    cfg = configparser.ConfigParser()
    cfg.read_file(cfg_file)
    cfg_file.close()

    regenerate_config(cfg, args)
    main(cfg)

    cfg_file = open(args.config_file, "w")
    cfg.write(cfg_file)
    cfg_file.close()

  except KeyboardInterrupt:
    print ("Build cancelled")