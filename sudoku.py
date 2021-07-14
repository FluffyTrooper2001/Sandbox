import          itertools, functools


topleft =lambda i,N:i//N*N
flatten =lambda a:functools.reduce(list.__add__,[[*e]for e in a])
celln = lambda  a,i,j,N:flatten([e[topleft(i,N):topleft(i,N)+N]for e in a[topleft(j,N):topleft(j,N)+N]])
R = lambda N:   [*range(1,N**2+1)]
r2 = lambda N:  [*range(N**2)]
r = lambda N:   [*range(N)]
rij = lambda    N:[*itertools.product(r2(N), repeat=2)]

def aligned(i,  j, N):
    a = {(i, k) for k in r2(N)} | {(k, j)for k in r2(N)}
    x, y =      topleft(i,N),topleft(j,N)
    b = {(x+k,  y+l)for k,l in itertools.product(r(N),repeat=2)}
    return[* (  a|b) ^ {(i, j)}]

class           permutations:
  def __init__( self, N):
    self.N =    N
  def           __contains__(self, array):
    N2 = (N:=   self.N)**2
    for i,e in  enumerate(array):
      if not e: continue
      a = [int( f)for f in array]
      a.pop(    i)
      if int(e) not in R(N) or e in a:
        return  False
    return len( array)==N2

def pad(a, p,   l='', r=''):
    return l+p+ p.join([str(e)for e in a])+p+r

class           SolutionError(RuntimeError):
                pass

class Solved(   StopIteration):
    __str__ =   lambda s:"Puzzle Solved!"

class           UberSolved(KeyboardInterrupt):
    level   =   0
    __str__ =   lambda s:"Puzzle Solved!"
    def         __init__(self, m):
        self.   NN = len(m)
        N=      self.NN**0.5//1
        while   N**2<self.NN:N+=1
        self.   N=int(N)
        self.   NN=int(N**2)
        self.   matrix = m
        super(  ).__init__()

class cell(     set):
  __bool__ =    lambda s:len(s)==1#"number placed"
  tied =        None#hasattr? nahhh
  def tie(self, other, number):#bowties are cool
    if number   in self.R:#not the programming language R
      self.     tied |= {number:other}
      other.    tied |= {number:self}
      k = {*    self.tied}&{*other.tied}
      if len(   k)==2:
        c = [   self,other][len(self.tied)==2]
        for e   in{*c}:
         if e   not in k:[self - e,other - e]
    return      self
  def untie(    self, number):
      if number in self.tied:
         other= self.tied.pop(number)
         number in other.tied and other.untie(number)
  def __str__(  self):
      if len(   self)>1:return' '
      elif not  self:return'!'
      else:     return repr(self)
  def __repr__( self):
      if self:  return int(self).__str__()
      else:     return set(self).__str__()
  def __init__( self, __a, i, j, N):
      self.     coords = i, j
      if __a.   __class__ is int:__a={__a}
      super().  __init__(__a)
      self.     tied = {}
      self.N =  N
      self.r =  r(N)
      self.r2 = r2(N)
      self.R =  R(N)
  def __int__(  self):return self.__index__()
  def           __index__(self):
    if not len( self):
      raise     SolutionError(f'Conflict detected: {self.coords}')
    if          self:
      a ,=      self
      if a not  in self.R:raise SolutionError(f"Unknown element: {a}")
      return    a
    else:return 0
  def __hash__( self):return hash(int(self))
  def __eq__(   self, other:int):
    return not  not self and int(self)==other
  def __ne__(   self, other:int):return other not in self
  def __sub__(  self, other):
      if other  in self.tied:
          self. tied[other] += other
          self. untie(other)
      if {other } < self:self ^= {other}
      return    self
  def __add__(  self, other):
      if other  in self:
          if    other in self.tied:
                cell = self.tied[other]
                self.untie(other)
          else:
            for tie,cell in self.tied.copy().items():
                self.untie(tie)
                not cell and tie in cell and cell + tie
          self  &= {other}
      elif      self:self ^= self|{other}
      if self:  self.tied = {}
      return    self
  def __xor__(  self, other):
      return {  e for e in self if e not in other}
  def           __invert__(self):
      self |=   {*r2(self.N)}
      return    self

blank_ids =     lambda N:[[0 for i in r2(N)]for j in r2(N)]
blank_sol =     lambda N:[[cell(R(N), i, j, N)for i in r2(N)]for j in r2(N)]

class puzzle:
    guessed =   solved = _passkey = 0
    celln =     lambda s,i,j:celln(s.solve,i,j,s.N)
    notes =     ""
    __iter__ =  lambda s:iter(s.solve)

    @property
    def done(   self):
      N2 = (    N:=self.N)**2
      count =   [0]*N2
      for i,j   in rij(N):
        if      self[i,j]:
                count[int(self[i,j])-1]+=1
      return{   i+1 for i,e in enumerate(count)if e==9}

    def         check_solvable_legacy(self):
      try:self. __class__(self.matrix,solve_now=True).check_solved()
      except    SolutionError:return False
      except    Solved:return True
      except    UberSolved:return True
      except    Exception:return False
      else:     return False

    def         check_solvable(self):
      self.     check_solved()
      try:p =   self.__class__(self.matrix, solve_now=False, N=self.N)
      except    SolutionError:return False
      except    Solved:return True
      except    Exception:return False
      while     p.reduce():...
      try:      self.check_solved()
      except    Solved:return True
      except    SolutionError:return False
      except    Exception:return False
      else:     return False

    def get(    self,i=None,j=None, /):
      r = self. r2
      if i not  in r:return self.matrix
      if j not  in r:return self.matrix[i]
      return    self.matrix[j][i]

    def         aligned(self, i, j):
      return[   self[k,l]for k,l in aligned(i,j, self.N)]
    
    def set(    self, i, j, n, /):
      if i not  in self.r2 or j not in self.r2:raise          SolutionError('Invalid Number')
      self[i,   j] + n if n in self.R else(()for()in()).throw(SolutionError('Invalid Number'))

    def         __getitem__(self, ij):
      r = self. r2
      try:
        i,j =   ij
        assert  i in r and j in r
        return  self.solve[j][i]
      except    TypeError:
        j =     ij
        return  self.solve[j]

    def         transpose(self):
        return[ [*yeet]for yeet in zip(*self.solve)]

    def         __setitem__(
          self, ij, value
      ):
         r, R = self.r2, self.R
         i, j = ij
         assert i in r and j in r and value in R
         self.  guessed = 1
         self[  i,j] + value

    def         generate(self, matrix):
      N = self. N
      for i in  self.r2:
        matrix[ i ] += [0]*N
      for i,j   in rij(N):
        ...
      return    NotImplemented

    def         assert_unique(self):
      for i   in self.R:
        if i  not in flatten(self.matrix):
              return False
        else: return True

    def         __init__(
                self, matrix=None, *,
                coords:dict[tuple[int,int],int]=None,
                level=0, solve_now=True, N=1
    ):
      self.     level= level

      if matrix is None and coords is None:
        self.N= N
        self.   NN=N**2
        matrix= [[]]*self.NN
        self.   generate(matrix)
      elif      matrix is None:
        while True:
          try:
            NN =    min([N**2, max(flatten([*coords]))+1])
            N = 1
            while   N**2 < NN:N+=1
            self.   N=N
            self.   NN=N**2
            matrix= blank_ids(self.N)
            for i,j in coords:
                    matrix[j][i] = coords[i,j]
            break
          except IndexError:N+=1
      else:
        self.   NN=len(matrix)
        N = 1
        while   N**2 < self.NN:N+=1
        self.   N=N
        if      coords:
           for  i,j in coords:
                try:matrix[j][i] = coords[i,j]
                except ValueError:continue
                except IndexError:continue

      self.r=   r(N)
      self.r2 = r2(N)
      self.R=   R(N)
      self.     solve=blank_sol(N)

      for i,j   in rij(N):
        n,a  =  matrix[j][i],(i,j)
        if      n:
                self[a] + n
          
      try:      self.save()
      except    Solved as e:
        if not  self.solved:
                self.solved = 1
                self.view()
                print(e)
        else:   print("Already solved.")
        return
      except    SolutionError as e:
       if not self.guessed:
        @lambda E:(()for()in()).throw(E,e)
        class   InvalidPuzzle(SolutionError):pass
      if        self.matrix != blank_ids(N)and solve_now and self.assert_unique():
        try:    self.run()
        except  SolutionError as e:
                self.__init__(self.rollback, solve_now=False)
        except  Solved as e:
          if    not all([self[a]for a in rij(N)]):
                self.solved = 0
                print('Warning: Solved prematurely triggered')
                return
          if    self.solved:return
          self. solved = 1
          if    self.level: raise UberSolved(self.matrix)
          else: self.view()or print(e)
        except  UberSolved  as m:
          if    self.level: raise
          else: self.__init__(m.matrix, solve_now=True)

    def         __bool__(self):return self.matrix != blank_sol(self.N)

    @property
    def         passkey(self):
      return    abs(sum([hash(a)*int(self[a])for a in rij(self.N)]))

    def         __hash__(self):
      return    self.passkey

    @property
    def matrix( self):
      return[[  int(this)for this in that]for that in self.solve]

    def save(   self):
      if self.  solved or self.done=={*self.R}:
        raise   Solved

      s = self. matrix
      _f = [    int(self[i,j])for i,j in rij(self.N)]

      for i in  self.r2:
        if      self.get(i)not in permutations(self.N):
          raise SolutionError('Contradiction')
        if[*[*  zip(*[self[j]for j in self.r2])][i]]not in permutations(self.N):
          raise SolutionError('Contradiction')

      if not    hasattr(self, 'rollback'):
        self.   rollback = s

    def         update(self, matrix):
      for i, j  in rij(self.N):
        if n:=  matrix[j][i]:
          self[ i,j] + n
        else:
          self. reduce_cell(self, i, j)

    def run(    self):
      if self.  solved:raise Solved("Nothing to run.")

      while not self.reduce():...

      try:self. check_solved()
      except    Solved as e:
        if not  self.level:raise
        else:   raise UberSolved(self.matrix)
      except    SolutionError as e:
        if not  self.level:print(e)
        self.   save()
      else:
        try:    self.bugger_it()
        except  UberSolved as m:
          if    self.level:raise
          else: self.__init__(m.matrix, solve_now=True)or self.check_solved()

    def         bugger_it(self):
       for i,j   in rij(self.N):
          if not  self[i,j]:
             for k in  self[i,j]:
                m = self.matrix
                if  self.solved:raise UberSolved(m)
                m[  j][i] = k

                try:
                  if puzzle(
    m,
    solve_now=  True,
    level=      self.level+1
                  ).check_solvable():  raise UberSolved(m)
                except  Solved:        raise UberSolved(m)
                except  SolutionError: continue
                except  Exception as e:print(e.__class__.__name__+':', e)

    def         check_solved(self):
      if self.  solved or self.done=={*self.R}:
        raise   Solved
      else:     not_solved = 0

      _f = [    int(self[i,j])for i,j in rij(self.N)]

      for i in  self.r2:
        if      self.get(i)not in permutations(self.N):
          raise SolutionError('Contradiction')
        if[*[*  zip(*[self[j]for j in self.r2])][i]]not in permutations(self.N):
          raise SolutionError('Contradiction')

      for a in  rij(self.N):
                not_solved += not self[a]
      if        not_solved:return False
      else:     raise Solved

    def view(   self):
      m = self. matrix
      N,NN =    self.N, self.NN

      if not    self.level:
        print(  'Puzzle no.',hash(self))

      for l in  range(NN)[::N]:
        print(  pad(['-'*(
          1+(1+ len(str(N**2)))*N
        )]*N,'+'  ))
        print(  '\n'.join(
          [pad  (
            [   pad([
                f"{str(m[k][i+N*j]or' '): <{len(str(NN))}s}"for i in range(N)
            ],  ' '
            )   for j in range(N)],'|'
          )for  k in range(l,l+N)]
        ))
      print(    pad(['-'*(1+(1+ len(str(N**2)))*N)]*N,'+'))

    def         __invert__(self):self.view()

    def         __repr__(self):
      return'[' +',\n '.join([str(e)for  e in self.matrix])+']'

    @property
    def raw(    self):
      return'[' +',\n '.join([str(e)for e in self.solve])+']'

    def         reduce_cell(self, *l):
      a:list =  self.aligned(*l)
      c:cell =  self[l]
      stuck =   1

      for e in  a:
        if e    and  e < c:
          c ^=  e
          stuck = 0
      return    stuck

    def reduce( self):
      r = [1]*  3
      result =  1
      N = self. N

      while not all([self.reduce_cell(i,j)for i,j in rij(N)]):
                result = 0

      for line, row in zip(self, self.transpose()):
        r[0]*=  self.eliminate(line)
        r[1]*=  self.eliminate(row)
      for k,l   in itertools.product(self.r2[::N],repeat=2):
        r[2]*=  self.eliminate(celln(self,k,l,N))
      return    result*all(r)

    def         reduce_pair(self, c, d, n, m=None):
      if c or   d:return
      if m is   None:m=n
      if n not  in self.R and m not in self.R:
        raise   ValueError(f'Not in range 1-{self.NN}')

      c.tie(d,  n).tie(d, m)
      [self[    f]-n-m for f in{*
                aligned(*c.coords,self.N)
      }&{*      aligned(*d.coords,self.N)
      }]

    def         eliminate(self, a):
      stuck =   1
      [c-int(   e)for c,e in itertools.product(a,repeat=2)if e and not c and int(e)in c]
      h = {}

      for s in  a:
        self.   reduce_cell(*s.coords)
        for x   in s:
          h.    setdefault(x, []).append(s)
      e = [(n,  x)for n,x in h.items()if len(x)==2]

      for n,x   in e:
        c,d =   x
        if not  c and not d:
          if n  not in c.tied:
                self.reduce_pair(c, d, n)
                stuck *= 0
      r =       flatten(a)

      for n in  self.R:
        if r.   count(n)==1:
          _=[   c+n for c in a if n in c]
      return    stuck

    def __eq__( self, other):
      
      return    hash(self)==hash(other)

if __name__ ==  '__main__':
  data = {
(3,0):8, (3,1): 2, (4,1):7, (6,2):6,
(7,2):9, (8,0): 4, (0,4):7, (2,5):2,
(5,3):1, (5,5): 3, (7,3):7, (7,4):5,
(8,3):9, (8,5): 1, (0,6):8, (0,7):5,
(0,8):2, (1,6): 9, (1,7):4, (1,8):6,
(2,6):7, (2,7): 1, (2,8):3, (3,6):5,
(4,7):2, (6,8): 4} ;p = puzzle(
  solve_now =   True,
  coords =      data)
  assert p.     matrix==[
[1, 2, 5, 8, 6, 9, 7, 3, 4],
[9, 3, 6, 2, 7, 4, 5, 1, 8],
[4, 7, 8, 1, 3, 5, 6, 9, 2],
[3, 8, 4, 6, 5, 1, 2, 7, 9],
[7, 1, 9, 4, 8, 2, 3, 5, 6],
[6, 5, 2, 7, 9, 3, 8, 4, 1],
[8, 9, 7, 5, 4, 6, 1, 2, 3],
[5, 4, 1, 3, 2, 8, 9, 6, 7],
[2, 6, 3, 9, 1, 7, 4, 8, 5]
    ]; q =      puzzle([
[8,0,0,0,0,0,0, 0,0],
[0,0,3,6,0,0,0, 0,0],
[0,7,0,0,9,0,2, 0,0],
[0,5,0,0,0,7,0, 0,0],
[0,0,0,0,4,5,7, 0,0],
[0,0,0,1,0,0,0, 3,0],
[0,0,1,0,0,0,0, 6,8],
[0,0,8,5,0,0,0, 1,0],
[0,9,0,0,0,0,4, 0,0]],
                solve_now = True)
  def           make_25x25():
      prev =    globals().copy()
      for I in  range(26):globals()[chr(I+97)]=I+1
      M = [
[0,0,0,0,c,l,0, 0,0,o,0,0,0,0,0,g,0,u,f,0,k,0,y,p,0],
[0,0,e,0,0,0,0, w,u,p,d,q,0,0,0,j,m,0,0,o,h,v,i,t,0],
[w,p,0,l,0,e,0, m,0,x,i,0,0,0,0,0,0,0,b,r,0,0,0,0,q],
[u,0,g,0,0,j,r, 0,0,0,0,x,b,t,n,k,e,0,0,v,0,0,0,0,0],
[a,0,j,0,0,v,k, 0,0,t,0,m,o,0,0,0,0,0,0,q,u,r,c,0,x],

[t,0,s,f,r,0,a, i,0,y,c,b,0,m,0,q,o,0,0,j,0,0,0,0,0],
[0,0,c,0,0,n,0, 0,o,0,j,0,0,0,d,0,r,0,0,p,0,0,x,l,0],
[j,b,k,0,0,0,0, 0,h,0,0,u,t,g,0,0,0,0,s,0,f,m,0,o,0],
[0,0,0,0,0,m,0, f,b,0,0,r,0,p,0,0,0,0,0,0,0,n,0,0,t],
[0,i,l,o,0,0,0, k,0,0,s,v,q,w,0,0,0,x,0,0,0,h,0,0,0],

[0,c,0,0,0,h,l, d,0,j,x,g,s,0,0,a,n,t,0,0,m,u,0,r,0],
[k,0,w,0,0,0,m, y,0,q,0,a,0,0,t,0,j,e,c,g,0,i,o,0,0],
[0,j,0,0,t,0,i, e,k,0,u,0,0,b,0,w,0,0,r,0,0,x,0,y,0],
[e,m,0,0,0,0,0, r,g,0,0,h,0,0,0,0,0,d,0,0,0,f,l,0,v],
[n,a,0,0,v,0,0, o,x,b,e,p,k,r,f,y,0,0,0,0,s,0,0,0,0],

[o,u,0,0,l,0,g, a,0,0,0,n,m,x,0,0,0,j,p,y,0,0,0,0,0],
[0,r,0,e,0,i,0, v,0,0,h,t,0,0,0,0,0,0,l,s,0,0,a,n,0],
[0,x,n,0,0,w,0, s,0,m,0,0,0,0,0,o,q,0,0,0,0,p,u,v,0],
[0,0,m,v,h,0,0, 0,0,0,k,0,0,0,p,0,0,0,0,0,l,b,s,0,d],
[y,s,d,0,0,o,0, 0,p,e,0,0,0,0,l,m,0,0,h,i,0,k,g,0,0],

[0,0,0,i,0,s,0, g,0,0,0,0,0,0,0,t,0,y,j,0,x,o,0,b,f],
[l,k,0,0,n,d,c, 0,f,0,0,0,e,0,w,0,0,0,x,0,t,0,0,0,0],
[0,0,t,0,x,0,0, 0,a,0,b,0,0,0,u,0,0,o,0,0,q,w,0,g,r],
[0,0,b,0,p,0,0, 0,0,0,0,0,0,0,0,v,f,a,n,h,0,l,0,0,0],
[g,0,r,m,0,q,0, 0,0,0,0,0,0,0,0,s,0,l,w,0,d,a,0,0,h]
]
      try:raise UberSolved(M)
      except    UberSolved as J:puzzle.view(J)
      globals   ().update(prev)
      P25 =     puzzle(M)
      return P25
  P = make_25x25()
