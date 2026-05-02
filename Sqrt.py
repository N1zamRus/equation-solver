from BigFloat import (
    BigFloatm,
    get_BASE,
    get_blocks,
    get_exp10,
    get_sign,
    normalize
)




"""
def Sqrt(a)
    1. Необходимо найти x_old, тобишь начальное приближение, x_old = make_x0(a)
    2. Цикл TRUE
        Формула: x_new = (x + a/x) / 2
        if x_new >= x_old
            break
        x_old = x_new

       str_x = str(x)
    
    3. return x в виде BigFloat

        

        

def make_x0(a)
    1. Посмотрим кол-во цифр числа a
        k = кол-во блоков * кол-во цифр в блоке
    2. Попробуем предугадать кол-во цифр корня числа a, 
        это примерно t = K/2
        ЭТО ПОСЛУЖИТ СТЕПЕНЬЮ ДЛЯ НАЧАЛЬНОГО ЧИСЛА
    
    3. И тогда возьмём x0 за 10^t


"""