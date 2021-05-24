class BoyerMoore:
    
	def __init__(self, alphabet, pattern):
		self.alphabet = alphabet
		self.pattern = pattern
		self.preprocess()

	def preprocess(self):
		self.process_bcr()        #bad character rule
		self.process_gsr()        #good suffix rule
        
	def process_bcr(self):
        #pré-processamento da bad character rule
		self.occ = {'A': 5, 'C': -1, 'T': 2, 'G': 1}      #última posição das letras na sequencia (aqui só está a dar um exemplo porque poderia estar vazio)
		for c in self.alphabet:       #para um valor no alfabeto
			self.occ[c] = -1         #insere no dicionário com o valor -1
		for i in range(len(self.pattern)):    #para um valor i de 0 até ao tamanho do meu padrão
			self.occ[self.pattern[i]] = i     #se a letra existir no nosso padrão o valor -1 é alterado pela última posição da letra. se isto não acontecer mantém-se o -1 significando que não existe no padrão 

	def process_gsr(self):
        #pré-processamento do good suffix rule
		self.f = []
		self.s = []
		for i in range(len(self.pattern)+1):      #para um valor i 
			self.f.append(0)
			self.s.append(0)

		i = len(self.pattern)
		j = len(self.pattern)+1
		self.f[i] = j
        
		while i > 0:
			while j <= len(self.pattern) and self.pattern[i-1] != self.pattern[j-1]:
				if self.s[j] == 0:
					self.s[j] = j-i
				j = self.f[j]
			i -= 1
			j -= 1
			self.f[i] = j
            
		j = self.f[0]
        
		for i in range(len(self.pattern)):
			if self.s[i] == 0:
				self.s[i] = j
			if i == j:
				j = self.f[j]
	
	def search_pattern(self, text):
        
	    #Procura o padrão dado na sequencia.
        #Utiliza as estruturas resultantes dos pré-processamento, usando as 2 regras para avançar para o número máximo de posições permitidas.
	    
		res = []
		i = 0    # Posição da sequência
		while i <= (len(text) - len(self.pattern)):   #enquanto que a posição da sequencia é <= ao tamanho do texto - o tamanho do padrão
			j = len(self.pattern)-1                  # a variável j é igual à posição do padrão na sequencia (tamanho do padrão -1)
			while j >= 0 and self.pattern[j] == text[j+i]:   #enquanto que j>=0 e o padrão na posição j = texto na posição j + i
				j -= 1                              # retira-se 1 à posição do padrão (procurando assim os match)
			if j < 0:                            #se j<0
				res.append(i)                   #adiciona posição da sequencia ao dicionário res
				i = i + self.s[0]               #assim a posição da sequencia vai ser i+
			else:
				c = text[j+i]
				i += max(self.s[j+1], j-self.occ[c])
		return res


def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print(bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))


test()

# result = [5, 13, 23, 37]