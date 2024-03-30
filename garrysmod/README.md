# Garry's Mod RTX Tweaks

This is a set of unofficial patches for Garry's Mod to work better with RTX Remix, fixing missing shadows, light leaks, and crashes.

DISCLAIMER: Garry's Mod is a VAC protected game. By using these patches, you accept that I am not responsible for any issues or damages resulting from the use of these patches. Do not use Garry's Mod in VAC protected servers while using RTX Remix, these patches, or any other modification. To protect yourself from accidentally joining a VAC protected server, run Garry's Mod with the `-insecure` launch option.

## Recommendations

### gm_construct, gm_flatgrass, and other shader based skybox maps crash on load

Additional patches have been added that prevent the loading of shader dlls.  
If these maps still crash you, then follow the next instructions:

Go inside `garrysmod\bin` and remove or rename `game_shader_generic_garrysmod.dll` to something else.  
This will remove shaders for shader based skyboxes, and post processing effects which aren't used with RTX Remix anyway.  
Note: While the maps will load now, they still lack a skybox and may or may not have a functioning sun.

### Game crashes at menu

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
