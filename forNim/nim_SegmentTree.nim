import sugar, algorithm, strformat, bitops, math
import times, random

type SegmentTree*[T] = ref object of RootObj
  data : seq[T]
  n : uint32
  op : (T,T) -> T
  default : T
  l : uint32
proc newSegmentTree*[T](data:seq[T], op:(T,T)->T, default:T) : SegmentTree[T] = 
  new(result)
  result.n = cast[uint32](data.len)
  var size = 1'u32
  while size < result.n: size = size shl 1
  result.l = size
  result.data = newSeq[T](result.l shl 1)
  result.data.fill(default)
  result.default = default
  result.op = op
  result.data[result.l ..< result.l+result.n] = data
  for i in countdown(result.l-1,1,1):
    result.data[i] = result.op(result.data[2*i], result.data[2*i+1])
proc put*[T](self:SegmentTree[T], i:sink uint32, val:T) =
  i += self.l
  self.data[i] = val
  i = i shr 1
  while i > 0:
    self.data[i] = self.op(self.data[2*i], self.data[2*i+1])
    i = i shr 1
proc get*[T](self:SegmentTree[T], i,j:sink uint32) : T =
  i += self.l
  j += self.l
  result = self.default
  while j-i > 0:
    if (i and 1'u32) > 0:
      result = self.op(self.data[i], result)
      i += 1
    if (j and 1'u32) > 0:
      result = self.op(result, self.data[j-1])
      j -= 1
    i = i shr 1
    j = j shr 1

proc perf()=
  let N : uint32 = cast[uint32](2 * (10^5))
  let samples = newSeq[int](N)

proc test()=
  let data : seq[int] = @[1,2,3]
  var seg = newSegmentTree[int](data, (a:int,b:int)=>a+b, 0)

  let i = 2'u32
  echo seg.data
  seg.put(i, 5)
  echo seg.data
  echo data
  echo i
  echo seg.get(0, 3)

