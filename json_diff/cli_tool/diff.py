#!/usr/bin/env python

import sys
import json
from json_diff import _load_json, diff

def usage(ret=1):
    print('spdx_diff [option] <a> <b>')
    print('option:')
    print('  --indent=<n>: format json with indent=<n>')
    sys.exit(ret)

def main():
    if len(sys.argv) < 3:
        usage()

    a = None
    b = None
    kwds = {}
    for arg in sys.argv[1:]:
        if arg.startswith('--indent='):
            kwds['indent'] = int(arg[len('--indent='):])
        elif arg == '-h' or arg == '--help':
            usage(0)
        elif a is None:
            a = _load_json(arg)
        elif b is None:
            b = _load_json(arg)
        else:
            usage()

    if a is None or b is None:
        usage()

    print(json.dumps(diff(a, b), **kwds))

if __name__ == "__main__":
    main()
