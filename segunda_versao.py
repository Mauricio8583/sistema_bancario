import textwrap

def menu():
    menu = """\n
      ======================Menu=================
      [d]\tDepositar
      [s]\tSacar
      [e]\tExtrato
      [nc]\tNova Conta
      [lc]\tListar Contas
      [nu]\tNovo Usuario
      [q]\tSair
      """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: \tR$ {valor:.2f}\n"
        print("\n======Depósito realizado com sucesso=========")
    else:
        print("\n======Operação falhou!===========")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saque, limite_saque):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saque > limite_saque

    if excedeu_saldo:
        print("\t Operação falhou! Você não possui saldo suficiente")
    
    elif excedeu_limite:
        print("\t Operação falhou! Você não possui excedeu o limite")

    elif excedeu_saque:
        print("\t Operação falhou! Você não possui mais saques disponiveis")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: \tR$ {valor:.2f}\n"
        numero_saque += 1
        print("\t==========Saque realizado com sucesso===========")
    else:
        print("\t==========Operação falhou! Valor informado inválido============")
    
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\t===============EXTRATO=================")
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"\nSaldo:\tR$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (Somente numero):")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Ja extiste um usuario com esse cpf")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aa): ")
    endereco = input("Informe o endereco: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuario criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o cpf do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\t================Conta criada com sucesso===============")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuario não encontrado, fluxo de criação de conta encerrado")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
             Agencia: \t {conta["agencia"]}
             C/C: \t {conta["numero_conta"]}
             Titular: \t {conta["usuario"]["nome"]}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do deposito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saque=numero_saques,
                limite_saque=LIMITE_SAQUES
            )
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu":
            criar_usuario(usuarios)
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break


main()