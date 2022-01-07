from collections import Counter
from pandas import DataFrame
from tagsbank import tags
from pathlib import Path

N_sentencas_a_homogeneizar = 48
#N obtido por tentativa e erro de modo a maximizar o numero de tags e de tabelas
#a serem selecionadas por tagselect

def randomizador(original,N):
    frame = original.copy()
    randomizado = DataFrame(columns=frame.columns)
    while len(frame) >= N:
        smp = frame.sample(N)
        frame.drop(smp.index,inplace=True)
        dic = { col:[ item for row in smp[col] for item in row ] for col in smp.columns }
        randomizado = randomizado.append(dic,ignore_index=True)
    return randomizado

def _media_tags(processado,randomizado,tipo):
    processado[tipo] = randomizado[tipo].apply(Counter)
    for tag in tags[tipo]:
        coluna = processado[tipo].apply(Counter.get,args=[tag,0])/processado['len']
        if not coluna.std() == 0:
            processado[tag] = coluna
    processado.drop(tipo,axis=1,inplace=True)

def process(randomizado,N):
    processado = DataFrame()
    processado['len'] = randomizado.tokens.str.len()/N
    _media_tags(processado,randomizado,'POS')
    _media_tags(processado,randomizado,'DET')
    return processado

def exec(pack):
    amostra,N = pack
    dados = process(randomizador(amostra.dados,N),N)
    tabelar(dados,amostra.autor,amostra.obra)

def tabelar(dados,autor,obra):
    dados.to_csv('dados_processados/contagens-{}-{}.csv'.format(autor,obra))
    dados.corr().to_csv('dados_processados/correlacoes-{}-{}.csv'.format(autor,obra))
    tabela = dados.describe()
    tabela.loc['ratio'] = tabela.loc['std']/tabela.loc['mean']
    tabela.loc[['mean','std','ratio','count']].to_csv('dados_processados/descricao-{}-{}.csv'.format(autor,obra))

def main():
    from amostras import from_file
    from multiprocessing import Pool,cpu_count

    N = N_sentencas_a_homogeneizar
    amostras = ( from_file(path) for path in Path('dados/').glob('cicero-*') )
    amostras = ( (amostra,N) for amostra in amostras if len(amostra) >= 2*N )
    #o empacotamento (amostra,N) e para passar varios parametros para imap_unordered

    with Pool(1) as pool:
        list(pool.imap_unordered(exec,amostras))

if __name__ == '__main__': main()
