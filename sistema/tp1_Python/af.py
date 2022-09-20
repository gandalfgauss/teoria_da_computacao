#biblioteca sys para leitura de argumentos via linha de comando
import sys


def lerArquivo(nomeDoArquivo):
    """ funcao que le o arquivo e retorna uma lista onde cada posicao
        da lista possui uma linha do arquivo"""
    conteudoDoArquivo = ""
    with open(nomeDoArquivo) as arquivo:
        conteudoDoArquivo = arquivo.readlines()

    return conteudoDoArquivo


def definirEstadosIniciaisEFinais(linha):
    "dada a primeira linha do arquvio separa os estados iniciais e finais"
    estadosIniciais = []
    estadosFinais = []

    #separa os estados por ponto e virgula
    #a posicao 0 terah uma string contendo os estados iniciais separados por espaco
    #a posicao 1 terah uma string contendo os estados finais separados por espaco
    estados = linha.split(';')

    for estadoIncial in estados[0].split():
        estadosIniciais.append(estadoIncial)

    for estadoFinal in estados[1].split():
        estadosFinais.append(estadoFinal)


    return estadosIniciais, estadosFinais


def construirFuncaoDeTransicaoETestes(conteudoDoArquivo):
    """ recebe a segunda linha em diante do arquivo
        e constroi a funcao de transicao do automato
        e a retorna e retorna uma lista de testes que serao executados"""

    #a funcao de transicao eh um dicionario
    # as chaves do dicionario sao os estados
    #os valores do dicionario sao uma lista
    #cada posicao da lista possui uma lista de duas posicoes
    #a primeira posicao possui um simbolo de processamento
    #a segunda posicao o estado resultante
    funcaoDeTransicao = dict()
    palavraASeremVerificadas = []

    for transicao in conteudoDoArquivo:
        #se tem test na linha entao nao eh transicao, eh um teste
        if "test" in transicao:
            # desta maneira eh estraida somente a palavra a ser testada
            palavraASeremVerificadas.append(transicao.split()[1])

        else:
            #caso contrario eh transicao

            #se estado ja existe no dicionario
            if transicao.split()[0] in funcaoDeTransicao.keys():
                #eh so adicionar na lista de transicao do estado uma nova lista
                #essa nova lista contem o simbolo de entrada e o estado resultante
                funcaoDeTransicao[transicao.split()[0]].append([transicao.split()[1], transicao.split()[2]])
            else:
                #caso nao exista o estado no dicionario eh criado uma lista
                #e dentro dessa lista eh adicionado a transicao
                funcaoDeTransicao[transicao.split()[0]] = []
                funcaoDeTransicao[transicao.split()[0]].append([transicao.split()[1], transicao.split()[2]])

    return funcaoDeTransicao, palavraASeremVerificadas


def transitar(estadosAtivos, estadoATransitar, funcaoDeTransicao, simbolo, estadosResultantes):
    """ essa funcao recebe um estado que deve processar um simbolo 'estadoATransitar'
        recebe tambem os estados ativos, a funcao de transicao, o simbolo a ser processado,
        e os estados que serao resultantes da transicao, que eh parecido com os estados ativos
        , essa funcao realiza a transicao sobre um simbolo a partir de um estado
        e adiciona os estados resultante como proximos estados a serem transitados"""

    #recebe as transicoes do estado a ser transitado, se ele nao tiver transicoes retorna uma lista vazia
    transicoesDoEstado = funcaoDeTransicao.get(estadoATransitar, [])

    for transicao in transicoesDoEstado:
        #se o simbolo a ser processado for igual ao simbolo do estado e o estado resultante ja nao estiver ativo
        #entao eh adicionado como estado ativo na proxima iteracao
        if transicao[0] == simbolo:
            estadosResultantes.append(transicao[1])
            if transicao[1] not in estadosAtivos:
                estadosAtivos.append(transicao[1])


def palavrasAlcancaveiComLambda(estadosAtivos, funcaoDeTransicao):
    """a partir de um conjunto de estados ativos, essa funcao realiza as transicoes lambdas a partir deles"""
    mudou = True
    while mudou:
        mudou = False
        for estadoAtivo in estadosAtivos:
            for transicao in funcaoDeTransicao.get(estadoAtivo, []):
                if (transicao[0] == "lambda") and (transicao[1] not in estadosAtivos):
                        #caso tenha encontrado um transicao lambda
                        # o estado resultante deve ser adicionado a lista de estados ativos
                        #e o loop deve repetir mais uma vez em busca de novas transicoes lambdas
                        estadosAtivos.append(transicao[1])
                        mudou = True



def perteceALinguagem(palavra, estadosAtivos, funcaoDeTransicao, estadosFinais):
    """funcao que recebe uma palavra, um conjunto de estados ativos, um funcao de transicao
        e um conjunto de estados finais e imprime na tela se a palavra pertence a Linguagem representada
        pelo automato ou nao, caso pertenca deve imprimir o conjunto de estados finais ativos"""

    print("Iniciando o processamento de", palavra)
    print("Configuracao inicial: [", end="")
    for estadoAtivo in estadosAtivos:
        print(estadoAtivo," ", sep="", end="")

    print(",", palavra, "]", sep="")

    simbolosProcessados = 0

    tamanhoDaPalavra = len(palavra)

    #se a palavra for lambda o tamanho dela eh 0
    if palavra == "lambda":
        tamanhoDaPalavra = 0

    # enquanto os simbolos Processados forem menor que a palavra
    # e ainda tiver estados ativos
    # o loop deve se repetir
    while simbolosProcessados < tamanhoDaPalavra and len(estadosAtivos) > 0:
        #ativa os estados que tem transicao lambda
        palavrasAlcancaveiComLambda(estadosAtivos, funcaoDeTransicao)

        #gera uma copia dos estados ativos e o conjunto dos estados ativos eh zerado
        #esse conjunto sera o resultado das transicoes da copia dos estados ativos
        estadosAtivosAux = estadosAtivos.copy()
        estadosAtivos.clear()

        #para cada estado ativo deve ser realizada a transicao
        for estadoAtivo in estadosAtivosAux:
            #inicialmente nao resultou em nenhum estado pois nao transitou
            estadosResultantes = []

            print("Executando a transicao ", estadoAtivo , "-", palavra[simbolosProcessados], "-> ", end="")

            #realiza a transicao
            transitar(estadosAtivos, estadoAtivo, funcaoDeTransicao, palavra[simbolosProcessados], estadosResultantes)

            #imprime o resultado da transicao
            for estadoResultante in estadosResultantes:
                print(estadoResultante, "", end="")

            print("resulta em [ ", end="")
            for estadoResultante in estadosResultantes:
                print(estadoResultante, "", end="")


            #se ja esta no fim da palavra deve imprimir lambda ao inves de vazio
            if simbolosProcessados == tamanhoDaPalavra -1:
                print(",", "lambda]")

            else:
                #caso contrario imprime os simbolos restante a serem processados
                print(",", palavra[simbolosProcessados + 1:], "]")

        #aumenta em um os simbolos processados
        simbolosProcessados +=1

    #apos terminar a execucao das transicoes eh necessario realizar a transicao lambda dos estados resultantes
    palavrasAlcancaveiComLambda(estadosAtivos, funcaoDeTransicao)

    #verifica se pelo menos um dos estados ativos eh final
    if len(set(estadosFinais).intersection(set(estadosAtivos))) > 0:
        #se for imprime o conjunto de estados finais ativos
        print("Conjunto de Estados finais ativos: ", end="")
        for estado in set(estadosFinais).intersection(set(estadosAtivos)):
            print(estado, "", end="")
        print("\nA palavra", palavra, "eh aceita pelo AF")

    else:
        #caso nao tenha pelo menos um estado final ativo, a palavra nao eh aceita pela linguagem
        print("A palavra", palavra, "nao eh aceita pelo AF")

    print()


if __name__ =="__main__":

    #leio o arquivo e armazeno na variavel conteudo
    # o nome do arquivo eh passado como parametro na execucao
    conteudoDoArquivo = lerArquivo(sys.argv[1])

    #passar a primeira linha do arquivo que irá definir os estados iniciais e finais
    estadosIniciais, estadosFinais = definirEstadosIniciaisEFinais(conteudoDoArquivo[0])

    #inicialmente os estados ativos sao os estados iniciais
    estadosAtivos = estadosIniciais.copy()

    #definir transicoes e valores a testar
    #passar como parametro so da segunda linha a diante do arquivo
    funcaoDeTransicao, palavraASeremVerificadas = construirFuncaoDeTransicaoETestes(conteudoDoArquivo[1:])

    #para cada palavra a ser verifica eh verificada se ela pertence a linguagem
    for palavra in palavraASeremVerificadas:
        perteceALinguagem(palavra, estadosAtivos.copy(), funcaoDeTransicao, estadosFinais)

