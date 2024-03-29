# Garry's Mod RTX Tweaks

This is a set of unofficial patches for Garry's Mod to work better with RTX Remix, fixing missing shadows, light leaks, and crashes.

DISCLAIMER: Garry's Mod is a VAC protected game. By using these patches, you accept that I am not responsible for any issues or damages resulting from the use of these patches. Do not use Garry's Mod in VAC protected servers while using RTX Remix, these patches, or any other modification.

Now that that's out of the way, BPS patches are provided to apply the following patches to your game. I recommend the use of [Floating IPS](https://www.romhacking.net/utilities/1040/) to perform the patching, as it is lightweight, simple, and straightforward to use. These patches are built against Build ID 11653227, July 7, 2023. All technical info statements below are in the context of a disassembler such as IDA Pro or Ghidra.

In the event that Garry's Mod updates and these patches have not yet been updated, a python script called `applypatch.py` has been provided to hopefully automatically create new patches for you. Place the three dlls in a folder and then run `applypatch.py folder_name`, patched versions will appear within a "patched" directory inside.

## Contents

[Patches](https://github.com/BlueAmulet/SourceRTXTweaks/tree/main/garrysmod#patches)  
[Crash Fixes](https://github.com/BlueAmulet/SourceRTXTweaks/tree/main/garrysmod#crashes)  
[Recommendations](https://github.com/BlueAmulet/SourceRTXTweaks/tree/main/garrysmod#recommendations)

## Patches

### c_frustumcull

**engine.dll:**  
253270: Change `55 8B EC` to `32 C0 C3`  
253300: Change `55 8B EC` to `32 C0 C3`

**client.dll:**  
37A9C0: Change `55 8B EC` to `32 C0 C3`

### r_forcenovis

**client.dll:**  
29E1B7: Change `00` to `01`

### r_frustumcullworld

**engine.dll:**  
F50C6: Change `7E` to `EB`  
F5163: Change `75` to `EB`

F1DD5: Change `75` to `EB`

## Crashes

### failed to lock vertex buffer in CMeshDX8::LockVertexBuffer  
### integer division by zero

Credits to [@khang06](https://github.com/khang06) for this fix, found [here](https://github.com/khang06/misc/tree/master/reversing/source/portalrtxvbfix)

**shaderapidx9.dll:**  
350D0: Change `83 C4 10 8B E5 5D C3 CC CC CC` to `85 C0 75 02 B0 04 8B E5 5D C3`

### gm_construct, gm_flatgrass, and other shader based skybox maps crash on load

Additional patches have been added that prevent the loading of shader dlls.  
If these maps still crash you, then follow the next instructions:

Go inside `garrysmod\bin` and remove or rename `game_shader_generic_garrysmod.dll` to something else.  
This will remove shaders for shader based skyboxes, and post processing effects which aren't used with RTX Remix anyway.  
Note: While the maps will load now, they still lack a skybox and may or may not have a functioning sun.

## Recommendations

Additional patches have been added that should prevent the menu from crashing RTX Remix.  
If the menu crashes you still, replace the menu files with ones from [here](https://github.com/robotboy655/gmod-lua-menu), then follow the next instructions:

Go into `garrysmod\lua\menu\menu.lua` and remove or comment the `include( "loading.lua" )` line

Go into `garrysmod\lua\menu\background.lua` and make the following change:  
```
local function ShouldBackgroundUpdate()

	return false

end
```  
This will prevent an endless spam of script errors.

Go into `garrysmod\lua\menu\custom\_errors.lua` and remove or comment the following code:  
```
	if ( GetConVarNumber( "mat_dxlevel" ) < 90 ) then
		table.insert( Errors, {
			last	= SysTime(),
			text	= "mat_dxlevel is less than 90!"
		} )
	end
```  
This will hide the "mat_dxlevel is less than 90!" message
