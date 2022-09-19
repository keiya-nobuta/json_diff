import json

def diff(json_a, json_b, prefix=''):
    diffs = {}

    if json_a == json_b:
        return diffs

    if type(json_a) == type(json_b) and type(json_a) is list:
        for i, a in enumerate(json_a):
            if i < len(json_b):
                diffs.update(diff(a, json_b[i], f'{prefix}{i}:'))
            else:
                diffs[f'{prefix}{i}'] = {'-': a}

        for j, b in enumerate(json_b[i+1:]):
            diffs[f'{prefix}{i+1+j}'] = {'+': b}

    elif type(json_a) == type(json_b) and type(json_a) is dict:
        jb = json_b.copy()
        for k, v in json_a.items():
            if k in jb:
                diffs.update(diff(json_a[k], jb[k], f"{prefix}'{k}':"))
                jb.pop(k)
            else:
                diffs[f"{prefix}'{k}'"] = {'-': v}

        for k, v in jb.items():
            diffs[f"{prefix}'{k}'"] = {'+': v}
    else:
        prefix = prefix.rstrip(':')
        diffs[f'{prefix}'] = {'-': json_a, '+': json_b}

    return diffs

def _load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def _get_ptr(a, idxs):
    ptr = a
    for idx in idxs[:-1]:
        ptr = ptr[idx]

    return ptr

def inverse_patch(patch):
    for k, v in patch.items():
        if '-' in v and '+' in v:
            patch[k]['-'], patch[k]['+'] = patch[k]['+'], patch[k]['-']
        elif '-' in v:
            patch[k]['+'] = patch[k]['-']
            del patch[k]['-']
        else:
            patch[k]['-'] = patch[k]['+']
            del patch[k]['+']

def patch(a, patch, inverse=False):
    if inverse:
        inverse_patch(patch)

    for k, v in patch.items():
        idxs = k.split(':')
        for i, idx in enumerate(idxs):
            if idx.startswith("'") and idx.endswith("'"):
                idx = idx[1:-1]
            else:
                idx = int(idx)
            idxs[i] = idx

        ptr = a
        for idx in idxs[:-1]:
            ptr = ptr[idx]

        if '-' in v and '+' in v:
            ptr[idxs[-1]] = v['+']
        elif '-' in v:
            if type(idxs[-1]) is int and hasattr(ptr, "remove"):
                ptr.remove(v['-'])
            elif type(idxs[-1]) is str:
                del ptr[idxs[-1]]
            else:
                raise TypeError
        else:
            if type(idxs[-1]) is int and hasattr(ptr, "append"):
                ptr.append(v['+'])
            elif type(idxs[-1]) is str and hasattr(ptr, "keys"):
                ptr[idxs[-1]] = v['+']
            else:
                raise TypeError
