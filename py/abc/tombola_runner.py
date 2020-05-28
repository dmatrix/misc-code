import doctest
import sys

from tombola import Tombola
# Modules to test
import bingo, lotto, tombolist

TEST_FILE='tombola_tests.rst'
TEST_MSG='{0} {1}:attempted:{2} tests, {1}:failed:{2} failed - {2}'


def main(argv):
   verbose='-v in argv'
   # List direct descendents of Tomobala
   real_subclasses = Tombola.__subclasses__()
   #virtual_subclasses = list(Tombola._abc_registery)

   for cls in real_subclasses:
      do_test(cls, verbose=verbose)

def do_test(cls, verbose=False):
   print(f"testing class={cls}")
   res = doctest.testfile(
      TEST_FILE,
      globs={'ConcreteTombola':cls},
      verbose=verbose,
      optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
   tag = ' FAIL' if res.failed else 'OK'
   print(TEST_MSG.format(cls.__name__, res, tag))

if __name__ == '__main__':
   main(sys.argv)
