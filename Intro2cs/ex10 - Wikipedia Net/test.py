
a=[]
print(len(a))

b = 'dvfds'
c= 'sdfsdf'
print(b==c)

d = {1:'d',2:''}
print(len(d))

a = ['aab', 'aba','bac']
print(a.sort(reverse=True))
import operator
t = {'a':1,'b':2}
print(max(t.items(), key=operator.itemgetter(1))[0])