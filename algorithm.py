"""
Obtiene el número fibonacci en la posición n
"""
def fibbonaci(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a+b
        return b

"""
Get offset to random images
"""
def get_offset(key):
    offset = fibbonaci(len(key))
    module = 0

    for index , k in enumerate(key):
        module += ord(k)
        offset += index * ord(k) 

    return offset % module

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
def code_8_bit(value,key,position) -> int:

    position = position % len(key) 
    key = ord(key[position])            #Get ASCII code
    value = '{0:08b}'.format(value)
    key = '{0:08b}'.format(key)

    result = []
    for i in range(len(value)):
        if value[i] == key[i]:
            result += '1'
        else:
            result += '0'
    result = "".join( str(bit) for bit in result )

    return int(result,2)