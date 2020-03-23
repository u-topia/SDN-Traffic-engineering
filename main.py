class C0:
    name = 'C0'
class C1:
    num = 1
class C2(C0):
    num = 2
class C3:
    name = 'C3'
class C4(C2,C1,C3):
    pass
print(C4.name,C4.num)

