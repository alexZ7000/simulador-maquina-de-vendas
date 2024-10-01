# Definição dos símbolos, estados e transições
Sigma = ['m25', 'm50', 'm100', 'b']  # conjunto de símbolos
Q = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']  # conjunto de estados
q0 = 's0'  # estado inicial

# tabela de transição de estados
delta = {
    's0': {'m25': 's1', 'm50': 's2', 'm100': 's4', 'b': 's0'},
    's1': {'m25': 's2', 'm50': 's3', 'm100': 's5', 'b': 's1'},
    's2': {'m25': 's3', 'm50': 's4', 'm100': 's6', 'b': 's2'},
    's3': {'m25': 's4', 'm50': 's5', 'm100': 's7', 'b': 's3'},
    's4': {'m25': 's5', 'm50': 's6', 'm100': 's8', 'b': 's4'},
    's5': {'m25': 's6', 'm50': 's7', 'm100': 's8', 'b': 's5'},
    's6': {'m25': 's7', 'm50': 's8', 'm100': 's8', 'b': 's6'},
    's7': {'m25': 's8', 'm50': 's8', 'm100': 's8', 'b': 's7'},
    's8': {'m25': 's8', 'm50': 's8', 'm100': 's8', 'b': 's0'}  # aqui a máquina devolve o troco
}

# Função que calcula o troco baseado no total depositado
def calcular_troco(total):
    return total - 2.00

# Função que executa o autômato
def reconhecer(cadeia):
    estado = q0
    total_deposito = 0
    
    for simbolo in cadeia:
        try:
            # Determinar próximo estado
            proximo_estado = delta[estado][simbolo]
            
            # Atualizar o estado e o total depositado
            if simbolo == 'm25':
                total_deposito += 0.25
            elif simbolo == 'm50':
                total_deposito += 0.50
            elif simbolo == 'm100':
                total_deposito += 1.00
            
            estado = proximo_estado
            
            # Verifica se está no estado s0 (após pressionar o botão)
            if simbolo == 'b' and estado == 's0':
                if total_deposito >= 2.00:
                    troco = calcular_troco(total_deposito)
                    # Mensagem de saída com o troco
                    if troco > 0:
                        print(f"Entrada: {simbolo}, Estado atual: {estado}, Saída: r (refrigerante dispensado) + t{int(troco * 100)} (troco)")
                    else:
                        print(f"Entrada: {simbolo}, Estado atual: {estado}, Saída: r (refrigerante dispensado)")
                    estado = 's0'  # volta para o estado inicial
                else:
                    print(f"Entrada: {simbolo}, Estado atual: {estado}, Saída: n (valor insuficiente)")
                    estado = 's0'  # volta para o estado inicial
            else:
                print(f"Entrada: {simbolo}, Estado atual: {estado}, Saída: n")
                
        except KeyError:
            print(f"Entrada: {simbolo} não reconhecida no estado {estado}.")
            break

    if estado != 's0':
        print("A máquina não dispensou um refrigerante.")
    else:
        print("A máquina voltou ao estado inicial.")

# Teste da máquina de vendas
cadeia = ['m50', 'm50', 'm50', 'm25', 'm25', 'b']  # Totaliza R$2,00
reconhecer(cadeia)

cadeia_excedente = ['m50', 'm50', 'm50', 'm100','m100','m100', 'b']  # Totaliza mais de R$2,00
reconhecer(cadeia_excedente)
