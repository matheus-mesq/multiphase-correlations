import example_funcs #Pode importar o arquivo como um modulo
from example_funcs import (func_example2) #Pode também importar com esta syntax

# Estou definindo funcoes de testes. Neste caso duas funcoes

def case_test01():

    b = example_funcs.func_example1(2)

    print('Value of b is {}'.format(b))


def case_test02():

    d = func_example2(2, 8)

    print('Output is')
    print(d)




if __name__ == '__main__':
    # Aqui que efetivamente eu chamo a funcao de test
    # Se quizer testar case_test1 ou case_test2 é só comentar a execução


    case_test01()
    # case_test02()