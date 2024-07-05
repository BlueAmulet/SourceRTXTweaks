import sys
import os

# Generic patches for most 32bit source engine games
patches32 = {
'bin/engine.dll': [
    [('558bec538b5d08568b7510578b7d0c565753e8????ffff83c40c83f8027466', 0), '31c0c3'], # c_frustumcull
    [('015b5dc3cccccccc55', 8), '31c0c3'], # c_frustumcull
    [('db7530', 1), 'eb'], # brush entity backfaces
    [('88894d??85d27e', 6), 'eb'], # world backfaces
    [('75438b??04f3', 0), 'eb'], # world backfaces
],
'bin/shaderapidx9.dll': [
    [('b80000000f4c', 4), '909090'], # four hardware lights
    [('9483c410', 1), '85c07502b0048be55dc3'], # zero sized buffer
    [('558bec8b451053568b750833', 0), '31c0c3'], # shader constants
],
'bin/client.dll': [
    [('558bec538b5d08568b7510578b', 0), '31c0c3'], # c_frustumcull
    [[
        ('c6????03000000e8??????ff8b????????10', 6, '01'), # m_bForceNoVis [mov 1]
        ('889f??030000', 0, '0887') # m_bForceNoVis [mov bl]
        ]],
    [[
        ('8a81??030000c3cccccccccccccccccc8b', 0), # m_bForceNoVis [getter]
        ('cccccccccccccccccc8a814403', 9) # m_bForceNoVis [alt getter]
        ], 'b001c3'],
],
'bin/datacache.dll': [
    [('647838302e767478', 0), '647839302e767478'], # force load dx9 vtx
],
}

# Incomplete Garry's Mod 64bit patches
patches64 = {
'bin/win64/engine.dll': [
    # TODO: Missing c_frustumcull patches
    [('753cf30f10', 0), 'eb'], # brush entity backfaces
    [('7e5244', 0), 'eb'], # world backfaces
    [('753c498b4204', 0), 'eb'], # world backfaces
],
'bin/win64/shaderapidx9.dll': [
    [('480f4ec1c7', 0), '90909090'], # four hardware lights
    [('4833cce8??c503004881c448', 0), '85c0750466b80400'], # zero sized buffer
    [('4883ec084c', 0), '31c0c3'] # shader constants
],
'bin/win64/client.dll': [
    [('4883ec480f1022', 0), '31c0c3'], # c_frustumcull
    [('0fb68154', 0), 'b001c3'], # r_forcenovis [getter]
]
}

# Colored log output
try:
    import colorama
    colorama.just_fix_windows_console()

    def logwarn(*args, **kwargs):
        print(colorama.Fore.YELLOW, end='')
        print(*args, **kwargs)
        print(colorama.Style.RESET_ALL, end='')

    def logerror(*args, **kwargs):
        print(colorama.Fore.RED, end='')
        print(*args, **kwargs)
        print(colorama.Style.RESET_ALL, end='')
except:
    logwarn = print
    logerror = print

if len(sys.argv) < 1 or len(sys.argv) > 2:
    print('Usage: applypatch.py [folder]')
    sys.exit(1)

# Verify arguments
if len(sys.argv) >= 2:
    vers = sys.argv[1]
    if not os.path.isdir(vers):
        logerror(f'Error: [{vers}]: No such directory')
        sys.exit(1)
else:
    vers = os.getcwd()

# Select patches
if os.path.exists(os.path.join(vers, 'bin/win64/engine.dll')):
    patches = patches64
else:
    patches = patches32

# Check if all files are present
ver = {}
missing = False
for fname in list(patches):
    path = os.path.join(vers, fname)
    if not os.path.exists(path) and fname == 'bin/client.dll':
        # Attempt to locate client.dll
        for dir in os.listdir(vers):
            tpath = os.path.join(vers, dir, fname)
            if os.path.exists(tpath):
                nname = os.path.join(dir, fname).replace('\\', '/')
                print(f'Found {fname} as {nname}')
                patches[nname] = patches.pop(fname)
                path = tpath
                fname = nname
                break
    if not os.path.exists(path):
        logerror(f'Error: Missing file [{fname}]')
        missing = True
    else:
        print(f'Loading {fname}')
        with open(path, 'rb') as f:
            ver[fname] = bytearray(f.read())
if missing:
    sys.exit(1)

def findmask(data, hexstr, start=0):
    if '??' not in hexstr:
        return data.find(bytes.fromhex(hexstr), start)
    parts = hexstr.split('??')
    while True:
        findpos = data.find(bytes.fromhex(parts[0]), start)
        if findpos == -1:
            return -1
        good = True
        checkpos = findpos
        for part in parts:
            if part != '':
                bpart = bytes.fromhex(part)
                if data[checkpos:checkpos+len(bpart)] != bpart:
                    good = False
                    break
            checkpos += (len(part) // 2) + 1
        if good:
            return findpos
        start = findpos + 1

# Apply all patches
ver_out = {}
problems = False
os.makedirs(os.path.join(vers, 'patched'), exist_ok=True)
for fname in patches:
    print(f'\nPatching {fname}')
    for patchdata in patches[fname]:
        if type(patchdata[0]) == tuple:
            patchset = [patchdata[0]]
        else:
            patchset = patchdata[0]
        patched = False
        for i, patch in enumerate(patchset):
            findpos = findmask(ver[fname], patch[0])
            findpos2 = findmask(ver[fname], patch[0], findpos+1)
            if findpos != -1 and findpos2 == -1:
                findpos += patch[1]
                if len(patch) >= 3:
                    patchbytes = patch[2]
                else:
                    patchbytes = patchdata[1]
                pdata = bytes.fromhex(patchbytes)
                if len(patchset) > 1:
                    extra = f' [Patch #{i}]'
                else:
                    extra = ''
                print(f'{findpos:X}: Changing `{ver[fname][findpos:findpos+len(pdata)].hex()}` to `{patchbytes}`{extra}')
                if fname not in ver_out:
                    ver_out[fname] = ver[fname]
                ver_out[fname][findpos:findpos+len(pdata)] = pdata
                patched = True
                break
        if not patched:
            if len(patchset) > 1:
                logwarn(f'Failed to locate any patch for {", ".join([x[0] for x in patchset])}')
            else:
                logwarn(f'Failed to locate patch for {patchset[0][0]}')
            for patch in patchset:
                start = 0
                locations = []
                while True:
                    findpos = findmask(ver[fname], patch[0], start)
                    if findpos != -1:
                        locations.append(f'{findpos:X}')
                        start = findpos+1
                    else:
                        break
                if len(locations) > 0:
                    logwarn(f'    Found {patch[0]} at {", ".join(locations)}')
            problems = True

# Save patches
print('\nWriting changes to "patched" folder')
for fname in patches:
    if fname in ver_out:
        print(f'Writing {fname}')
        oname = os.path.join(vers, 'patched', fname)
        os.makedirs(os.path.dirname(oname), exist_ok=True)
        with open(oname, 'wb') as f:
            f.write(ver_out[fname])
    else:
        print(f'No patches applied to {fname}')

if problems:
    logwarn('\nWarning: Not all patches applied successfully')
