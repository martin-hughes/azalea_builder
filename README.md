# Project Azalea Build Helper

This project contains a system intended to help build a working system using the Azalea kernel, starting from any other
system that has a Linux-like build toolchain.

More information about Project Azalea can be found on its [Github Page](https://github.com/martin-hughes/project_azalea)

## Prerequisites

To compile the full system, you will need the following tools and libraries installed:

From the Azalea repositories:
- azalea_libc source code
- azalea_acpica source code
- azalea_libcxx builder source code
- project_azalea (the main kernel and tools) source code.

From other locations:
- libcxx (part of the LLVM suite) source code
- Python 2.6 or later (*)
- GCC 5.4 or later (no longer tested)
- Clang 6.0.0 or later (earlier versions may work, but are not tested)
- SCons (*)
- NASM (*)
- libvirtualdisk (https://github.com/martin-hughes/libvirtualdisk) (*) - only used in the test scripts.
- Qemu - The demo virtual machine runs on qemu, and qemu-nbd is required to create disk images from scratch. (optional)
- Virtualbox - Required to generate disk images from scratch (optional) and can be used as a test system.
- GRUB2 2.02 beta 2 or later - Required to generate disk images from scratch. (optional)
- Doxygen - Only needed to generate documentation. (optional)
- Visual Studio - only needed if doing a Windows build (optional, see below)

## Building and testing an Azalea system

To build a system simply execute `./builder.py` from the root of this source tree. You will be prompted to enter the
locations of the various repositories and a location to build a system image in.

Once building is complete, and provided that there are no errors, run `start_demo.py` to launch a QEmu instance that
boots the kernel.