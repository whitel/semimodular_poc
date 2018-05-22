#! /usr/bin/python3

import dnf

import sys

base = dnf.Base()
base.read_all_repos()

base.fill_sack()

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

def pkg_csum(base, pkg):
    ydbi = base._yumdb.get_package(pkg)
    csum = None
    if 'checksum_type' in ydbi and 'checksum_data' in ydbi:
        csum = (ydbi.checksum_type, ydbi.checksum_data)
    else:
        pkgs = base.sack.query().available()._nevra(
                pkg.name, pkg.evr, pkg.arch)
        if len(pkgs) != 1:
            return csum
        print("Fixing:", _ui_nevra(pkg))
        rpo = pkgs[0]
        ydbi.from_repo = rpo.repoid
        if hasattr(rpo.repo, 'repoXML'):
            md = rpo.repo.repoXML
            if md and md._revision is not None:
                ydbi.from_repo_revision = str(md._revision)
            if md:
                ydbi.from_repo_timestamp = str(md._timestamp)

        ydbi.releasever = base.conf.releasever
        csum = rpo.returnIdSum()
        if csum is not None:
            ydbi.checksum_type = str(csum[0])
            ydbi.checksum_data = csum[1]
            csum = (ydbi.checksum_type, ydbi.checksum_data)
        loginuid = dnf.yum.misc.getloginuid()
        if loginuid is not None:
            ydbi.installed_by = str(loginuid)

    return csum

def fixup_pklist(base):
    pkgs = base.sack.query().installed().run()
    ret = 0
    for pkg in pkgs:
        csum = pkg_csum(base, pkg)
        if csum is None:
            print(" ** BROKEN:", nevra(pkg))
    return ret

fixup_pklist(base)
