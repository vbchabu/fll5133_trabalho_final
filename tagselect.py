###################################################################
## ESTE SCRIPT SERVE APENAS PARA RETORNAR AS TUPLAS EM dic_dados ##
###################################################################

from pandas import read_csv
from tagsbank import tags
from pathlib import Path
from collections import namedtuple,Counter
T = namedtuple('Tupla',['path','ano','tabela'])
G = namedtuple('Genus',['arquivos','tags'])
N = namedtuple('Nome',['arquivo','ano'])

limiar_tab = 0.3                    #max ratio permitida em metade ou mais da tabela
limiar_tag = 0.3                    #max ratio permitida para tag em tabela passada pelo teste anterior
limiar_cor_tab = 0.5                #max corr permitida em metade ou mais de tabela passada pelo teste a frente
limiar_cor_tag = 0.5                #max correlacao permitida entre tags
inexiste = {'ratio':limiar_tag*999} #se tag nao existe em uma tabela, nao pode ser usada

generos = ['filosofia','oratoria','epistola']

def _condicao_dados(tabela):
    if len([ None for col in tabela.columns if tabela[col]['ratio'] >= limiar_tab ]) >= len(tabela.columns)/2:
        return False
    return True

def _condicao_tags(tag,dados):
    for dado in dados:
        if dado.tabela.get(tag,inexiste)['ratio'] >= limiar_tag: return False
    return True

def _condicao_tupla(tupla,dados):
    if len([ None for dado in dados if abs(dado.tabela[tupla[0]][tupla[1]]) >= limiar_cor_tag ]) >= len(dados)/2:
        return True
    return False

def _condicao_corr(tabela,matriz):
    if len([ None for tupla in matriz if (abs(tabela[tupla[0]][tupla[1]]) >= limiar_cor_tab) ]) >= len(matriz)/2:
        return False
    return True

def _arquivo(path):
    return path.name.replace('descricao-cicero-','').replace('csv','txt')

def _cond_arq(path,obras,genero):
    return obras.query('arquivo == @_arquivo(@path)').genero.iloc[0] == genero

#recebe como string 'filosofia', 'epistola' ou 'oratoria'
#seleciona dentre todos os arquivos os que correspondem ao genero da string
def banco_de_dados(genero):
    obras = read_csv('cicero.csv')
    lista = Path('dados_processados/').glob('descricao-cicero-*')
    return [ T(path,int(obras.query('arquivo == @_arquivo(@path)').ano.iloc[0]),read_csv(path,index_col=0)) for path in lista if _cond_arq(path,obras,genero) ]

def seletor(genero):
    dados = banco_de_dados(genero)

    #comecamos por olhar as variancias se estao dentro dos limiares parametrizados
    #exclui tabelas com metade ou mais das ratio acima do limiar_tab
    dados = [ dado for dado in dados if _condicao_dados(dado.tabela) ]

    #exclui tags que, nas tabelas aprovadas, possuam ratio acima do limiar_tag
    chaves = { key:None for key in tags.keys() }
    for key in chaves.keys():
        chaves[key] = [ tag for tag in tags[key] if _condicao_tags(tag,dados) ]

    #agora vamos olhar as correlacoes
    dados = [ T(dado.path,dado.ano,read_csv(str(dado.path).replace('descricao','correlacoes'),index_col=0)) for dado in dados ]
    chaves = chaves['POS']#+chaves['DET'] #neste trabalho analisaremos apenas as tags POS
    dados = [ T(dado.path,dado.ano,dado.tabela[chaves].loc[chaves]) for dado in dados ]
    #apenas queremos olhar as correlacoes entre as tags que permanecem na analise

    matriz = [ (tag1,tag2) for tag1 in chaves for tag2 in chaves ]
    matriz = [ tupla for tupla in matriz if chaves.index(tupla[0]) < chaves.index(tupla[1]) ]

    #limpa tags fortemente correlacionadas com outras tags segundo _condicao_tupla
    suspeito = Counter([ tag for tupla in matriz if _condicao_tupla(tupla,dados) for tag in tupla ]).most_common(1)
    while suspeito:
        suspeito = suspeito[0][0]
        chaves.remove(suspeito)
        matriz = [ tupla for tupla in matriz if suspeito not in set(tupla) ]
        suspeito = Counter([ tag for tupla in matriz if _condicao_tupla(tupla,dados) for tag in tupla ]).most_common(1)
    del suspeito
    dados = [ T(dado.path,dado.ano,dado.tabela[chaves].loc[chaves]) for dado in dados ]

    #exclui tabelas com mais da metade das entradas (nao repetidas) com correlacao acima do limiar_cor
    dados = [ N(dado.path,dado.ano) for dado in dados if _condicao_corr(dado.tabela,matriz) ]

    return G(dados,set(chaves))

dic_dados = { genero:seletor(genero) for genero in generos }
