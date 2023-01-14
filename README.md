# GMod RTX Tweaks

This is a set of tweaks for Garry's Mod to work better with RTX Remix, fixing missing shadows, light leaks, and crashes.

DISCLAIMER: Garry's Mod is a VAC protected game. By using these patches, you accept that I am not responsible for any issues or damages resulting from the use of these patches. Do not use Garry's Mod in VAC protected servers while using RTX Remix, these patches, or any other modification.

Now that that's out of the way, a BPS patch is provided to apply the following patches to your game. I recommend the use of [Floating IPS](https://www.romhacking.net/utilities/1040/) to perform the patching, as it is lightweight, simple, and straightforward to use. These patches are built against Build ID 8912316, June 10, 2022. All technical info statements below are in the context of a disassembler such as IDA Pro or Ghidra.

## c_frustumcull

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

**engine.dll:**  
244FC0: Change `55 8B EC` to `32 C0 C3`  
245050: Change `55 8B EC` to `32 C0 C3`

**client.dll:**  
361C00: Change `55 8B EC` to `32 C0 C3`

## r_forcenovis

Also new to Portal with RTX is r_forcenovis, which disables the BSP level visibility checks. (guessing, unsure)  
This fixes some light leaking issues.

<details>  
<summary>Technical info</summary>

Search for "CViewRender::Render" and go to the function referencing this string.  
Near the top of this function, there should be a byte sized `this` member being set to 0:  
`*(byte*)(this + 844) = 0;`  
Change this to 1.

</details>

**client.dll:**  
254522: Change `00` to `01`

## r_frustumcullworld

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

Search for "Refusing to render the map on an entity to prevent crashes!" and go to the function referencing this string.  
Later in the function is a check against `< -0.01f or -0.0099999998f`, this is a backface check, skip this check.

</details>

**engine.dll:**  
EFD36: Change `7E` to `EB`  
EFDD3: Change `75` to `EB`

ECC45: Change `75` to `EB`

## Crashes

### failed to lock vertex buffer in CMeshDX8::LockVertexBuffer

Credits to [@khang06](https://github.com/khang06) for this fix, found [here](https://github.com/khang06/misc/tree/master/reversing/source/portalrtxvbfix)

<details>  
<summary>Technical info</summary>

Search for "CMeshMgr::FindOrCreateVertexBuffer (dynamic VB)" and go to the function referencing this string.  
At the top of the function should be a function call taking two arguments, go inside this function.  
This function should consist of a single call followed by a value return:  
`function_call(0, a1, a2, v3);`  
After the function call and eax has been loaded, add in the following instructions:  
```  
test   eax,eax  
jne    +0x2  
mov    al,0x4  
```

</details>

**shaderapidx9:**  
35020: Change `83 C4 10 8B E5 5D C3 CC CC CC` to `85 C0 75 02 B0 04 8B E5 5D C3`  
