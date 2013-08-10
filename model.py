
from z3 import *

init('./Z3/z3-4.3.2.30df2837fbff-x86-ubuntu-12.04/bin/libz3.so')

x = Int('x')
y = Int('y')
solve(x > 2, y < 10, x + 2*y == 7)

# a sequence of steps, each step represents a creation of new value out of existing ones
# initial values are 0, 1 and x_0
# e.g., step 1 for ops not and shl1:
# v1 = y_1 * (not  (z_1_1 * 0 + z_1_2 * 1 + z_1_3 * x_0))
#    + y_2 * (shl1 (z_2_1 * 0 + z_2_2 * 1 + z_2_3 * x_0))
# where x, y - binary
# subject to:
# sum y = 1
# sum z = 1

# global:
#  must be a tree? all new values must be used exactly once - except for the result
#  enforce number of steps?
#  sum of ys for any given operator >= 1

