import ast

agenda = []
alterada = False
tipos_de_telefone = ["celular ", "fixo ", "residência ", "trabalho ", "fax "]
#pergunta = input(f"Tipo de telefone: [{''.join(tipos_de_telefone)}]")


def pede_nome(nome="vazio"):
    pergunta = input("Nome: ")
    if pergunta == "":
        return nome
    return pergunta


def pede_telefone(telefone="vazio"):
    pergunta = input("Telefone: ")
    if pergunta == "":
        return telefone
    return pergunta


def pede_tipo_de_telefone(tipo="vazio"):
    while True:
        pergunta = input(
            f"Tipo de telefone: [{''.join(tipos_de_telefone)}]").lower()

        if pergunta == "":
            return tipo
        for t in tipos_de_telefone:
            if t.startswith(pergunta):
                return pergunta
        else:
            print("Telefone inválido!")


def pede_email(email="vazio"):
    pergunta = input("Email: ")
    if pergunta == "":
        return email
    return pergunta


def pede_aniversario(aniversario="vazio"):
    pergunta = input("Data de aniversario: ")
    if pergunta == "":
        return aniversario
    return pergunta


def mostrar_dados(nome, telefone, email, aniversario):
    print(f"Nome: {nome}")
    print("Telefones:")
    for e in telefone:
        print(f"Telefone: {e[0]}  |Tipo: {e[1]}")
    print(f"Email: {email}")
    print(f"Aniversário: {aniversario}")
    print("-"*15)


def pede_nome_arquivo():
    return input("Nome do arquivo: ")


def confirmacao(operacao):
    while True:
        resposta = input(f"confirma {operacao}? (s/n) ").lower()
        if resposta in "sn":
            return resposta
        else:
            print("Digite ou s ou n")


def pesquisa(nome):
    mnome = nome.lower()
    for p, e in enumerate(agenda):
        if e[0].lower() == mnome:
            return p
    return None


def novo():
    global agenda, alterada
    nome = pede_nome()
    print(nome)
    existe_na_agenda = verificar_existencia_nome(nome)
    if existe_na_agenda:
        print("O nome já existe na agenda")
    else:
        telefones = []
        while True:
            telefone = pede_telefone()
            tipo = pede_tipo_de_telefone()
            telefones.append([telefone, tipo])
            if confirmacao("adicionar mais um número") == "n":
                break
        email = pede_email()
        aniversario = pede_aniversario()
        agenda.append([nome, telefones, email, aniversario])
        alterada = True


def verificar_existencia_nome(nome):
    global agenda
    for e in agenda:
        if nome in e:
            return True
    return False


def apaga():
    global agenda, alterada
    nome = pede_nome()
    p = pesquisa(nome)
    if p is not None:
        confirmação = confirmacao("apagar")

        if confirmação == "s":
            del agenda[p]
            print("Excluído com sucesso")
            alterada = True
        else:
            print("Não excluído")

    else:
        print("Nome não encontrado.")


def altera():
    global agenda, alterada
    p = pesquisa(pede_nome())
    if p is not None:
        nome = agenda[p][0]
        telefones = agenda[p][1]
        email = agenda[p][2]
        aniversario = agenda[p][3]
        print("Encontrado:")
        mostrar_dados(nome, telefones, email, aniversario)
        nome = pede_nome(nome)
        print(agenda[p])
        print(telefones)
        print(telefones[0])
        for index, telefone in enumerate(telefones):
            telefone_novo = pede_telefone(telefone[0])
            tipo = pede_tipo_de_telefone(telefone[1])
            telefones[index] = [telefone_novo,tipo]
        email = pede_email()
        aniversario = pede_aniversario()
        confirmação = confirmacao("alteração")
        if confirmação == "s":
            agenda[p] = [nome, telefones, email, aniversario]
            grava()
            print("Alteração realizada!")
            alterada = True
        else:
            print("alteração não realizada")
    else:
        print("Nome não encontrado.")


def lista():
    print(agenda)
    print("\nAgenda\n\n-----------")
    for posição, e in enumerate(agenda):
        print(f"Posição ocupada {posição+1}º")
        e[0] = e[0].replace("$", "#")
        #e[1] = e[1].replace("$", "#")
        e[2] = e[2].replace("$", "#")
        e[3] = e[3].replace("$", "#")
        mostrar_dados(e[0], e[1], e[2], e[3])
    print("----------\n")


def lê():
    global agenda, alterada
    nome_arquivo = pede_nome_arquivo()
    while True:
        if alterada == True:
            resposta = input(
                "As alterações ainda não foram salvas, deseja continuar? (s/n)")
            if resposta.lower() == "s":
                break
            elif resposta.lower() == "n":
                return None
            else:
                print("Digite ou s ou n")
        else:
            break
    leu = ler_arquivo(nome_arquivo)
    if leu:
        gravar_ultimo_arquivo_lido(nome_arquivo)


def ler_arquivo(nome):
    global agenda
    try:
        with open(nome, "r", encoding="utf-8") as arquivo:
            agenda = []
            for l in arquivo.readlines():
                nome_pessoa, telefones, email, aniversario = l.strip().split("#")
                telefones_lista = ast.literal_eval(telefones)
                
                agenda.append([nome_pessoa, telefones_lista, email, aniversario])
        return True
    except Exception as e:
        print(f"Arquivo não encontrado. ERRO: {e}")
        return False


def grava():
    global alterada
    nome_arquivo = pede_nome_arquivo()
    gravou = gravar_em_arquivo(nome_arquivo)
    if gravou:
        gravar_ultimo_arquivo_lido(nome_arquivo)
    alterada = False


def gravar_em_arquivo(nome):
    global agenda
    try:
        with open(nome, "r+", encoding="utf-8") as arquivo:
            for e in agenda:
                e[0] = e[0].replace("#", "$")
                #e[1] = e[1].replace("#", "$")
                e[2] = e[2].replace("#", "$")
                e[3] = e[3].replace("#", "$")
                arquivo.write(f"{e[0]}#{e[1]}#{e[2]}#{e[3]}\n")
        return True
    except Exception as e:
        print(f"Arquivo não encontrado. ERRO: {e}")
        return False


def gravar_ultimo_arquivo_lido(nome):
    with open("ultima_agenda.txt", "w") as ultima_agenda:
        ultima_agenda.write(nome)


def ler_ultimo_arquivo_lido():
    with open("ultima_agenda.txt", "r") as ultima_agenda:
        for e in ultima_agenda.readlines():
            print(f"Última agenda lida: {e}")
            return e


def ordenar_nomes():
    global agenda
    agenda = sorted(agenda, key=lambda contato: contato[0].lower())
    grava()


def valida_faixa_inteiro(pergunta, inicio, fim):
    while True:
        try:
            valor = int(input(pergunta))
            if inicio <= valor <= fim:
                return valor
        except ValueError:
            print(f"Valor inválido, favor digitar entre {inicio} e {fim}")


def menu():
    print(
        f"""
    Tamanho da agenda = {len(agenda)}
    1 - Novo 
    2 - Altera
    3 - Apaga
    4 - Lista
    5 - Grava
    6 - Lê
    7 - Ordenar por nome


    0 - Sai
        """
    )
    return valida_faixa_inteiro("Escolha uma opção: ", 0, 7)


ultimo_arquivo_lido = ler_ultimo_arquivo_lido()
ler_arquivo(ultimo_arquivo_lido)

while True:
    opção = menu()
    if opção == 0:
        break
    elif opção == 1:
        novo()
    elif opção == 2:
        altera()
    elif opção == 3:
        apaga()
    elif opção == 4:
        lista()
    elif opção == 5:
        grava()
    elif opção == 6:
        lê()
    elif opção == 7:
        ordenar_nomes()
