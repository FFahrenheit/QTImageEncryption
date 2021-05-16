"""
Obtiene el número fibonacci en la posición n
"""
def fibbonaci(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a+b
        return b

"""
Obtiene la posición del número fibonacci number
"""
def reverse_fibonacci(number):
        a, b = 0, 1
        counter = 0
        while number >= b:
            if number == b:
                return counter
            a, b = b, a+b
            counter += 1
        return 0 

"""
Cifrado XOR con una clave y una posición
"""

def decode_8_bit(value,key,position) -> int:
    # return value
    return decode_8_bit(value,key,position)
    if value == 0:
        return 255
    return value - 1

def code_8_bit(value,key,position) -> int:
    # return value
    # if value == 255:
    #     return 0
    # return value + 1

    position = position % len(key) 
    key = ord(key[position])            #Get ASCII code
    value = '{0:08b}'.format(value)
    key = '{0:08b}'.format(key)

    result = []
    for i in range(len(value)):
        if value[i] == key[i]:
            result += "1"
        else:
            result += "0"
    result = "".join( str(bit) for bit in result )

    return int(result,2)