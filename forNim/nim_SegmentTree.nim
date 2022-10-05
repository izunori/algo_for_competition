import sugar, algorithm, strformat, bitops, math
import times, random
import mersenne
import random

type SegmentTree*[T] = ref object of RootObj
  data : seq[T]
  n : uint32
  op : (T,T) -> T
  default : T
  l : uint32
proc newSegmentTree*[T](data:seq[T], op:(T,T)->T, default:T): SegmentTree[T] =
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
    result.data[i] = result.op(result.data[2'u32*i], result.data[2'u32*i+1'u32])
proc put*[T](self:SegmentTree[T], i:sink uint32, val:T) =
  i += self.l
  self.data[i] = val
  i = i shr 1
  while i > 0'u32:
    self.data[i] = self.op(self.data[2'u32*i], self.data[2'u32*i+1'u32])
    i = i shr 1
proc get*[T](self:SegmentTree[T], i,j:sink uint32): T =
  i += self.l
  j += self.l
  result = self.default
  while j-i > 0'u32:
    if (i and 1'u32) > 0'u32:
      result = self.op(self.data[i], result)
      i += 1
    if (j and 1'u32) > 0'u32:
      result = self.op(result, self.data[j-1'u32])
      j -= 1
    i = i shr 1
    j = j shr 1

proc perf()=
  let N : uint32 = cast[uint32](2 * (10^5))
  let M : uint32 = cast[uint32](2 * (10^5))

  var samples = newSeq[int](M)
  for i in 0'u32..N-1:
    samples[i] = rand(10)

  var indexes = newSeq[uint32](M)
  for i in 0'u32..N-1:
    indexes[i] = uint32(rand(int(N)))

  var data = newSeq[int](N)

  var seg = newSegmentTree(data, (a:int, b:int) => (a+b), 0.int)
  let time = cpuTime()
  for i in 0'u32..M-1:
    seg.put(indexes[i], samples[i])
  echo cpuTime() - time

proc test()=
  let data : seq[int] = @[1,2,3]
  var seg = newSegmentTree[int](data, (a:int,b:int) => (a+b), 0.int)

  echo seg.data
  seg.put(0'u32, 5)
  echo seg.data
  echo data
  echo seg.get(0'u32, 3)

test()
perf()
