# Why do bitwise operations?
## Maybe we to isolate bits, because they represent true/false
## "All cryptographers know how to do is XOR"
## Bitwise operations can be faster
​
​
Operation      Boolean Operator     Bitwise Operator
AND                   &&                 &
OR                    ||                 |
XOR                   --                 ^
NOT                   !                  ~
​
a = True
b = False
(a && b) == False
​
  0b10000011
& 0b01010101
------------
  0b00000001
​
  0b00110101
& 0b10101010
------------
  0b00100000
​
  0b01
  0b10
  0b00
​
OR
a = True
b = False
(a || b) == True
​
  0b10101110
| 0b11010001
------------
  0b11111111
​
  0b00101110
| 0b10100110
------------
  0b10101110 
​
XOR
"exclusive or"
"There can only be one"
a = False
b = True
(a xor b) == True
​
a = True
b = True
(a xor b) == False
​
   0b10101101
^  0b00110110
-------------
   0b10011011
​
NOT
​
~0b10101010
-----------
 0b01010101
​
 # djb2 hash >>
 Rightshifting
   0b10101010
   0b01010101 >> 1
   0b00101010 >> 2
   0b00010101 >> 3
   0b00001010 >> 4
   0b00000001 >> 7
   0b00000000 >> 8
​
​
Left bitshifting
   0b10101010
  0b101010100 << 1
 0b1010101000 << 2
​
​
   0b101010100000 << 4
   0b00001010 >> 4
​
How could we extract the leftmost bit?
We want it on its own?
    v
  0b10101010  >> 7
​
 
 Bitmasking 
   0b10101010
 & 0b00000011
   -----------
   0b00000010
​
       vv
   0b10101010
​
1. Move them to the side
  - Rightshift the first nibble
2. Mask out all the other bits
  - Mask out the other two
​
​
   0b10101010 >> 4
​
   0b00001010
 & 0b00000011
 ------------
   0b00000010
​
Apply all this (shifting and masking) to extract instruction length aka number of operands
​
Apply shifting and masking to extract whether this is an ALU op.
​
ADD = 0b10100000
​
ADD register1 register2
​
​
num_operands = ADD >> 6
is_alu_operation = (ADD >> 5) & 0b1
​
pc += num_operands + 1
​
0b10100000 >> 5
0b101 & 0b001--> 0b1
​
​
​
(1 and 0) --> 0
0b00001110
0b00000011