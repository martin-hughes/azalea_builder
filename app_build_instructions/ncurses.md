# Building ncurses for Azalea

These instructions assume you're using a Linux machine, and have a copy of the ncurses codebase on it already. These
instructions were built using ncurses 6.1.

*Note: ncurses support in Azalea is not yet complete, you will probably not successfully compile any programs linking
to ncurses.*

Simply execute the following commands, after editing the paths to reflect your system.

```
export LDFLAGS='-L/xxx/azalea_sys_image/apps/developer/libc/lib -L/xxx/azalea_sys_image/apps/developer/kernel/lib -static'
export LIBS='-lazalea_linux_shim -lazalea_libc -lazalea'
export CFLAGS='-Wall -mno-red-zone -nostdinc -nostdlib -nodefaultlibs -mcmodel=large -ffreestanding -fno-exceptions -U _LINUX -U __linux__ -D __AZALEA__ -isystem /xxx/azalea_sys_image/apps/developer/libc/include -isystem /xxx/azalea_sys_image/apps/developer/kernel/include'
export CXXFLAGS='-Wall -mno-red-zone -nostdinc -nostdinc++ -nostdlib -nodefaultlibs -mcmodel=large -ffreestanding -fno-exceptions -U _LINUX -U __linux__ -D __AZALEA__ -isystem /xxx/azalea_sys_image/apps/developer/libc/include -isystem /xxx/azalea_sys_image/apps/developer/kernel/include -isystem /xxx/azalea_sys_image/apps/developer/libcxx-kernel/include/c++/v1 -static'
export CPPFLAGS='-Wall -mno-red-zone -nostdinc -nostdinc++ -nostdlib -nodefaultlibs -mcmodel=large -ffreestanding -fno-exceptions -U _LINUX -U __linux__ -D __AZALEA__ -isystem /xxx/azalea_sys_image/apps/developer/libc/include -isystem /xxx/azalea_sys_image/apps/developer/kernel/include -isystem /xxx/azalea_sys_image/apps/developer/libcxx-kernel/include/c++/v1 -static'
mkdir azalea_build
cd azalea_build
../configure --host=x86_64-elf --with-build-cc=clang --without-ada --disable-db-install --without-manpages --without-progs --without-tack --without-tests --with-build-cc=clang --without-cxx-binding --prefix=/xxx/azalea_sys_image/apps/developer/ncurses --includedir=/xxx/azalea_sys_image/apps/developer/ncurses/include --libdir=/xxx/azalea_sys_image/apps/developer/ncurses/lib cf_cv_working_poll='yes'
make
make install
```
## Notes:

1. When configuring we set `cf_cv_working_poll` because the ncurses configure script assumes path names that don't
   exist in Azalea and the test for poll() gives a false result.

2. You'll then need to copy the relevant output into a location to allow you to use it in while building Azalea programs.
