# toy python project

sque = [1, 3, 5, 6, 8, 10]
sq = [1, 3, 5, 6, 8, 10, 11, 15, 17]

def mul(p,q) : return p*q;

def calcTween(a) :
    if(len(a) % 2 != 0) :
        print("-- It is not even number length list --", a)

    length = len(a) // 2 # len(2) / 2 => The result is float type
    for i in range(length) :
        j = (i*2);
        print(" -- calc tween -- ", a[j], a[j+1], "result = ", mul(a[j], a[j+1]))
  
#for i in range(3) :
#    j = (i*2);
#    print(sque[j], sque[j+1])
#    print(mul(sque[j], sque[j+1]))

calcTween(sque)
calcTween(sq)



