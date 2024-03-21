import sys
import os

patches32 = {
'garrysmod/bin/client.dll': [
    ['558bec538b5d08568b7510578b', '32c0c3'], # c_frustumcull
    ['00e8????efff8b0d??????10??????????????????????????ff', '01'], # r_forcenovis
],
'bin/engine.dll': [
    ['558bec538b5d08568b7510578b7d0c565753e8????ffff83c40c83f8027466', '32c0c3'], # c_frustumcull
    ['558bec538b5d08568b7510578b7d0c565753e8??ddffff83c40c83f8027453', '32c0c3'], # c_frustumcull
    ['7530f30f10', 'eb'], # brush entity backfaces
    ['7e3ceb06', 'eb'], # world backfaces
    ['75438b4604', 'eb'], # world backfaces
],
'bin/materialsystem.dll': [
    ['558bec83ec7c57', '31c0c3'], # no shader loading
],
'bin/shaderapidx9.dll': [
    ['0f4cd68bf7', '909090'], # four hardware lights
    ['83c4108be55dc3cccccccccccccccccc55', '85c07502b0048be55dc3'], # zero sized buffer
    ['558bec51a140200e10538b5d', 'c3'] # vertex shader constants
],
}

patches64 = {
'bin/win64/client.dll': [
    ['4883ec480f1022', '32c0c3'], # c_frustumcull
    ['0fb68154', 'b001c3'], # r_forcenovis [getter]
],
'bin/win64/engine.dll': [
    # TODO: Missing c_frustumcull patches
    ['753cf30f10', 'eb'], # brush entity backfaces
    ['7e5244', 'eb'], # world backfaces
    ['753c498b4204', 'eb'], # world backfaces
],
'bin/win64/materialsystem.dll': [
    ['40554155', '31c0c3'], # no shader loading
],
'bin/win64/shaderapidx9.dll': [
    ['480f4ec1c7', '90909090'], # four hardware lights
    ['4833cce804c5', '85c0750466b80400'], # zero sized buffer
    ['48895c240848896c24104889742418574883ec20488b05', 'c3'] # vertex shader constants
],
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
if os.path.isdir(os.path.join(vers, 'bin/win64')):
    patches = patches64
else:
    patches = patches32

# Check if all files are present
ver = {}
missing = False
for fname in patches:
    path = os.path.join(vers, fname)
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
    for patch in patches[fname]:
        findpos = findmask(ver[fname], patch[0])
        findpos2 = findmask(ver[fname], patch[0], findpos+1)
        if findpos != -1 and findpos2 == -1:
            pdata = bytes.fromhex(patch[1])
            print(f'{findpos:X}: Changing `{ver[fname][findpos:findpos+len(pdata)].hex()}` to `{patch[1]}`')
            if fname not in ver_out:
                ver_out[fname] = ver[fname]
            ver_out[fname][findpos:findpos+len(pdata)] = pdata
        else:
            logwarn(f'Failed to locate patch for {patch[0]}')
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
