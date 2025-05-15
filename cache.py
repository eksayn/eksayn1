from collections import OrderedDict
from time import time,sleep
def smart_cache(lru_cache_size,lifetime,watch):
    def decorator(func):
        d=OrderedDict()
        last_watch_results = [w() for w in watch]
        def wrapper(*args,**kwargs):
            current_watch_results = [w() for w in watch]
            if current_watch_results != last_watch_results:
                last_watch_results[:] = current_watch_results
                d.clear()
            cur_time=time()
            res=func(*args,**kwargs)
            key=tuple(args)+tuple(kwargs.values())
            if key not in d:
                d[key]=[res,cur_time]
            values_to_del=[]
            for i in d:
                if cur_time-d[i][1]>lifetime:
                    values_to_del.append(i)
            for i in values_to_del:
                d.pop(i)
            while len(d)>lru_cache_size:
                d.popitem(False)
           
            print(d.items())
        return wrapper
    return decorator    
config1=1
config2=2
def watch1():
    return config1

def watch2():
    return config2
@smart_cache(2,2,list((watch1,watch2)))
def f(a,b):
    return a+b
for i in range(10):
    f(i,i+1)
f(6,7)
config2=3
f(1,2)
sleep(3)
f(7,8)
