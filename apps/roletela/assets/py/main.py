import json
   
def LerLista():
    try:
    except:
    try:
        dados = json.load(arquivo)
    except:
        print('arquivo vazio')
        dados = []
    arquivo.close()
    return dados
    
def AdicionarAoJson(nome, canal):
    dados = LerLista()
    dados.append({
        "nome": nome,
        "canal": canal
    })
    json.dump(dados, arquivo)
    arquivo.close()
    
def CadastrarFilme():
    while True:
        nome = input("Digite o nome do filme: ")
        canal = input("Digite o canal do filme: ")
        AdicionarAoJson(nome, canal)
        continuar = input("Deseja cadastrar outro filme? (s/n): ")
        if continuar.lower() == "s":
            continue
        elif continuar.lower() == "n":
            break
        else:
            print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

CadastrarFilme()