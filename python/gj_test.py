__author__ = 'leswing'
'''Matrix manipulation, with adjoined rows, Gauss-Jordan algoithms for
different types or fields and rings, inversion.
Omits general gauss_jordanMod
'''

#from mod import ZMod, Mod
#from xgcd import mgcd, xgcd

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

def mgcd(a,b):
    """Returns (gcd, x, y, s, t) where
    gcd is the greatest common divisor of a and b, with the sign of b
    if b is nonzero, and with the sign of a if b is 0;
    the numbers x,y, s, t are such that
       gcd = xa+yb
         0 = sa+tb
    and abs(xt-ys) = 1
    Otherwise put: the determinant of matrix (hence m in name)
        x y
        s t
    has magnitude 1, and multiplied by column vector
           a
           b
    is column vector
           gcd
           0
    """
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a, b)
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy, x, y


def gauss_jordan(m, eps = 1.0/(10**10)):
    """Puts given matrix (2D array) into the Reduced Row Echelon Form.
       Returns True if successful, False if 'm' is singular.
       Specifically designed to minimize float roundoff.
       NOTE: make sure all the matrix items support fractions!
             An int matrix will NOT work!
       Written by Jarno Elonen in April 2005, released into Public Domain"""
    (h, w) = (len(m), len(m[0]))
    for y in range(0,h):
        maxrow = y
        for y2 in range(y+1, h):    # Find max pivot
            if abs(m[y2][y]) > abs(m[maxrow][y]):
                maxrow = y2
        (m[y], m[maxrow]) = (m[maxrow], m[y])
        if abs(m[y][y]) <= eps:     # Singular?
            return False
        for y2 in range(y+1, h):    # Eliminate column y
            c = m[y2][y] / m[y][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c
    for y in range(h-1, 0-1, -1): # Backsubstitute
        c  = m[y][y]
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                m[y2][x] -=  m[y][x] * m[y2][y] / c
        m[y][y] /= c
        for x in range(h, w):       # Normalize row y
            m[y][x] /= c
    return True

def gauss_jordanExactField(m):
    """Puts given matrix (2D array) into the Reduced Row Echelon Form.
    Returns True if successful, False if 'm' is singular.
    Assumes all element operations are calulated exactly,
    as in a finite field or the rational numbers, but NOT float.
    Use function gauss_jordan for float calculation.
    Use other varants for rings with 0-divisors.
    Based on floating point code by Jarno Elonen,April 2005,
    released into Public Domain"""
    # commentM and comment are not a part of the algorithm -
    #    they just shows progress if global variable VERBOSE is set to True.
    (h, w) = (len(m), len(m[0]))
    commentM('Starting m', m)
    for y in range(0,h):
        comment('Working on row', y)
        for pivot in range(y, h):    # Find nonzero (invertible) pivot
            if m[pivot][y] != 0: break
        else:
            return False
        if y != pivot:
            (m[y], m[pivot]) = (m[pivot], m[y]) # swap pivot row
            commentM('swap rows', y, pivot, m)
        if m[y][y] != 1:
            inv = 1/m[y][y]             # normalize exactly immediately
            for x in range(y, w):
                m[y][x] *= inv
            commentM('Normalizing row', y, 'Multiple by inverse', int(inv), m)
        for y2 in range(y+1, h):    # Eliminate column y, below row y
            c = m[y2][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c
        if y+1 < h: commentM('Zeroed column', y, 'below row', y, m)
    for y in range(h-1, 0-1, -1): # Back substitute
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                m[y2][x] -=  m[y][x] * m[y2][y]
    commentM('Final, after back substitution', m)
    return True

def gauss_jordanModPow2(m):
    """Puts given matrix (2D array) into the Reduced Row Echelon Form.
    Returns True if successful, False if 'm' is singular.
    Assumes all elements are in Z/nZ with n a powr of 2.  One line changed
    Based on floating point code by Jarno Elonen,April 2005,
    released into Public Domain"""
    # Only change from field version is 6th line.
    (h, w) = (len(m), len(m[0]))
    commentM('Starting m', m)
    for y in range(0,h):
        comment('Working on row', y)
        for pivot in range(y, h):    # Find nonzero (invertible) pivot
            if m[pivot][y].value % 2 != 0: #ONLY CHANGE - easy test for invertible
                break
        else: # Python syntax with FOR not if
            return False
        if y != pivot:
            (m[y], m[pivot]) = (m[pivot], m[y]) # swap pivot row
            commentM('swap rows', y, pivot, m)
        if m[y][y] != 1:
            inv = m[y][y].inverse()             # normalize exactly immediately
            for x in range(y, w):
                m[y][x] *= inv
            commentM('Normalizing row', y, 'Multiple by inverse', int(inv), m)
        for y2 in range(y+1, h):    # Eliminate column y, below row y
            c = m[y2][y]
            for x in range(y, w):
                m[y2][x] -= m[y][x] * c
        if y+1 < h: commentM('Zeroed column', y, 'below row', y, m)
    for y in range(h-1, 0-1, -1): # Backsubstitute
        for y2 in range(0,y):
            for x in range(w-1, y-1, -1):
                m[y2][x] -=  m[y][x] * m[y2][y]
    commentM('Final, after back substitution', m)
    return True

def gauss_jordanMod(m):
    """Puts given matrix (2D array) into the Reduced Row Echelon Form.
    Returns True if successful, False if 'm' is singular.
    Assumes all element are modular with some mod n.
    This version is the most general.  More efficient alternatives:
    If n is prime: gauss_jordanExactField
    If n is a power of 2: gauss_jordanModPow2
    Based on floating point code by Jarno Elonen,April 2005,
    released into Public Domain"""

    print '''Doing nothing:
      You need to write gauss_jordanMod in gaussJordan2, or use
      the gaussJordan module, via gaussJordan.pyc.'''

def comment(*args):
    '''print variable length parameter list.'''
    if VERBOSE:
        for arg in args:
            print arg,
        print

def commentM(*args):
    '''Print variable length parameter list, with a matrix/list last.'''
    if VERBOSE:
        comment(*args[:-1])
        display(args[-1])

def makeMat(height, width, elt=0.0):
    ''' Make a matrix with given height, width, filled with elt.'''
    return [[elt for i in range(width)] for j in range(height)]

def identity(height, ONE=1.0):
    '''Return the ientity matrix of size height.
    The value of ONE sets the type of the elements.'''
    ans = makeMat(height, height, ONE-ONE)
    for i, r in enumerate(ans):
        r[i] = ONE
    return ans

def adjoin(m, b):
    '''mutate matrix m, appending rows of matrix b(of same height)'''
    for i, r in enumerate(m):  # enumerate pairs index and element
        r += b[i] # augment the row with b's row, mutating the row of m

def collapseColumns(m, start, past):
    ''' mutate m, removing column c: start <= c < past.'''
    for r in m:
        del(r[start:past]) # remove part from row, mutating the row

def mul(m1, m2, ans=None):
    '''Multiply matrices m1*m2, using ans as place for the answer if not None.
    Returns the answer.
    If m1 is a simple list, it is taken as a row matrix.
    If m2 is a simple list, it is taken as a column matrix.
    The result is always a new matrix (list of lists).
    '''

    if not isinstance(m1[0], list): # left lit to row matrix
        m1 = [m1]
    h = len(m1)
    k = len(m1[0])
    if not isinstance(m2[0], list): # right list to column matrix
        m2 = transpose([m2])
    assert k == len(m2)
    w = len(m2[0])
    if ans is None:
        ans = makeMat(h, w)
    for r in range(h):
        for c in range(w):
            tot = 0
            for i in range(k):
                tot += m1[r][i]*m2[i][c]
            ans[r][c] = tot
    return ans

def linComb(m1, m2, a=1, b=1):
    '''return a*m1 + b*m2 for same sized matrices/lists m1 and m2,
    and scalar (not list) multipliers a, b.'''
    if isinstance(m1, list):
        return [linComb(r1, r2, a, b) for (r1, r2) in zip(m1, m2)]
        # if seq1 contains s0, s1, ..., seq2 contains t0, y1, ...,
        # then zip(seq1, seq2) contains (s0, t0), (s1, t1), ....
    return m1*a + m2*b

add = linComb # just addition with default parameters used

def sub(m1, m2):
    '''return m1 - m2 for same sized matrices/lists m1 and m2.'''
    return linComb(m1, m2, 1, -1)

def matConvert(mat, cls):
    '''Return a new matrix/list with all elements e of matrix m replaced by
    cls(e).  The name is chosen to suggest a class conversion,
    but any function could be used for 1-1 replacements of non-list elements.
    '''
    if isinstance(mat, list):
        return [matConvert(r, cls) for r in mat]
    return cls(mat)

convertMat = matConvert # original naming convention inconsistent!

def copyMat(m):
    '''Return a matrix/list copying each non-list element in matrix m.'''
    def same(x):
        return x
    return matConvert(m, same)

def transpose(m):
    '''Return a new matrix that is the transpose of m.
    If a single list is provided rather than a list of lists, it is treated
    as a single row matrix, [m].
    '''
    if not isinstance(m[0], list):
        m = [m]
    return [[r[j] for r in m] for j in range(len(m[0]))]

def mxvSolve(m, v, gj = gauss_jordan):
    '''solve mx = v for square matrix m, replacing v with the solution x.
    If v is a single list, it is understood as a column matrix.
    Return True on success.
    '''
    isVec = not isinstance(v[0], list)
    vOrig = v
    if isVec:  # convenience conversion
        v = transpose(v)
    m = copyMat(m)
    adjoin(m, v)
    success = gj(m)
    collapseColumns(m, 0, len(m))
    if isVec:
        vOrig[:] = transpose(m)[0]
    else:
        vOrig[:] = m
    return success

def invert(m, gj=gauss_jordan, cls='ignore!'):
    '''Return True and convert m to its inverse in place if possible,
    using Gauss-Jordan variant gj.
    Return False otherwise, and m is not meaningful.
    cls is ignored - obsolete, not needed.'''
    ONE = m[0][0] - m[0][0] + 1  # right class for identity
    v = identity(len(m), ONE)
    success = mxvSolve(m, v, gj)
    m[:] = v
    return success

# Only testing/display functions follow.

def display(m, label=None, colWidth=5):
    '''Pretty print a matrix or list; also prints a scalar.'''
    if not isinstance(m, list):
        if label: print label,
        print m
        return
    if not isinstance(m[0], list):
        if not label:
            label = 'Plain list:'  #? note source as list vs 1 row matrix
        m = [m]
    if label:
        print label
    if isinstance(m[0][0], Mod):
        print 'Elements are mod', m[0][0].modulus()
        m = matConvert(m, int)
    for r in m:
        for x in r:
            print format(x, str(colWidth)),
        print

def showOff(m, cls=float, f=gauss_jordan):
    '''Show off inversion of matrix m using Gauss-Jordan version f,
    where the elements e of m are transformed first to cls(e).
    '''
    m = matConvert(m, cls)
    mc = copyMat(m)
    display(m, 'Matrix to reduce, using ' + f.func_name)
    adjoin(m, identity(len(m), cls(1)))
    display(m, 'With lines adjoined')
    if not f(m):
        print 'Failed!'
    else:
        display(m, 'After GJ variant ' + f.func_name)
    showInvert(mc, f, cls)

def showInvert(m, gj=gauss_jordan, cls=float):
    '''Show off inversion of matrix m using Gauss-Jordan version gj,
    where the elements e of m are transformed first to cls(e).
    '''
    display(m, 'Matrix; Now do inverse in one function call:')
    mc = convertMat(m, cls) # fixed!
    setVerbose(False)
    if not invert(mc, gj):
        print 'Not invertible'
    oldVerbose()
    display(mc, 'Inverted')
    check = mul(m, mc)
    commentM('Multiply and check', check)
    assert  check == identity(len(m), cls(1))

def showMxvSolve(m, v, gj=gauss_jordan, cls=float, verbose=False):
    '''Show off inversion of matrix m using Gauss-Jordan version gj,
    where the elements e of m are transformed first to cls(e).
    '''
    m = matConvert(m, cls)
    v = matConvert(v, cls)
    display(m, 'Matrix')
    display(v, 'v:')
    vc = copyMat(v)
    isVec = not isinstance(v[0], list)
    setVerbose(verbose)
    if not mxvSolve(m, vc, gj):
        print 'Not invertible'
    oldVerbose()
    display(vc, 'Solution')
    check = mul(m, vc)
    if isVec:
        check = transpose(check)[0]
    commentM('Multiply and check', check)
    assert  check == v

def showLinComb(*param):
    '''See linComb for parameters.  Display all parametersand result.'''
    showOp(linComb,
           ['Testing linComb, return a*m1 + b*m2', 'm1', 'm2', 'a', 'b'],
           *param)

def showOp(f, labels, *param):
    print labels[0]
    for i, p in enumerate(param):
        display(p, labels[i+1])
    display(f(*param), 'result')


VERBOSE = False
_V_STACK = []

def setVerbose(verbose):
    '''Set global verbosity, remember old value; pair with an oldVerbose call.
    '''
    global VERBOSE
    _V_STACK.append(VERBOSE)
    VERBOSE = verbose

def oldVerbose():
    '''Recall last global verbosity value remembered by setVerbose.'''
    global VERBOSE
    VERBOSE = _V_STACK.pop()


def test():
    '''test of GassJordan versions.'''
    m = ([[1., 2.],
          [4., 7.] ])
    m2 = ([[0., 1.],
           [1., 7.] ])
    m3 = [[8, 7],
          [3, 5]]
    m4 = [[88, 5, 119],
          [26, 2, 37],
          [55, 29,53]]
    m5 = [[88, 5, 19],
          [33, 2, 37],
          [55, 29,53]]

    m6 = [[ 84,  17,  23],
          [140,  11,   2],
          [105,  19,  44]]

    Mod2 = ZMod(2)

    #showOff(m)
    #showOff(m2)
    m = matConvert(m, int)
    m2 = matConvert(m2, int)
    #showOff(m, Mod11, gauss_jordanExactField)
    #showOff(m2, Mod11, gauss_jordanExactField)

    showOff(m3, Mod2, gauss_jordanModPow2)
    #showOff(m4, Mod128, gauss_jordanModPow2)

    v = [1, 2, 3]
    showMxvSolve(m4, v, gauss_jordanModPow2, Mod16)

    ##    showOff(m3, Mod16, gauss_jordanMod)  # homework!
    ##    showOff(m4, Mod128, gauss_jordanMod)
    ##    showOff(m5, Mod90, gauss_jordanMod)
    ##    showOff(m6, Mod180, gauss_jordanMod)
    showLinComb(m, m2, 2, -1)
    showOp(sub, ['Testing sub(m1,m2)', 'm1', 'm2'],
           matConvert(m4, Mod128), matConvert(m5, Mod128))

if __name__ == '__main__':
    VERBOSE = True
    test()