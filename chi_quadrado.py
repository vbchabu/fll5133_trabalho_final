from tagselect import generos,dic_dados
import matplotlib.pyplot as plt
from pandas import read_csv
import numpy as np
from collections import namedtuple
T = namedtuple('T',['ano','tabela','arquivo'])
D = namedtuple('D',['media','varmedia','varsimples'])

tags_gen = { genero:dic_dados[genero].tags for genero in generos }

valores = { genero:dic_dados[genero].arquivos for genero in generos  }
valores = { genero:[ T(arquivo.ano,read_csv(arquivo.arquivo,index_col=0)[tags_gen[genero].union({'len'})],arquivo.arquivo) for arquivo in valores[genero] ] for genero in generos }
#a informacao sobre ano sera importante no estudo da variacao das POS tags no tempo, mas nao aqui

def media(genero,tag):
    medias = np.array([ v.tabela[tag]['mean'] for v in valores[genero] ])
    variancias = np.array([ v.tabela[tag]['std']**2/v.tabela[tag]['count'] for v in valores[genero] ])
    pesos = 1/variancias
    return (medias*pesos).sum() / pesos.sum()

def var_media(genero,tag):
    variancias = np.array([ v.tabela[tag]['std']**2/v.tabela[tag]['count'] for v in valores[genero] ])
    return (1/variancias).sum()**-1

def var_simples(genero,tag):
    medias = np.array([ v.tabela[tag]['mean'] for v in valores[genero] ])
    return medias.var()*len(medias)/(len(medias)-1)
    #funcao np.var() fornece variancia populacional, precisamos da
    #variancia amostral, por isso o reescalonamento por n/(n-1)

statisticas = { genero:{ tag:D(media(genero,tag),var_media(genero,tag),var_simples(genero,tag)) for tag in tags_gen[genero] } for genero in generos }

#devolve qui-quadrado reduzido e incerteza
def chi(tabela,stats,tags):
    medias = np.array([ tabela[tag]['mean'] for tag in tags ])
    incertezas = np.array([ tabela[tag]['std']**2/tabela[tag]['count'] for tag in tags ])
    dados = np.array([ stats[tag].media for tag in tags ])
    variancias_media = np.array([ stats[tag].varmedia for tag in tags ])
    variancias_simples = np.array([ stats[tag].varsimples for tag in tags ])
    chi_quad = ( (medias - dados)**2 / (variancias_simples + variancias_media + incertezas) ).sum()
    gdl = len(tags)-1
    return chi_quad/gdl, np.sqrt(2/gdl)
