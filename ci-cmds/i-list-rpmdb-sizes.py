#! /usr/bin/python3

import dnf

import sys

base = dnf.Base()
base.read_all_repos()
# sack.load_system_repo(build_cache=False)

base.fill_sack(load_available_repos=False)

mods = []

rn2m = {}

def envra(pkg):
    return "%s:%s-%s-%s.%s" % (pkg.epoch, pkg.name, pkg.version, pkg.release, pkg.arch)
def nevra(pkg):
    return "%s-%s:%s-%s.%s" % (pkg.name, pkg.epoch, pkg.version, pkg.release, pkg.arch)
def nvra(pkg):
    return "%s-%s-%s.%s" % (pkg.name, pkg.version, pkg.release, pkg.arch)

def _ui_nevra(pkg):
    if str(pkg.epoch) == '0':
        return nvra(pkg)
    else:
        return nevra(pkg)

def _ui_envra(pkg):
    if str(pkg.epoch) == '0':
        return nvra(pkg)
    else:
        return envra(pkg)

class RPMDBVersion(object):
    def __init__(self):
        self._num = 0
        self._chksum = dnf.yum.misc.Checksums(['sha1'])

    def __str__(self):
        return "%u:%s" % (self._num, self._chksum.hexdigest())

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, basestring):
            return str(self) == other
        if self._num != other._num:
            return False
        if self._chksum.digest() != other._chksum.digest():
            return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def update(self, pkg, csum):
        self._num += 1
        # self._chksum.update(str(pkg)) -- broken by DNF
        self._chksum.update(_ui_envra(pkg))
        # print(_ui_envra(pkg), csum is not None)
        if csum is not None:
            self._chksum.update(csum[0])
            self._chksum.update(csum[1])


def pkg_csum(base, pkg):
    ydbi = base._yumdb.get_package(pkg)
    csum = None
    if 'checksum_type' in ydbi and 'checksum_data' in ydbi:
        csum = (ydbi.checksum_type, ydbi.checksum_data)
    return csum

def os_ver(base):
    return "%s/%s" % (base.conf.releasever, base.conf.arch)

def rpmdb_version(base):
        main = RPMDBVersion()
        pkgs = base.sack.query().installed().run()
        # pkgs = base._do_package_lists(pkgnarrow='installed').installed
        for pkg in pkgs:
            csum = pkg_csum(base, pkg)
            main.update(pkg, csum)
        return main

def dlsize(base):
    pkgs = base.sack.query().installed().run()
    ret = 0
    for pkg in pkgs:
        ret += pkg.downloadsize
    return ret

def pksize(base):
    pkgs = base.sack.query().installed().run()
    ret = 0
    for pkg in pkgs:
        ret += pkg.installsize
    return ret

def print_pklist(base):
    pkgs = base.sack.query().installed().run()
    ret = 0
    for pkg in pkgs:
        csum = pkg_csum(base, pkg)
        if csum is None:
            print(nevra(pkg))
        else:
            csum = "%s:%s" % csum
            print(nevra(pkg), csum)
    return ret

print(os_ver(base), rpmdb_version(base), pksize(base))
if len(sys.argv) > 1 and sys.argv[1] == 'version':
    sys.exit(0)
print_pklist(base)
