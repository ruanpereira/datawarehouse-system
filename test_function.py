class Fabrica:
    def __init__(self):
        self.function_caps = None
    
    def set_function(self, func):
        self.function_caps = func

    def usar_funcao_em_outra_parte(self, *args, **kwargs):
        if self.function_caps:
            return self.function_caps(*args, **kwargs)
        else:
            print("Nenhuma função foi definida!")
            return None

def local():
    print("Executando função local")
    return "Resultado Local"

def nuvem():
    print("Executando função nuvem")
    return "Resultado Nuvem"

# Cria instância da Fábrica
fabrica = Fabrica()

# Usuário escolhe a função
choice = int(input("""
0. local
1. nuvem
"""))

if choice == 0:
    fabrica.set_function(local)
elif choice == 1:
    fabrica.set_function(nuvem)
else:
    print("Opção inválida")
    exit()


resultado = fabrica.usar_funcao_em_outra_parte()
print("Retorno:", resultado)