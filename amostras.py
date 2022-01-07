from re import sub
from pandas import DataFrame,read_csv
from cltk.nlp import NLP
from cltk.sentence.lat import LatinPunktSentenceTokenizer

nlp = NLP(language='lat')
sent_tokenizer = LatinPunktSentenceTokenizer().tokenize

class Amostra():

    def __init__(self,autor,obra,dados=None):
        self.autor = autor
        self.obra = obra
        if dados is None:
            dados = self.__filtrar__()
            dados = sent_tokenizer(dados.decode())
            dados = ( nlp(sent) for sent in dados )
            dados = ( (sent.tokens,sent.pos,[ sent.words[i].dependency_relation for i in range(len(sent.words)) ]) for sent in dados )
        self.dados = DataFrame(dados,columns=['tokens','POS','DET'])

    def __filtrar__(self):
        with open(self.autor+'/'+self.obra+'.txt','rb') as arquivo:
            texto = arquivo.read()
        texto = sub(b'<head>[^^]*</head>',b'',texto)              #limpa cabecalhos
        texto = sub(b'<p class=pagehead>[^<]*</p>',b'',texto)
        texto = sub(b'<div class="footer">[^^]*</div>',b'',texto) #limpa rodape
        texto = sub(b'nbsp;?',b'',texto)         #limpa parte do codigo html
        texto = sub(b'<[^>]*>',b'',texto)        #limpa as demais chaves html
        texto = sub(b'\[[ivxlc]*\]',b'',texto)   #limpa a numeracao dos passos
        texto = sub(b'[!?]', b'\.', texto)       #limpa a pontuacao, exceto \. que e necessario para tokenizar
        texto = sub(b'([A-Z])\.',b'\g<1>',texto) #resolve siglas de prenomes tirando o \.
        texto = sub(b'([A-Z][a-z])\.',b'\g<1>',texto)
        texto = texto.lower()
        texto = texto.replace(b'v',b'u')         #troca v por u
        texto = texto.replace(b'j',b'i')         #troca j por i
        texto = sub(b'[^abcdefghiklmnopqrstuxyz\. ]',b'',texto)   #limpa todo o resto
        return texto

    def __len__(self):
        return len(self.dados)

    def __repr__(self):
        return 'Amostra({},{})'.format(self.autor,self.obra)

    def to_file(self,path):
        self.dados.append({'tokens':self.autor,'POS':self.obra},ignore_index=True).to_csv(path,index=False)
        #autor e obra sao enxertados na ultima linha do frame a ser salvo

def from_file(path):
    frame = read_csv(path)
    autor,obra = frame.iloc[-1].drop('DET')
    dados = frame.iloc[:-1]
    for col in dados.columns:               #transforma a string lida do arquivo
        dados[col] = dados[col].apply(eval) #em verdadeiro dado tipo list
    return Amostra(autor,obra,dados)
