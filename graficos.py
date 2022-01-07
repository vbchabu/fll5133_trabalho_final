from chi_quadrado import valores,statisticas,generos,chi
from chi_quadrado import tags_gen as tags
import matplotlib.pyplot as plt
from pandas import read_csv
from math import sqrt

def dispersao_tag_tag(tag_x,tag_y):
    plota = False
    for genero in generos:
        if (tag_x in tags[genero] or tag_x == 'len') and tag_y in tags[genero]:
            val_x = [ valor.tabela[tag_x]['mean'] for valor in valores[genero] ]
            val_y = [ valor.tabela[tag_y]['mean'] for valor in valores[genero] ]
            err_x = [ v.tabela[tag_x]['std']/sqrt(v.tabela[tag_x]['count']) for v in valores[genero] ]
            err_y = [ v.tabela[tag_y]['std']/sqrt(v.tabela[tag_y]['count']) for v in valores[genero] ]
            plt.errorbar(val_x,val_y,err_y,err_x,fmt='.',alpha=0.5,label=genero)
            plota = True
    if plota:
        #plt.title('Dispersão {} x {}'.format(tag_y,tag_x),fontsize=)
        plt.legend()
        plt.grid(axis='both',alpha=0.5,linestyle=':')
        plt.xlabel(tag_x)
        plt.ylabel(tag_y)
        plt.savefig('graficos/{}_x_{}.png'.format(tag_y,tag_x))
        #plt.show()
        plt.close()

def dispersao_no_tempo(tag):
    max_ano = 0
    for genero in generos:
        if tag in tags[genero] or tag == 'len':
            val = sorted(valores[genero],key=(lambda x : x.ano))
            val_tag = [ valor.tabela[tag]['mean'] for valor in val if valor.ano > 0 ]
            err = [ valor.tabela[tag]['std']/sqrt(valor.tabela[tag]['count']) for valor in val if valor.ano > 0 ]
            ano = [ valor.ano for valor in val if valor.ano > 0 ]
            max_ano = max(ano+[max_ano])
            plt.errorbar(ano,val_tag,err,label=genero,fmt='.',alpha=0.5)
    #plt.title('Evolução de {} no tempo'.format(tag),fontsize=15)
    plt.legend()
    plt.grid(axis='both',alpha=0.5,linestyle=':')
    plt.xlabel('ano (a.C.)')
    plt.xlim(max_ano+1,40)
    plt.ylabel(tag)
    plt.savefig('graficos/{}_no_tempo.png'.format(tag))
    #plt.show()
    plt.close()

def histograma(tag):
    for genero in generos:
        if tag in tags[genero] or tag == 'len':
            val = [ valor.tabela[tag]['mean'] for valor in valores[genero] ]
            plt.hist(val,bins=6,histtype='barstacked',rwidth=0.2,alpha=0.5,label=genero,density=True)
    plt.legend()
    plt.xlabel(tag)
    plt.savefig('graficos/histograma_{}.png'.format(tag))
    # plt.show()
    plt.close()

def histograma3(genero_chi):
    tag_select = set(tags['oratoria']).intersection(set(tags['epistola'])).intersection(set(tags['filosofia']))
    sigma = sqrt( 2/(len(tag_select)-1) )
    for genero in generos:
        val = [ chi(texto.tabela,statisticas[genero_chi],tag_select)[0] for texto in valores[genero] ]
        plt.hist(val,bins=20,histtype='barstacked',rwidth=0.2,alpha=0.5,label=genero,density=True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('$\chi^2_{redux}$, '+'$\sigma$ = {:.1f}'.format(sigma))
    plt.savefig('graficos/histograma3_{}.png'.format(genero_chi))
    plt.show()
    plt.close()

def histograma2(genero_chi,genero_teste):
    tag_select = set(tags[genero_chi]).intersection(set(tags[genero_teste]))
    sigma = sqrt( 2/(len(tag_select)-1) )
    val_teste = [ chi(texto.tabela,statisticas[genero_chi],tag_select)[0] for texto in valores[genero_teste] ]
    val_chi = [ chi(texto.tabela,statisticas[genero_chi],tag_select)[0] for texto in valores[genero_chi] ]
    plt.hist(val_teste,bins=15,histtype='barstacked',rwidth=0.2,alpha=0.5,label=genero_teste,density=True)
    plt.hist(val_chi,bins=15,histtype='barstacked',rwidth=0.2,alpha=0.5,label=genero_chi,density=True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('$\chi^2_{redux}$, '+'$\sigma$ = {:.1f}'.format(sigma))
    plt.savefig('graficos/histograma2_{}_{}.png'.format(genero_chi,genero_teste))
    #plt.show()
    plt.close()

def histograma1(genero_chi):
    tag_select = tags[genero_chi]
    sigma = sqrt( 2/(len(tag_select)-1) )
    val_chi = [ chi(texto.tabela,statisticas[genero_chi],tag_select)[0] for texto in valores[genero_chi] ]
    plt.hist(val_chi,bins=15,histtype='barstacked',rwidth=0.2,alpha=0.5,label=genero_chi,density=True)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('$\chi^2_{redux}$, '+'$\sigma$ = {:.1f}'.format(sigma))
    plt.savefig('graficos/histograma1_{}.png'.format(genero_chi))
    plt.show()
    plt.close()

#todas_as_tags = { tag for genero in generos for tag in tags[genero] }
#todas_as_tags = list(todas_as_tags)
#dispersao_no_tempo('len')
#histograma('len')
#for tag in todas_as_tags:
#    histograma(tag)
#     dispersao_tag_tag('len',tag)
#     dispersao_no_tempo(tag)
#     for outra in todas_as_tags:
#         if todas_as_tags.index(outra) > todas_as_tags.index(tag):
#             dispersao_tag_tag(tag,outra)

for genero_chi in generos:
    histograma1(genero_chi)
    histograma3(genero_chi)
    for genero_teste in generos:
        if genero_teste != genero_chi:
            histograma2(genero_chi,genero_teste)
