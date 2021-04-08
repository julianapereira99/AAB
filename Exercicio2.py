# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:58:50 2021

@author: Juliana
"""

class SuffixTreeMulti:

    def __init__(self):
        self.nodes = {0: (-1, {})}  # root node
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''

    def print_tree(self):
        for k in self.nodes.keys():
            if type(self.nodes[k][0]) == int and self.nodes[k][0] < 0 or \
                    type(self.nodes[k][0]) == tuple and self.nodes[k][0][0] < 0:
                print(k, "->", self.nodes[k][1])
            else:
                print(k, ":", self.nodes[k][0])
        print(self.nodes)

    def add_node(self, origin, symbol, leafnum=-1):
        self.num += 1   #vai dando valores aos nós
        self.nodes[origin][1][symbol] = self.num   #acede ao dicionário do tuplo do nó e atribui um nucleótido ao nº do nó
        self.nodes[self.num] = (leafnum, {})    #cria o tuplo donde se guardam as próximas posições

    def add_suffix(self, p, sufnum, seq):
        pos = 0
        node = 0
        while pos < len(p):    
            if p[pos] not in self.nodes[node][1].keys():  
                if pos == len(p) - 1:
                    self.add_node(node, p[pos], (sufnum, seq))
                else:
                    self.add_node(node, p[pos])
            node = self.nodes[node][1][p[pos]]
            pos += 1    

    def suffix_tree_from_seq(self, text, text1):
        self.seq1 = text
        self.seq2 = text1
        t = text + "$"
        t1 = text1 + '#'
        for seq in [t, t1]:
            for i in range(len(seq)):
                if seq == t:
                    self.add_suffix(seq[i:], i, 0)
                else:
                    self.add_suffix(seq[i:], i, 1)

    def find_pattern(self, pattern):
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
            else:
                return None
        return self.get_leafes_below(node)

    def get_leafes_below(self, node):
        res = []
        if type(self.nodes[node][0]) == int and self.nodes[node][0] >= 0 or \
                type(self.nodes[node][0]) == tuple and self.nodes[node][0][0] >= 0:
            res.append(self.nodes[node][0])
        else:
            for k in self.nodes[node][1].keys():
                newnode = self.nodes[node][1][k]
                leafes = self.get_leafes_below(newnode)
                res.extend(leafes)
        return res

    def nodes_below(self, node):
        '''
         Método que dado o identificador (número) de um nó na árvore de sufixos, retorna a
         lista com todos os identificadores dos nós que estão abaixo de si na árvore

        '''
        res = []    #criei uma lista vazia
        res.append(node)    #adicionei o local a partir donde vai começar a contar
        if list(self.nodes[node][1].values()):  #se o node do dicionário tiver algum valor
            for m in res:   #então por cada valor dentro da lista
                #se tiver apenas 1 número como valor e esse valor for menor que 0 ou for um tuplo e o primeiro valor do tuplo for inferior a zero
                #vai estender esse valor no interior da lista res para ir buscar todos os nós existentes abaixo do node
                if type(self.nodes[node][0]) == int and self.nodes[node][0] < 0 or \
                        type(self.nodes[node][0]) == tuple and self.nodes[node][0][0] < 0:
                    res.extend(list(self.nodes[m][1].values()))
        res.remove(node)    #Retiro o node para não contar, apenas conta o que vem asseguir
        lst = []
        for k in self.nodes.keys():
            #para cada chave no dicionário nodes vou verificar
            if type(self.nodes[k][0]) == int and self.nodes[k][0] >= 0 or \
                    type(self.nodes[k][0]) == tuple and self.nodes[k][0][0] >= 0:
                #se a chave do loop é um número ou um tuplo. E se for um número vemos se é >=0 ou se for um tuplo, se o primeiro número desse tuplo é >=0
                #se isto acontecer acrescentamos à lista lst
                lst.append(k)
            elif type(self.nodes[k][0]) == int and self.nodes[k][0] < 0 or \
                    type(self.nodes[k][0]) == tuple and self.nodes[k][0][0] < 0:
                # fazemos o mesmo mas desta vez verificamos se esses valores são menores que zero. Se sim ...
                if '$' in self.nodes[k][1]:
                    #se $ estiver presente então acrescentamos o valor do $ à lista
                    lst.append(self.nodes[k][1]['$'])
                if '$' in self.nodes[k][1] and len(self.nodes[k][1]) == 1 or '#' in self.nodes[k][1] and\
                        len(self.nodes[k][1]) == 1:
                    #se o tamanho do dicionário for =1 e estiver presente como chave desse dicionário $ ou o #
                    #acrescentamos ao dicionário
                    lst.append(k)
                if '#' in self.nodes[k][1]:
                    #se # estiver presente então acrescentamos o valor do # à lista
                    lst.append(self.nodes[k][1]['#'])
        for r in lst:   #para cada valor de lst
        #se esse valor estiver em res vai remover as terminações ($ e #)
            if r in res:
                res.remove(r)
        return sorted(res)

    def matches_prefix(self, prefix):
        '''
        Método que permita, dada uma string (prefixo), verificar todos os padrões distintos que
        iniciem por esse prefixo e que estejam contidos na sequência que deu origem à árvore.

        '''
        res = []
        res1 = []
        a = 0
        b = 0
        if prefix not in self.seq1 and prefix not in self.seq2:     
        #primeiro procurar nas sequencias se existe existe o prefixo, se não existir obtemos um tuplo com lista vazia
            return (0, res), (1, res1)

        elif prefix in self.seq1 and prefix not in self.seq2:
            #se o prefixo existir em seq1 e não existir na seq2
            for p in range(len(self.seq1)):
                if self.seq1[p] == prefix[0]:
                #fazemos um loop para procurar onde pode começar o prefixo na sequencia
                    a = p
                    for l in range(len(prefix)):
                        
                        if self.seq1[p + l] == prefix[l]:
                        #se a proxima letra na sequencia for igual à proxima letra do prefixo...
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i is True:
                        #criamos uma string que retém toda a sequencia a partir do prefixo
                        string = self.seq1[a + len(prefix):]
                        #coloca dentro do dicionário todas as letras a partir do prefixo a
                        res.append(self.seq1[a:])
                        for f in range(len(string)):
                            #acrescenta ao dicionário o prefixo mais uma parte da string para termos todos
                            #os padrões distintos que se iniciem com esse prefixo
                            res.append(prefix + string[:f])
                        return (0, sorted(list(set(res)))), (1, res1)
                    

        elif prefix not in self.seq1 and prefix in self.seq2:
            #exatamente o mesmo que a anterior
            #se o prefixo não existir em seq1 e existir na seq2
            for p in range(len(self.seq2)):
                if self.seq2[p] == prefix[0]:
                    b = p
                    for l in range(len(prefix)):
                        if self.seq2[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i is True:
                        string = self.seq2[b + len(prefix):]
                        res1.append(self.seq2[b:])
                        for f in range(len(string)):
                            res1.append(prefix + string[:f])
                        return (0, res), (1, sorted(list(set(res1))))
                    

        else:
            #se o prefixo existir em seq1 e em seq2
            #voltamos a fazer o mesmo só que para cada uma
            for p in range(len(self.seq1)):
                if self.seq1[p] == prefix[0]:
                    a = p
                    for l in range(len(prefix)):
                        if self.seq1[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i == True:
                        string = self.seq1[a + len(prefix):]
                        res.append(self.seq1[a:])
                        for f in range(len(string)):
                            res.append(prefix + string[:f])
                if self.seq2[p] == prefix[0]:
                    b = p
                    for l in range(len(prefix)):
                        if self.seq2[p + l] == prefix[l]:
                            i = True
                            pass
                        else:
                            i = False
                            break
                    if i == True:
                        string = self.seq2[b + len(prefix):]
                        res1.append(self.seq2[b:])
                        for f in range(len(string)):
                            res1.append(prefix + string[:f])
        return (0, sorted(list(set(res)))), (1, sorted(list(set(res1))))

    def largestCommonSubstring(self):
        '''
        Encontrar a maior substring comum a ambas as sequencias

        '''
        lst = []
        string1 = self.seq1
        string2 = self.seq2

        for sub in range(len(string1)):
            #colocar em lst todas as substrings existentes na seq1
            lst.append(string1[sub:])
        lst = list(set(lst))    #remoção das substrings repetidas
        for p in lst:
            if p not in string2:
                #se alguma substring em seq1 não existir em seq 2, vamos remover porque não são concidentes
                lst.remove(p)
        if len(lst) == 0:
            #se a lista estiver vazia, então não existem substrings comuns
            return None
        elif len(lst) == 1:
            #se só existir 1 substring comum esse será a nossa maior coincidente
            return lst
        else:
            #se existir mais do que 1 substring comum então vamos organizar a lista por tamanho, de maior para menor
            #e o resultado será a primeira substring da lista
            sorted(lst, key=len, reverse=True)
            return lst[0]


def test():
    seq1 = 'TACTA'
    seq2 = 'AGTAC'
    stm = SuffixTreeMulti()
    stm.suffix_tree_from_seq(seq1, seq2)
    stm.print_tree()
    print(stm.find_pattern("TA"))
    print(stm.find_pattern("ACG"))
    print(stm.nodes_below(12))
    print(stm.matches_prefix('TA'))
    print(stm.matches_prefix('GT'))


test()