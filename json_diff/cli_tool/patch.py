#!/usr/bin/env python

import sys
import json
from json_diff import _load_json, patch

def usage(ret=1):
    print('spdx_patch [option] <spdx.json> <patch>')
    print('option:')
    print('  --inverse: interpretation <patch> to inverse-patch.')
    print('  --indent=<n>: enable json format with indent=<n>')
    sys.exit(ret)

def main():
    if len(sys.argv) < 3:
        usage()

    inverse=False
    kwds = {}
    source = None
    diff = None
    for arg in sys.argv[1:]:
        if arg == '--inverse':
            inverse=True
        elif arg.startswith('--indent='):
            kwds['indent'] = int(arg[len('--indent='):])
        elif arg == '-h' or arg == '--help':
            usage(0)
        elif source is None:
            source = _load_json(arg)
        elif diff is None:
            diff = _load_json(arg)
        else:
            usage()

    if source is None or diff is None:
        usage()

    patched = patch(source, diff, inverse)
    print(json.dumps(patched, **kwds))

if __name__ == "__main__":
    main()
