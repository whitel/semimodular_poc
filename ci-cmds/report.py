#! /usr/bin/python

import os
import sys

def _ui_num(num):
    num = str(num)
    if len(num) ==  4:
        return "  %s.%sK" % (num[0], num[1:3])
    if len(num) ==  5:
        return " %s.%sK" % (num[0:2], num[2:4])
    if len(num) ==  6:
        return "%s.%sK" % (num[0:3], num[3:5])
    if len(num) ==  7:
        return "  %s.%sM" % (num[0], num[1:3])
    if len(num) ==  8:
        return " %s.%sM" % (num[0:2], num[2:4])
    if len(num) ==  9:
        return "%s.%sM" % (num[0:3], num[3:5])
    if len(num) == 10:
        return "  %s.%sG" % (num[0], num[1:3])
    if len(num) == 11:
        return " %s.%sG" % (num[0:2], num[2:4])
    if len(num) == 12:
        return "%s.%sG" % (num[0:3], num[3:5])
    return "%6s" % num


def parse_rpmdb(line):
    # print "JDBG:", line
    relarch, rpmdb, size = line.split()
    rel,arch = relarch.split("/")
    pkgs,checksum = rpmdb.split(':')
    pkgs = int(pkgs)
    size = int(size)
    ret = {}
    for k in ('rel', 'arch', 'rpmdb', 'size', 'pkgs', 'checksum'):
        ret[k] = locals()[k]
    return ret

def parse_tst(line):
    mod, res = line.split('=>', 1)
    mod = mod.strip()
    res = res.strip()
    if ':' not in mod:
        mods = ''
        if '/' not in mod:
            modn = mod
            modp = ''
        else:
            modn, modp = mod.split('/')
    else:
        if '/' not in mod:
            modn, mods = mod.split(':')
            modp = ''
        else:
            modn, mods = mod.split(':')
            mods, modp = mods.split('/')
    return {'mod' : mod, 'res' : res,
            'modn' : modn, 'mods' : mods, 'modp' : modp}

def parse_file(fn):
    fo = open(fn)
    beg = parse_rpmdb(fo.readline())
    tests = []
    while True:
        line = fo.readline()
        if not line:
            break
        tst = parse_tst(line)
        res = parse_rpmdb(fo.readline())
        tests.append((tst, res))
    return beg, tests

def main():
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: file|dir"
        sys.exit(1)
    
    beg = None
    tests = []
    num = 0
    for fn in sys.argv[1:]:
        if os.path.isdir(fn):
            for nfn in os.listdir(fn):
                if not nfn.startswith('test-'):
                    continue
                num += 1
                d = parse_file(fn + '/' + nfn)
                if beg is None:
                    beg = d[0]
                if beg != d[0]:
                    print "Error:", nfn, beg, d[0]
                tests.extend(d[1])
        else:
            num += 1
            d = parse_file()
            if beg is None:
                beg = d[0]
            if beg != d[0]:
                print "Error:", fn, beg, d[0]
            tests.extend(d[1])

    # print "JDBG:", tests
    print "Files:", num
    print "Tests:", len(tests)
    print "  Fails:", len([x for x in tests if x[0]['res'] != 'pass'])
    print "  Pass:",  len([x for x in tests if x[0]['res'] == 'pass'])
    print "Modules:", len(set((x[0]['modn'] for x in tests)))
    print "  Fails:", len(set((x[0]['modn'] for x in tests if x[0]['res'] != 'pass')))
    print "  Pass:",  len(set((x[0]['modn'] for x in tests if x[0]['res'] == 'pass')))

    maxmod = 0
    for tst, res in tests:
        maxmod = max(maxmod, len(tst['mod']))
    for tst, res in tests:
        if tst['res'] == 'pass':
            print "%-*s" % (maxmod, tst['mod']),
            print 'Pkgs:', _ui_num(res['pkgs'] - beg['pkgs']),
            print 'Size:', _ui_num(res['size'] - beg['size'])
        else:
            print "%-*s" % (maxmod, tst['mod']),
            print tst['res']

if __name__ == '__main__':
    main()
