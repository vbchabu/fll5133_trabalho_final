#as listas POS e DET foram obtidas a partir de uma varredura dos dados
#obtidos das amostras de texto apos passarem por processo_nlp.py
POS = [ 'PUNCT', 'AUX', 'X', 'ADV', 'PART', 'CCONJ', 'NOUN', 'SCONJ', 'VERB',
        'ADP', 'PROPN', 'PRON', 'NUM', 'DET', 'ADJ' ]

DET = [ 'advmod:emph', 'obl:arg', 'aux', 'flat', 'conj:expl', 'nsubj', 'root',
        'advcl', 'mark', 'det', 'advcl:pred', 'csubj', 'xcomp', 'obl', 'nmod',
        'advcl:cmpr', 'cc', 'nsubj:pass', 'discourse', 'csubj:pass', 'acl',
        'vocative', 'expl:pass', 'amod', 'nummod', 'conj', 'appos', 'case',
        'xcomp:pred', 'aux:pass', 'compound', 'advmod:neg', 'parataxis:rep',
        'cop', 'obj', 'ccomp', 'parataxis', 'fixed', 'acl:relcl', 'advmod',
        'orphan', 'punct' ]

tags = { 'POS':POS, 'DET':DET }
