import os
import itertools
import msvcrt

_COLOR_SEQUENCES={
    'end':0,'bold':1,'italics':2,'_underline':3,'underline':4,
    'blink':5,'_blink':6,'invert':7,
    'default':37,
    'red':31,
    'green':32,
    'gold':33,
    'blue':34,
    'turquoise':35,
    'purple':36,
    'black':30,
    'pink':91,
    'bright_green':92,
    'yellow':93,
    'sky_blue':94,
    'cyan':95,
    'magenta':96,
    'grey':90,
    'white':97
}
COLOURS={a:f'\x1b[{b}m'for a,b in _COLOR_SEQUENCES.items()}
HIGHLIGHTS={a:f'\x1b[{b+10}m'for a,b in _COLOR_SEQUENCES.items()if b>20}
COLOUR = lambda s='',color='',highlight='',end=True,invert=False:COLOURS[color or 'default']+HIGHLIGHTS[highlight or 'black']+s+COLOURS['end']*end+COLOURS['invert']*invert

@lambda c:c()
class bugger:
    __setattr__, __getattribute__, __setitem__, __getitem__ = (lambda*a:None,)*4
    __iter__ = lambda*a:iter(())

class terminal:
  save = lambda s: print(end='\x1b[s')
  get  = lambda s: print(end='\x1b[u')
  _blink = 1
  blink= lambda s:setattr(s,'_blink',not s._blink)or s._blink

  def __init__(self):
      os.system('')
      os.system('mode 100,50')# WINDOWS
      print(end=COLOUR('\x1b[A','black','default',end=False))
      self.get()

  def mode(self, i, j):
      return os.system(f'mode {i},{j}')

  reset = lambda s:print(end=COLOURS['end'])

  @staticmethod
  def log(message):
      message=str(message)
      from os import get_terminal_size as g
      return print(message+' '*-(len(message)-g()[0]+1)*('\n'not in message and'\r'not in message), end='\x1b[u')

  def pretty(self, s, n=30, c=32, f=0):
    C = f'\x1b[{f};{c}m'
    return f'{C}{str(s): <{n}s}{COLOURS["end"]}'

  def loadbar(self, iterable, f, n=62, offset=0):
    print('['+' '*n+']')
    result=[]
    for i,e in enumerate(iterable):
        p = int(i*n//len(iterable))
        print('\x1b[A[\x1b[44m'+' '*p+COLOURS['end']+' '*(n-p)+']', self.pretty(
            len(iterable)-i+offset,
            len(str(len(iterable)+offset))
        ), 'remaining')
        result += [f(e)]
    return result


class Minesweeper:
    """
    x: col; horizontal
    y: row; vertical
    0 < n < x*y-9 for obvious reasons
    """
    running = dead = False
    terminal, t, *here = terminal(),0,0,0
    clicked:[{0:False, 1:True, 2:"!",3:"?"},...]
    chars = {
        'board':('|',"---",'+'),
        'numbers':(
            ' \x1b[0;47m \x1b[30m ',
            ' \x1b[0;47;34m1\x1b[0;30;47m ',
            ' \x1b[0;47;32m2\x1b[0;30;47m ',
            ' \x1b[0;47;31m3\x1b[0;30;47m ',
            ' \x1b[0;47;35m4\x1b[0;30;47m ',
            ' \x1b[0;47;91m5\x1b[0;30;47m ',
            ' \x1b[0;47;36m6\x1b[0;30;47m ',
            ' \x1b[0;47;30m7\x1b[0;30;47m ',
            ' \x1b[0;47;90m8\x1b[0;30;47m ',
            lambda i:f' \x1b[0;30;{100+7*i}m_\x1b[0;30;47m '
        ),
        'other':lambda i,b=0:f' \x1b[0;{b*7};'+[f"{7*(not b)};30;{41+60*(not b)}m*\x1b[0;30;47m", '107;30m!\x1b[0;30;47m', "31;107m?\x1b[0;30;47m"][i%3]+' '
    }

    def _get(self, i, j):
        (x,y,n),clicked = self.xyn, self[i,j]
        nuke,number = self.bombs[j][i], self.numbers[j][i]
        if i not in range(x) and j not in range(y):raise RuntimeError('Dimensional Panic.')
        if nuke and self.dead:magic=self.chars['other'](0,self.here==(i,j))
        elif clicked<2:
             magic = self.chars['numbers'][number]if clicked else self.chars['numbers'][9](self.here==(i,j))
        else:magic = self.chars['other']  (clicked-1,self.here==(i,j))
        return magic

    def update_board(self):
        (x,y,n),a,b,c = self.xyn,*self.chars['board']
        d = self.chars['numbers'][9](0)
        e,f = f"{a}{a.join([d]*x)}{a}", f"\n{c}{c.join([b]*x)}{c}\n"
        if not self.running:
            self.title('\x1b[30;47m',n)
            self.board = f"""\n   
{c}{c.join([b]*x)}{c} 
{f.join([e]*y)} 
{c}{c.join([b]*x)}{c} \x1b[0m\x1b[u\r\n\x1b[A"""
            print('\x1b[u',end=self.board)
        else:
            flags = sum(self[a]==2 for a in self)
            self.board = f"\x1b[A\n\n{c}{c.join([b]*x)}{c}\n"
            self.board+= f.join([a+a.join([self._get(i,j)for i in range(x)])+a for j in range(y)])
            self.board+= f"\n{c}{c.join([b]*x)}{c}\x1b[u"
            self.title(self.board,max(n-flags,n*self.dead),[':)','X('][self.dead],self.t)

    def                       generate(self):
        import                   random
        *_,_n = x,y,n ,=        self.xyn
        self.bombs,            self.numbers,              self.clicked ,= (
  [[(0x00for 0in(x,y))-15for bugger.this in range(x)]for bugger.that in range(y)]
                         for bugger.it in range(3))
        while                   n:n ,= [n-1
          for r1,r0 in[(random.randint(0,x-1),random.randint(0,y-1))]
             if not self.bombs[r0][r1] for self.bombs[r0][r1]in[1]
                                  ]or[n]
        for(i,j),k,l in itertools.product(self,range(-1,2),range(-1,2)):
         for                m,n in[[i+k,j+l]]:
          if           m in range(x) and n in range(y):
           for self.numbers[j][i]in[self.numbers[j][i]+self.bombs[n][m]]:
                              bugger.it_all
        self.       terminal.log('board generated.')

    def __init__(self, x=16, y=16, n=40, c=True):
        (0 < n < x*y - 9 > x > 2 < y)or yo_mamma is fat
        self.terminal.mode(max(x*4+3,os.get_terminal_size()[0]),y*2+20)
        self.terminal.get()
        *self.xyn, _e, self.classic = x,y,n,0,c
        print()
        self.title(f"{n} bombs total",n,':)',0)
        self.terminal.get()
        self.update_board()
        try:self.start()                                                         and this is the.__init__-method
        except KeyboardInterrupt:
            self.terminal.reset()
            self.terminal.log('GAME QUIT')
            self.DIE(True)
        except Exception as e:
            self.terminal.reset()
            print('\x1b[u'+'\n'*(y*2+2))
            _e=e
        if _e==1:self.DIE(True)
        elif _e:raise _e.__class__(str(_e))

    def DIE(self, quit=False):
        self.dead = True
        self.terminal.get()
        self.update_board()
        class GameOver(RuntimeError):
            __str__=lambda s:"YOU GOT EXPLODED!"if not quit else"GAME QUIT"
        self.running = False
        raise GameOver

    def select(self, i, j):
        x,y,n = self.xyn
        if self.bombs[j][i]and all(all(p)for p in self.numbers):self.hint()
        elif not any(any(p)for p in self.clicked)and(self.numbers[j][i]or self.bombs[j][i]):
            self.terminal.log('Bad start, board regenerating. Please wait.')
            while self.numbers[j][i]or self.bombs[j][i]:self.generate()
            self.select(i, j)
        else:
            if self.bombs[j][i]:self.DIE()
            else:
                self[i,j] = 1
                self.classic or self.update_board()
            if not self.numbers[j][i]:
                _={self[m,n]==1 or self.select(m,n)for k,l in itertools.product(range(-1,2),repeat=2)for m,n in[(i+k,j+l)]if m in range(x)and n in range(y)}
                while msvcrt.kbhit(): msvcrt.getch()
            if self.check_done():
                self.title('You Win!',0,'B)',self.t)
                print(end=COLOURS['default'])
                @lambda E:(()for()in()).throw(E,'You Win!')
                class GameWon(RuntimeError):self.running=False

    def title(self, message='', bombs=0, smiley=':)', time=0):
        x,*_ = self.xyn
        bombs = f"{chr(27)}[91;40m{bombs:0>3d}{chr(27)}[30;47m"
        smiley = f'{chr(27)}[100m {smiley:s} {chr(27)}[47m'
        time = f"{chr(27)}[40;91m{str(time).zfill(3):s}{chr(27)}[30;47m"
        self.terminal.log(f'{message}\n{bombs: <{2*x+len(bombs)-5}}{smiley:s}{time: >{2*x+len(time)-4}s}')

    @property
    def sweep_mode(self):
        return not self.classic

    def right_click(self, *a):
        if self[a]==1:return
        x,y,n=self.xyn
        self[a] = {0:2,2:3,3:0,1:1}[self[a]]
        if self.sweep_mode: # experimental still...
            i,j = a
            if self.bombs[j][i]:
                self[a]=1
                self.bombs[j][i]=0
                *_,n = self.xyn = x,y,n-1
                for k,l in itertools.product(range(-1,2),repeat=2):
                    for m,n in[(i+k,j+l)]:
                        if m in range(x)and n in range(y)and self.numbers[n][m]:
                            self.numbers[n][m]-=1
                            if not self.numbers[n][m]:self.select(m,n)
            else:self.DIE()


    def check_done(self):
        for i,j in self:
            if self[i,j]in[0,2,3]and not self.bombs[j][i]:
                return False
        return True

    def move(self,
w:int = 0,     a:int = 0,
s:int = 0,     d:int = 0
    ):
        o = i, j = self.here
        x,y,_= self.xyn
        w *= not not j
        a *= not not i
        I, J = d-a, s-w
        j += J
        i += I
        tolerance:int = x+y-1
        while(not(j in range(y)and i in range(x))or self[i,j]==1)and tolerance:
            tolerance -= 1
            j += J
            i += I
            if i >= x: i:int = x-1
            elif i<0 : i = int()
            if j >= y: j:int = y-1
            elif j<0 : j = int()
            if(i==j==0 or x-1==i>0<j==y-1 or i==0<j==y-1 or j==0<i==x-1)and self[i,j]==1:#if your in a corner and you already know that spot:
                if self!=1:i,j=o#try to go back
                else:
                    for k in range(x if I else y):
                        if self[k if I else i,k if not I else j]!=1:
                            i,j = k if I else i,k if not I else j
                            break
                    if self[i,j]==1:tolerance=0
            elif self[i,j]!=1:break
        if not tolerance and not self.check_done():
            for i,j in self:
                if self[i,j] != 1: break
        self.here = i,j

    def __reduce__(self):return self.__class__, self.xyn

    def __iter__(self):
        x,y,_ = self.xyn
        return iter([*itertools.product(range(x),range(y))])

    def __getitem__(self, ij):
        i,j = ij
        return self.clicked[j][i]

    def __setitem__(self, ij, item):
        i,j = ij
        self.clicked[j][i] = item

    def __eq__(self, n):
        return n==self[self.here]

    def __ne__(self, n):
        return not self==n

    def react_select(self, *a):
        if self[a]:return
        x,y,n = self.xyn
        self.title(' '*(x*4+2),n,':O',self.t)
        import time
        time.sleep(0.25)
        self.select(*a)

    def reset(self):
        a = x,_,n,_ = *self.xyn,self.classic
        self.title(' '*(x*4+2),n,':)',self.t)
        self.__init__(*a)

    def digit_move(self, d):
        x,y,n = self.xyn
        I, J = self.here
        if self[d,J] != 1:
            self.move(**{'a'if d<I else'd':abs(I-d)})
            return
        for j in range(y):
            if self[d,J]!=1:
                self.move(**{'a'if d<I else'd':abs(I-d),'w'if j<J else's':abs(J-j)})
                break
        if self[d,j]==1 and self[I,J]==1:
            for a in self:
                if self[a]!=1:
                    self.here=a
                    break

    def hint(self):
        I, J = self.here
        a = self==1
        b = self.bombs[J][I]
        if a or(b and self==2):self.terminal.log("That spot is already known")
        elif b:
            self[self.here]=2
            self.terminal.log("Probably don't click there :/")
        else:
            self.terminal.log(str(self.numbers[J][I]))
            self.select(I, J)

    def random_move(self):
        from random import choice as c
        self.here = c([a for a in self if self[a]!=1])

    def start(self):
        self.running = True
        self.generate()
        self.update_board()
        import time
        T = time.time()//1
        while self.running:
            self.t = t = int(time.time()-T)
            char=msvcrt.getch().decode('ANSI')if msvcrt.kbhit()else'\1'
            (lambda i,j:{
char in'\t/?':lambda:self.right_click(i, j),
char in'\b\xff':self.reset,
char in' \r':lambda:self.react_select(i, j),
char in'wasdqezx':lambda:self.move(w=char in'qwe',a=char in'qaz',s=char in'zsx',d=char in'edx'),
char in'[\x1b':lambda:self.DIE(True),
char=='à':lambda:(c:=msvcrt.getch().decode('ANSI'))not in'KHMP'and(self.reset()or 1)or self.move(**{{'K':'a','H':'w','M':'d','P':'s'}[c]:1}),
char in'h;:':self.hint,
char in'rl':self.random_move,
char.isdigit():lambda:self.digit_move(int(char))
            }.get(1,lambda:0)()or self.update_board())(*self.here)
            if self.check_done():
                self.title("You Win!",0,'B)',t)
                print(end=COLOURS['default'])
                @lambda E:(()for()in()).throw(E,'You Win!')
                class GameWon(RuntimeError):self.running=False

def main():
    Minesweeper.terminal.save()
    try:Minesweeper(int(input('x> ')),int(input('y> ')),int(input('bombs> ')),input("classic>")[0]in'Yy')
    except NameError as e:
        k = e.__str__()
        from ctypes import py_object as p
        hack = lambda:p.from_address(id(e)+8)
        hack().value = type(hack().value.__name__,(hack().value,),{'__str__':lambda s:k.removeprefix('name ').removesuffix('not defined') + 'obese'}); raise ValueError(e)
    except Exception as e:
        Minesweeper.terminal.reset()
        print(e.__class__.__qualname__+':',e,'                     ')
        input('ok>')
        raise


__name__ == '__main__' and main()and...._.___._.___.morse.code_lol.__
