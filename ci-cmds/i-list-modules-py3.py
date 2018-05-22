#! /usr/bin/python3

import dnf

import sys

base = dnf.Base()
base.read_all_repos()
base.fill_sack()

mods = []

for module in base.repo_module_dict.values():
    for stream in module.values():
        for version in stream.values():
            mods.append((module.name, stream.stream, version.version, ",".join(sorted(version.profiles))))

if len(sys.argv) > 1 and sys.argv[1] == 'latest':
    last = None
    for i in sorted(mods):
        if last is not None and (last[0] != i[0] or last[1] != i[1]):
            print("%20s %10s %16s %s" % last)
        last = i
    if last is not None:
            print("%20s %10s %16s %s" % last)
else:
    for i in sorted(mods):
        print("%20s %10s %16s %s" % i)

