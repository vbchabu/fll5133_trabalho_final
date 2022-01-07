from multiprocessing import cpu_count,Pool
from collections import Counter,namedtuple
texto = namedtuple('Texto',['texto','oratoria'])
classes = namedtuple('Classes',['oratoria','filosofia'])
resultado = namedtuple('Avaliacao',['oratoria','positivo'])
from pathlib import Path
import numpy as np

from cltk.stops.lat import STOPS


from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('english')

def pre_processar(texto):
    tokens1 = word_tokenize(texto)
    tokens2 = ( token.lower() for token in tokens1 if token.isalpha() )
    return [ stemmer.stem(token) for token in tokens2 if token not in stops ]

def exec(arq):
    with open(arq,'r') as arquivo:
        spam = bool(int(arquivo.readline()))
        texto = pre_processar(arquivo.read())
    return texto,spam

def processar(lista):
    conts = Counter(( item.spam for item in lista ))
    N = classes(spams=conts[True],hams=conts[False])
    t_spam = [ token for item in lista if item.spam for token in item.texto ]
    t_ham = [ token for item in lista if not item.spam for token in item.texto ]
    freqs = classes(spams=Counter(t_spam),hams=Counter(t_ham))
    vocabulario = set(t_spam).union(set(t_ham))
    return N,freqs,vocabulario

def laplace(x,str):
    if str == 'spams':
        return (freqs.spams[x]+1)/(T.spams+V)
    if str == 'hams':
        return (freqs.hams[x]+1)/(T.hams+V)

def log_probabilidade(e_mail):
    txt = e_mail.texto
    p_spam = np.fromiter(( laplace(t,'spams') for t in txt if t in vocabulario ),dtype='float64')
    p_spam = np.log10(Probabilidade.spams) + np.log10(p_spam).sum()
    p_ham = np.fromiter(( laplace(t,'hams') for t in txt if t in vocabulario ),dtype='float64')
    p_ham = np.log10(Probabilidade.hams) + np.log10(p_ham).sum()
    return classes(spams=p_spam,hams=p_ham)

def avaliar(e_mail):
    leitura = e_mail.spam
    prob = log_probabilidade(e_mail)
    if prob.spams > prob.hams: classificacao = True
    else: classificacao = False
    return resultado(spam=leitura,positivo=classificacao)

if __name__ == '__main__':
    with Pool(cpu_count()//2) as pool:
        arq = ( arquivo for arquivo in Path('Enron/').rglob('*.txt') )
        corpus = [ email(*result) for result in pool.imap_unordered(exec,arq) ]
else:
    corpus = [ email(*exec(arq)) for arq in Path('Enron/').rglob('*.txt') ]

treinamento = slice(0,round(len(corpus)*0.8))
avaliacao = slice(treinamento.stop,None)

N,freqs,vocabulario = processar(corpus[treinamento])
Probabilidade = classes(spams=N.spams/sum(N),hams=N.hams/sum(N))
T = classes(spams=sum(freqs.spams.values()),hams=sum(freqs.hams.values()))
V = len(vocabulario)

resultados = Counter(( avaliar(e_mail) for e_mail in corpus[avaliacao] ))
fp = resultados[resultado(spam=False,positivo=True)]
vp = resultados[resultado(True,True)]
fn = resultados[resultado(True,False)]
vn = resultados[resultado(False,False)]

cobertura = vp/(vp+fn)
precisao = vp/(vp+fp)
acuracia = (vp+vn)/(vp+vn+fp+fn)
media_f = 2*(precisao*cobertura)/(precisao+cobertura)
#nessa definicao, 0 <= media_f <= 1

string = '{:10}: = {:.1f}%'
print(string.format('Cobertura',cobertura*100))
print(string.format('Precisao',precisao*100))
print(string.format('Acuracia',acuracia*100))
print(string.format('Media F',media_f*100))
