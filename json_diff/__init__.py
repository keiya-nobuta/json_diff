import json

def _match4(l1, l2):
    i = j = 0
    diffs = []
    len1 = len(l1)
    len2 = len(l2)
    while True:
        if i >= len1:
            while j < len2:
                diffs.append((-1, j))
                j = j + 1
            break
        elif j >= len2:
            while i < len1:
                diffs.append((i, -1))
                i = i + 1
            break

        if l1[i] == l2[j]:
            i = i + 1
            j = j + 1
            continue

        if i+1 < len1 and l1[i+1] == l2[j]:
            diffs.append((i, -1))
            i = i + 2
            j = j + 1
            continue

        if j+1 < len2 and l1[i] == l2[j+1]:
            diffs.append((i, j))
            i = i + 1
            j = j + 2
            continue

        if i+2 < len1 and l1[i+2] == l2[j]:
            diffs.append((i, -1))
            diffs.append((i+1, -1))
            i = i + 3
            j = j + 1
            continue

        if j+2 < len2 and l1[i] == l2[j+2]:
            diffs.append((i, j))
            diffs.append((i, j+1))
            i = i + 1
            j = j + 3
            continue

        if i+3 < len1 and l1[i+3] == l2[j]:
            diffs.append((i, -1))
            diffs.append((i+1, -1))
            diffs.append((i+2, -1))
            i = i + 4
            j = j + 1
            continue

        if j+3 < len2 and l1[i] == l2[j+3]:
            diffs.append((i, j))
            diffs.append((i, j+1))
            diffs.append((i, j+2))
            i = i + 1
            j = j + 4
            continue

        diffs.append((i, -1))
        diffs.append((i, j))
        i = i + 1
        j = j + 1

    return diffs

def diff(json_a, json_b, prefix=''):
    diffs = {}

    if json_a == json_b:
        return diffs

    if type(json_a) == type(json_b) and type(json_a) is list:
        len1 = len(json_a)
        len2 = len(json_b)
        longer = len1 if len1 > len2 else len2

        k = len(json_a)
        for i, j in _match4(json_a, json_b):
            if i >= 0 and j >= 0:
                diffs.setdefault(f'{prefix}{i}', {})
                diffs[f'{prefix}{i}'].update({'+': json_b[j]})
                k = k + 1
                continue

            if j < 0:
                diffs.setdefault(f'{prefix}{i}', {})
                diffs[f'{prefix}{i}'].update({'-': json_a[i]})
                k = k - 1

            if i < 0:
                diffs.setdefault(f'{prefix}{k}', {})
                diffs[f'{prefix}{k}'].update({'+': json_b[j]})
                k = k + 1

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
