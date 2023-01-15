# Half Life 2 RTX Tweaks

This is a set of unofficial patches for Half Life 2 to work better with RTX Remix, fixing missing shadows and light leaks.

BPS patches are provided to apply the following patches to your game. I recommend the use of [Floating IPS](https://www.romhacking.net/utilities/1040/) to perform the patching, as it is lightweight, simple, and straightforward to use. These patches are built against Build ID 9963621, November 18, 2022.

## Contents

[Patches](https://github.com/BlueAmulet/SourceRTXTweaks/tree/main/hl2#patches)

## Patches

### c_frustumcull

**engine.dll:**  
23D1B0: Change `55 8B EC` to `32 C0 C3`  
23D240: Change `55 8B EC` to `32 C0 C3`

**client.dll:**  
268750: Change `55 8B EC` to `32 C0 C3`  
		  
**episodic client.dll:**  
2718F0: Change `55 8B EC` to `32 C0 C3`

### r_forcenovis

**client.dll:**  
1C2E50: Change `8A 81 44 03 00 00` to `B0 01 0F 1F 40 00`

**episodic client.dll:**  
1C42C0: Change `8A 81 44 03 00 00` to `B0 01 0F 1F 40 00`

### r_frustumcullworld

**engine.dll:**  
FD5F3: Change `7E` to `EB`  
FD685: Change `75` to `EB`

FAD4D: Change `75` to `EB`  
