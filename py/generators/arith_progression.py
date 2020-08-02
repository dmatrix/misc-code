#
# class example from 'Fluent Pyton'
#

from fractions import Fraction
import itertools

class ArithmethicProgression:
   """
   Class demonstrating how to create a generator by implementing
   a __iter__() method and using the yield keyword for generating
   a series results
   """
   def __init__(self, begin, step, end=None):
      self.begin = begin
      self.step = step
      self.end = end  # None -> "infinite series"

   def __iter__(self):
      # Produce a result coerced type of the self.begin
      result = type(self.begin + self.step)(self.begin)
      # Set to True if this is going to be an infinte series
      forever = self.end is None
      index = 0
      # when this loop exits so will __iter__ with the yielded list
      while forever or result < self.end:
         # Current result is produced
         yield result
         index += 1
         result = self.begin + self.step * index

# No need for class. We can achieve the same effect with a generator function

def arithprog_gen(begin, step, end=None):
   # Produce a result coerced type of the self.begin
   result = type(begin + step)(begin)
   # Set to True if this is going to be an infinte series
   forever = end is None
   index = 0
   # when this loop exits so will __iter__ with the yielded list
   while forever or result < end:
      # Current result is produced
      yield result
      index += 1
      result = begin + step * index

# Use itertools to write the same function
def artihprog_gen_iter_tools(begin, step, end=None):
   first = type(begin + step)(begin)
   ap_gen = itertools.count(first, step)
   if end is not None:
      ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)

   return ap_gen
if __name__ == '__main__':

   print(list(ArithmethicProgression(0, 1, 3)))
   print(list(ArithmethicProgression(0, 1/3, 1)))
   # Use Fractions
   print(list(ArithmethicProgression(0, Fraction(1,3),1)))
   print("-" * 50)

   # Use generator function
   print(list(arithprog_gen(0, 1, 3)))
   print(list(arithprog_gen(0, 1/3, 1)))

   # Use Fractions
   print(list(arithprog_gen(0, Fraction(1, 3), 1)))
   print("-" * 50)

   # Use iteratools gen
   print(list(artihprog_gen_iter_tools(0, 1, 3)))
   print(list(artihprog_gen_iter_tools(0, 1 / 3, 1)))
   print(list(artihprog_gen_iter_tools(0, Fraction(1, 3), 1)))
