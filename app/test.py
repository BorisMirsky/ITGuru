

mylist = ['1', '2', '3', '4', '5']

def func(x):
    flag=0
    for i in mylist:
        if x == i:
            flag=1
            print(11)
            break
        else:
            print(22)
    print(flag)


func('54')
