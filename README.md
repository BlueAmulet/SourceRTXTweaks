# RTX Remix patches for Source Engine games

This is a set of unofficial patches and recommendations for various Source Engine based games, to improve lighting and reduce crashes when using RTX Remix.  
DLL Offsets are provided for use with a hex editor, and BPS patches are provided to apply all changes easily at once. I recommend the use of [Floating IPS](https://www.romhacking.net/utilities/1040/) to perform the patching, as it is lightweight, simple, and straightforward to use.

Disclaimer: Some of the games listed below make use of Valve Anti-Cheat. By using these patches, you accept that I am not responsible for any issues or damages resulting from the use of these patches. Do not use those games in VAC protected servers while using RTX Remix, these patches, or any other modification.

## Games

[Garry's Mod](https://github.com/BlueAmulet/SourceRTXTweaks/tree/main/garrysmod)  
[Half Life 2](https://github.com/BlueAmulet/SourceRTXTweaks/tree/main/hl2)

## Recommendations

The following launch options should be beneficial to all Source Engine based games:

## Technical Info

This is to help with finding the relevant code again incase a game receives and update.  
All technical info statements below are in the context of a disassembler such as IDA Pro or Ghidra.

### c_frustumcull

Portal with RTX added in c_frustumcull, which prevents objects out of view from being skipped.  
This primarily fixes missing shadows, though technically it is also a light leak.

<details>  
<summary>Technical info</summary>

Search for the following set of bytes in engine.dll or client.dll: `83 C4 0C 83 F8 02 74`  
There should be several hits in 2 functions within engine.dll, and 1 function within client.dll.  
Replace the start of the functions with the following bytes: `32 C0 C3`  
This is equal to the following instructions:  
```  
xor al, al  
retn  
```

</details>

### r_forcenovis

Also new to Portal with RTX is r_forcenovis, which disables the BSP level visibility checks. (guessing, unsure)  
This fixes some light leaking issues.

<details>  
<summary>Technical info</summary>

Search for "CViewRender::Render" and go to the function referencing this string.  
Near the top of this function, there should be a byte sized `this` member being set to 0:  
`*(byte*)(this + 844) = 0;` or `this[844] = 0;`  
The number may not be 844. Change this to 1.

If the code is optimized to make sure of a register known to be zero to assign the value:  
With a debugger such as [x64dbg](https://x64dbg.com/), set a break point on this instruction.  
Check the address listed and set a hardware byte read breakpoint on it.  
This should get you the function that reads this member, change it to the following instructions:  
```  
mov    al,0x1  
retn  
```

</details>

### r_frustumcullworld

This exists inside Source Engine already, but Portal with RTX extended it to also disable various backface culling checks.  
This fixes light leaks when a wall is not facing the camera.

<details>  
<summary>Technical info [World backfaces]</summary>

This one is hard to explain, apologies in advance.  
Search for "r_frustumcullworld" and go to the function referencing this string.  
There should be a function call with parameters (byte, "r_frustumcullworld", "1", 0)  
If using IDA Pro and the byte variable is missing, decompile the inner function and then refresh the first function.  
Go to the byte variable and skip ahead 0x1C, the dword variable here is the actual variable for r_frustumcullworld.  
Find references to this dword variable and go to the function found.  
There should be an if else statement on a function parameter, both containing a check on r_frustumcullworld and a function call.  
Go into the function call contained in else (code handled when parameter is false)  
Inside the function should be code like this, go inside the function call:  
```  
if (*(int*)var >= 0) {  
	function_call();  
	return;  
}  
```  
There will be two loops, disable the first loop entirely.  
Inside the second loop is a check against `< -0.01f or -0.0099999998f`, this is a backface check, skip this check.

</details>

<details>  
<summary>Technical info [Brush entity backfaces]</summary>

For Garry's Mod:  
	Search for "Refusing to render the map on an entity to prevent crashes!" and go to the function referencing this string.  
For other games:  
	Check for references on the -0.01f float found above, and goto the nearest function.  
	This function should also contain references to the "$AlphaTestReference" string  
Find the check against `< -0.01f or -0.0099999998f`, this is a backface check, skip this check.

</details>  
