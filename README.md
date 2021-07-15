# ImpostorCPU
## [sus]

Program designed to mimic an actual CPU, or at least try to get close to it. Basic operations like move memory, do math, etc. mimic the real thing, but the way most other things work (buses, etc.) are made up and don't look like the real thing in the slightest.

Instruction size: 11 bytes
Byte: 8 bits
Max Address Size: 8 bytes (32bit)
Other notes:
> this in no ways follows conventions for how to handle floating points, signed numbers, etc. 
> a range of addresses in memory are 32bit/8byte only (meaning only multiples of 4 in this range are writable and readable from). this is mostly to handle "buses" that irl would be 32bits wide, and also because i'm nots have the smort.
> no i didn't name it ImpostorCPU just to make among us jokes