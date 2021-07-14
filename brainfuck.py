"""
+ increment
- decrement
< move one cell left
> move one cell right
, pull character from input as ascii value, return 0 if no input.
. push cell value to output as character.
[ while cell != 0 loop code between this character and matching ]
] if cell = 0, exit loop, else go back to matching [
"""
chars = '+-<>.,[]'
class BrainfuckError(RuntimeError):...

def brainfuck(code,input=input):
    from collections import defaultdict as d
    from ctypes import py_object as p
    hack=lambda v:p.from_address(v)
    l=input==__builtins__.input
    if not l:input=lambda i=1:input.pop(i-1)
    a,o=d(int),''
    i=p=t=0
    gulag = [hack(id(IndexError)).value]
    hack(id(__builtins__.IndexError)).value=StopIteration
    for c in iter(lambda:code[p],None):
        def __0(i,*_):
            a[i]+=1
            a[i]%=256
            return i,*_,
        def __1(i,*_):
            a[i]-=1
            a[i]%=256
            return i,*_,
        def __2(i,o,t):
            o+=chr(a[i])
            return i,o,t
        def __3(i,*_):
            a[i]+=ord(input(1))%256
            return i,*_,
        f = [__0,__1,
             lambda i,*_:(i+1,*_),
             lambda i,*_:(i-1,*_),
             __2,__3,
             lambda i,o,t:(i,o,t+(not a[i])),
             lambda i,o,t:(i,o,t-bool(a[i])),lambda*_:_][chars.find(c)]
        if t:
            if c=='[':t+=1
            if c==']':t-=1
        else:
            i,o,t = f(i,o,t)
        p += 1 - 2*(t<0)
    hack(id(IndexError)).value = gulag.pop(0)
    return o,int(p!=len(code))

try:
    print(brainfuck(input("bf> ")))
except Exception as e:
    raise BrainfuckError(e)
