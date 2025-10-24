

mylist = ['1', '2', '3', '4', '5']

def func(x):
    flag=0
    for i in mylist:
        if x == i:
            print(1)
            break
        else:
            print(2)
            #break


func('5')
