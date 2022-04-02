 33 y = 2463534242;
 34 def xor():
 35     global y
 36     y = y ^ (y << 13 & 0xFFFFFFFF)
 37     y = y ^ (y >> 17 & 0xFFFFFFFF)
 38     y = y ^ (y << 5 & 0xFFFFFFFF)
 39     return y
