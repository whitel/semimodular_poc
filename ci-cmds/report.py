#! /usr/bin/python

import os
import sys

html = False

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
    def usage():
        if len(sys.argv) < 2:
            print >>sys.stderr, "Usage: [html] file|dir"
            sys.exit(1)
    usage()
    if sys.argv[1] == 'html':
        html = True
        sys.argv = sys.argv[0:1] + sys.argv[2:]
    usage()

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
        elif os.path.exists(fn):
            num += 1
            d = parse_file(fn)
            if beg is None:
                beg = d[0]
            if beg != d[0]:
                print "Error:", fn, beg, d[0]
            tests.extend(d[1])
        else:
            print >>sys.stderr, " No such file or directory:", fn
            continue
    if html:
        prnt_html(beg, num, tests)
    else:
        prnt_text(beg, num, tests)

def prnt_html(beg, num, tests):
    print "<h2>Tests:", len(tests), "</h2>"
    print "<dl>"
    print "<dt>", "Failures", "</dt>", "<dd>", len([x for x in tests if x[0]['res'] != 'pass'])
    print "</dd>"
    print "<dt>", "Passes", "</dt>", "<dd>", len([x for x in tests if x[0]['res'] == 'pass'])
    print "</dd></dl>"
    print "<h2>", "Modules:", len(set((x[0]['modn'] for x in tests))), "</h2>"
    print "<dl>"
    print "<dt>", "Failures", "</dt>", "<dd>", len(set((x[0]['modn'] for x in tests if x[0]['res'] != 'pass')))
    print "</dd>"
    print "<dt>", "Passes", "</dt>", "<dd>", len(set((x[0]['modn'] for x in tests if x[0]['res'] == 'pass')))
    print "</dd></dl>"

    print "<h2> Modules </h2>"
    print "<table class=\"pure-table pure-table-striped\">"
    print "<thead>"
    print "<tr> <th> Name </th><th> Stream </th><th> Profile </th>"
    print "<th> Result </th> <th> Packages </th> <th> Size </th> </tr>"
    print "</thead>"

    print "<tbody>"
    for tst, res in tests:
        if tst['res'] == 'pass':
            print "<tr class=\"pass\">"
        elif 'SYS' in tst['res']:
            print "<tr class=\"sysfail\">"
        else:
            print "<tr class=\"fail\">"
        print "<td> %s </td>" % (tst['modn'])
        print "<td> %s </td>" % (tst['mods'])
        print "<td> %s </td>" % (tst['modp'])
        if tst['res'] == 'pass':
            print "<td> Pass </td>"
            print " <td> %s </td> " % _ui_num(res['pkgs'] - beg['pkgs']),
            print " <td> %s </td> </tr>" % _ui_num(res['size'] - beg['size'])
        else:
            print "<td> %s </td>" % tst['res']
            print "<td> </td>" 
            print "<td> </td>" 
            print "</tr>" 
    print "</tbody>"
    print "</table>"

def prnt_text(beg, num, tests):
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
