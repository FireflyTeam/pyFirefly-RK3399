try:
    from setuptools import setup
except:
    from distutils.core import setup
from distutils.command.build_ext import build_ext as _build_ext

import re,sys

PLAT_SUPPORT={
    'Rockchip RK3399':'rk3399',
}
def check_plat():
    cpuinfo = open("/proc/cpuinfo", 'r')
    for line in cpuinfo:
        m = re.match(r'^Serial\s*:\s*(.*)',line)
        if m is not None:
            break
    plat = "Rockchip RK3399"
    return PLAT_SUPPORT[plat] #use this way to install python3399 
   
    if m is None:
        print('Not found platform information!')
        return None

    try:
        plat=m.group(1)
    except:
        print('Not found hardware information!')
        return None

    for psk in PLAT_SUPPORT.keys():
        if psk in plat:
            print('FireflyP use <%s>' % PLAT_SUPPORT[psk])
            return PLAT_SUPPORT[psk]

    print('FireflyP do not support <%s>!' % plat)
    return None


fplat=check_plat()
if fplat is None:
    sys.exit(1)


setup(
    name='fireflyP',
    version='0.8.2',
    author='zhansb',
    author_email='service@t-firefly.com',
    url='http://en.t-firefly.com/en/',
    license='MIT',
    packages=['fireflyP','fireflyP.lib'],
    package_dir={'fireflyP': 'fireflyP/'+fplat, 'fireflyP.lib':'fireflyP/lib'},
    description='FireflyP is designed for using devices port on firefly platforms',
    )
