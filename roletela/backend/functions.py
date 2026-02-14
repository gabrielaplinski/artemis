import json
   
def LerLista():
    try:
        arquivo = open("./roletela/assets/filmes.json", "r")
    except:
        arquivo = open("./roletela/assets/filmes.json", "w")
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
        "id": len(dados) + 1,
        "titulo": nome,
        "plataforma": canal
    })
    arquivo = open("./roletela/assets/filmes.json", "w")
    json.dump(dados, arquivo)
    arquivo.close()
    
def CadastrarFilme():
    while True:
        nome = input("Digite o nome do filme: ").capitalize()
        canal = input("Digite a plataforma do filme: ").capitalize()
        AdicionarAoJson(nome, canal)
        continuar = input("Deseja cadastrar outro filme? (s/n): ")
        if continuar.lower() == "s":
            continue
        elif continuar.lower() == "n":
            break
        else:
            print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")

def ListarFilmes():
    dados = LerLista()
    for filme in dados:
        print(f'{filme["id"]} - {filme["titulo"]} : {filme["plataforma"]}')

def Sorteio():
    import random
    dados = LerLista()
    filme_sorteado = random.choice(dados)
    separator = '-' * 30
    print(separator)
    print(f'Filme sorteado: {filme_sorteado["titulo"]} - Plataforma: {filme_sorteado["plataforma"]}')
    print(separator)
    
CadastrarFilme()
ListarFilmes()
Sorteio()