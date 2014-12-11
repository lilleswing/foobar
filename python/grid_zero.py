__author__ = 'leswing'

# I didn't want to implement Gaussian Elimination in GF(2)
# But turned out it was harder to find a solution then to make one :(
# Timeout

def ZMod(m):
    '''Return a function that makes Mod objects for a particular modulus m.
    '''
    def ModM(coef):
        return Mod(coef, m)
    return ModM

class FiniteGroup:
    '''Super class provides an iterator for self's group.'''

    def group(self, excludeSelf=False):
        '''Iterator over self's whole group if not excludeSelf,
        starting from self or right after it if excludeSelf.
        This version assuming subclass defines instance method next.
        '''
        if not excludeSelf:
            yield self
        f, last = self.next(), None
        while f != self:
            yield f
            f, last = f.next(last), f

    def next(self, prev=None):
        '''Cyclicly return another element of the group.
        This version depends on methods int, likeFromInt, totCodes.
        Optional argument prev ignored in this version.'''
        return self.likeFromInt((int(self)+1) % self.totCodes())


class ParamClass:
    '''Mixin class allows conversion to object with same parameters.
    Assumes method sameParam and constructor that can copy parameters.'''

    def like(self, val):
        '''convert val to a the same kind of object as self.'''
        if self.sameParam(val):
            return val  # avoid unnecessary copy - assumes immutable
        return self.__class__(val, self)

    def tryLike(self, val):
        '''convert val to the same kind of object as self, with the same
        required parameters, if possible, or return None'''
        try:
            return self.like(val)
        except:
            return None

class Mod(FiniteGroup, ParamClass): #subclass of classes above
    '''A class for modular arithmetic, mod m.
    If m is prime, the inverse() method and division operation are always
    defined, and the class represents a field.

    >>> Mod26 = ZMod(26)
    >>> x = Mod26(4)
    >>> y = Mod26(11)
    >>> z = Mod26(39)
    >>> print x+y
    15 mod 26
    >>> print z
    13 mod 26
    >>> print -x
    22 mod 26
    >>> print z - x
    9 mod 26
    >>> print x*8
    6 mod 26
    >>> print x*z
    0 mod 26
    >>> print x**6
    14 mod 26
    >>> print x/y
    24 mod 26
    >>> x == y
    False
    >>> x*y == -8
    True
    >>> e = Mod(1, 5)
    >>> for x in range(1, 5):
    ...     print x, int(e/x)
    1 1
    2 3
    3 2
    4 4
    '''

    #class invarient:
    #  self.m is the modulus
    #  self.value is the usual smallest nonnegative representative

    def __init__(self, n=0, m=None):
        '''Construct a Mod object.
        If n is a Mod, just copy its n and m, and any m parameter should match.
        If m is a Mod, take its m value.
        Otherwise both m and n should be integers, m > 1; construct n mod m.
        '''
        if isinstance(m, Mod):
            m = m.m
        if isinstance(n, Mod):
            assert m is None or m == n.m, 'moduli do not match'
            self.value = n.value; self.m = n.m
            return
        else:
            assert isinstance(m, (int, long)), 'Modulus type must be int or Mod'
            assert m > 1, 'Need modulus > 1'
        assert isinstance(n, (int, long)), 'representative value must be int'
        self.m = m; self.value = n % m

    def __str__(self):   # used by str built-in function, which is used by print
        'Return an informal string representation of object'
        return "{0} mod {1}".format(self.value, self.m)

    def __repr__(self):  # used by repr built-in function
        'Return a formal string representation, usable in the Shell'
        return "Mod({0}, {1})".format(self.value, self.m)

    def sameParam(self, other):
        'True if other is a Mod with same modulus'
        return isinstance(other, Mod) and other.m == self.m

    def __add__(self, other): # used by + infix operand
        'Return self + other, if defined'
        other = self.tryLike(other)
        if other is None: return NotImplemented
        return Mod(self.value + other.value, self.m)

    def __sub__(self, other): # used by - infix operand
        'Return self - other, if defined'
        other = self.tryLike(other)
        if other is None: return NotImplemented
        return Mod(self.value - other.value, self.m)

    def __neg__(self):# used by - unary operand
        'Return -self'
        return Mod(-self.value, self.m)

    def __mul__(self, other): # used by * infix operand
        'Return self * other, if defined'
        other = self.tryLike(other)
        if other is None: return NotImplemented
        return Mod(self.value * other.value, self.m)

    def __div__(self,other):
        'Return self/other if other.inverse() is defined.'
        other = self.tryLike(other)
        if other is None: return NotImplemented
        return self * other.inverse()

    def __eq__(self, other): # used by == infix operand
        '''Return self == other, if defined
        Allow conversion of int to same Mod type before test.  Good idea?'''
        other = self.tryLike(other)
        if other is None: return NotImplemented
        return other.value == self.value

    def __ne__(self, other): # used by != infix operand
        'Return self != other, if defined'
        return not self == other

    # operations where only the second operand is a Mod (prefix r)
    def __radd__(self, other):
        'Return other + self, if defined, when other is not a Mod'
        return self + other # commutative, and now Mod first

    def __rsub__(self, other):
        'Return other - self, if defined, when other is not a Mod'
        return -self + other # can make definite Mod first

    def __rmul__(self, other):
        'Return other * self, if defined, when other is not a Mod'
        return self * other # commutative, and now Mod first

    def __rdiv__(self,other):
        'Return other/self if self.inverse() is defined.'
        return self.inverse() * other # can make definite Mod first

    def __pow__(self, n): # used by ** infix operator
        '''compute power using successive squaring for integer n
        Negative n allowed if self has an inverse.'''
        s = self  # s holds the current square
        if n < 0:
            s = s.inverse()
            n = abs(n)
        return Mod(pow(s.value, n, s.m), s.m)
        # algorithm (but not in C):
    ##        result = Mod(1, self.m)
    ##        while n > 0:
    ##           if n % 2 == 1:
    ##              result = s * result
    ##           s = s * s  # compute the next square
    ##           n = n//2    # compute the next quotient
    ##        return result

    def __int__(self):
        'Return lowest nonnegative integer representative.'
        return self.value

    def totCodes(self):
        '''Return number of elements in the group.
        This is an upper bound for likeFromInt.'''
        return self.m

    def likeFromInt(self, n):
        '''Int code to Mod object'''
        assert 0 <= n < self.m
        return Mod(n, self.m)

    def __nonzero__(self):
        """Returns True if the current value is nonzero.
        (Used for conversion to boolean.)
        """
        return self.value != 0

    def __hash__(self):
        ''' Hash value definition needed for use in dictionaries and sets.'''
        return hash(self.value)

    def modulus(self):
        '''Return the modulus.'''
        return self.m

    def inverse(self):
        '''Return the multiplicative inverse or else raise a ValueError.'''
        (g,x,y) = xgcd(self.value, self.m)
        if g == 1:
            return Mod(x, self.m)
        raise ValueError, 'Value not invertible'

def xgcd(a,b):
    """Extended GCD:
    Returns (gcd, x, y) where gcd is the greatest common divisor of a and b
    with the sign of b if b is nonzero, and with the sign of a if b is 0.
    The numbers x,y are such that gcd = ax+by."""
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a,b)
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy

# EXPLANATION:
# Mathematical analysis reveals that at each stage in the calculation
# the current remainder can be expressed in the form ax + by for some
# integers x, y.  Moreover, the x-sequence and y-sequence are
# generated by the recursion (where q is the integer quotient of the
# current division):
#
#         new x = prev x - q * x;   new y = prev y - q * y
#
# and where the initial values are x = 0, prev x = 1, y = 1, prev y = 0.
# Moreover, upon termination the x and y sequences have gone one step
# too far, (as has the remainder), so return the previous x, y values.

def gauss_jordanModPow2(m):
    """Puts given matrix (2D array) into the Reduced Row Echelon Form.
    Returns True if successful, False if 'm' is singular.
    Assumes all elements are in Z/nZ with n a powr of 2.  One line changed
    Based on floating point code by Jarno Elonen,April 2005,
    released into Public Domain"""
    # Only change from field version is 6th line.
    (h, w) = (len(m), len(m[0]))
    for y in range(0,h):
        for pivot in range(y, h):    # Find nonzero (invertible) pivot
            if m[pivot][y].value % 2 != 0: #ONLY CHANGE - easy test for invertible
                break
        else: # Python syntax with FOR not if
            return False
        if y != pivot:
            (m[y], m[pivot]) = (m[pivot], m[y]) # swap pivot row
        if m[y][y] != 1:
            inv = m[y][y].inverse()             # normalize exactly immediately
            for x in range(y, w):
                m[y][x] *= inv
        for y2 in range(y+1, h):    # Eliminate column y, below row y
            c = m[y2][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c
    for y in range(h-1, 0-1, -1): # Backsubstitute
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                m[y2][x] -=  m[y][x] * m[y2][y]
    return True


def matConvert(mat, cls):
    '''Return a new matrix/list with all elements e of matrix m replaced by
    cls(e).  The name is chosen to suggest a class conversion,
    but any function could be used for 1-1 replacements of non-list elements.
    '''
    if isinstance(mat, list):
        return [matConvert(r, cls) for r in mat]
    return cls(mat)


def flip(m, index):
    size = len(m)
    row = index // size
    col = index % size
    for i in xrange(size):
        m[row][i] += 1
        m[i][col] += 1
    m[row][col] += 1


def valid(m):
    for row in m:
        for value in row:
            if value % 2 != 0:
                return False
    return True


def answer(matrix):
    size = len(matrix)
    row_indexes = list()
    col_indexes = list()
    for i in xrange(size):
        row_part = list()
        col_part = list()
        for j in xrange(size):
            row_part.append(i * size + j)
            col_part.append(j * size + i)
        row_indexes.append(row_part)
        col_indexes.append(col_part)

    mp = list()
    row_size = size * size
    for i in xrange(size):
        for j in xrange(size):
            mp_row = [0] * row_size
            my_switches = set()
            my_switches.update(row_indexes[i])
            my_switches.update(col_indexes[j])
            for index in xrange(len(mp_row)):
                if index in my_switches:
                    mp_row[index] = 1
            mp_row.append(matrix[i][j])
            mp.append(mp_row)
    mp = matConvert(mp, ZMod(2))
    gauss_jordanModPow2(mp)
    total = 0
    for i in xrange(len(mp)):
        row = mp[i]
        val = row[-1].value
        if val == 1:
            flip(matrix, i)
        total += val
    if valid(matrix):
        return total
    return - 1


def test(m, a):
    #m = [[1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]]
    #on = [1, 1, 0, 0]
    #for i in xrange(len(m)):
    #    row = m[i]
    #    row.append(on[i])
    #print(gauss_jordan(m))
    #print(m)
    a1 = answer(m)
    if a1 != a:
        print("WRONG %s %d %d" % (m, a1, a))


test([[1, 1], [0, 0]], 2)
#test([[1, 1, 1], [1, 0, 0], [1, 0, 1]], -1)

