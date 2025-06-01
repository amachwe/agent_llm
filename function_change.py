def f(x:int)->int:
    y = x+1
    return y

def test_f()->bool:
    assert f(10) == 11
    assert f(-1) == 0
    
    return True

import random

def add_oner(x: int)->int:
    r = random.random()
    y = x + 1 + round(r)
    print(r, y)
    return y

x : dict[str,str] = {"a":"b"}
print(x)

assert add_oner(10)==11

if __name__ == "__main__":
    test_f()