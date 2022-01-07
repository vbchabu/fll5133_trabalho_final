from multiprocessing import Pool,cpu_count
from amostras import Amostra
from pathlib import Path

def exec(obra):
    amostra = Amostra('cicero',obra)
    amostra.to_file('dados/{}-{}.csv'.format(amostra.autor,amostra.obra))

def main():
    obras = { item.parts[-1].replace('.txt','') for item in Path('cicero/').glob('*.txt') }
    #ja_feito = { item.parts[-1].replace('cicero-','') for item in Path('dados/').glob('*') }
    #obras = obras.difference(ja_feito)
    #back up para o caso de interrupcao do processamento dos dados

    with Pool(cpu_count()-1) as pool:
        i = 0
        n = len(obras)
        print('Feito: {:3d} de {}.'.format(i,n))
        for _ in pool.imap_unordered(exec,obras):
            i += 1
            print('Feito: {:3d} de {}.'.format(i,n))
        print('Pronto.')

if __name__ == '__main__': main()
