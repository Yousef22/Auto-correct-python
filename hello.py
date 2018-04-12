import marisa_trie
#Structure trie pour réduire le temps d'exectuion et la consomuation méméoire


from flask import Flask, jsonify, request
app = Flask(__name__)

def load_french_dictionary():
	with open('/Users/macbook/Desktop/PYTHONPROJET/francais.txt', encoding='iso-8859-1') as f:
		content = f.read()
	letters = set()
	for word in content.split('\n'):
		for letter in word:
			letters.add(letter)
	return letters, marisa_trie.Trie(content.split('\n'))
#Je décompose le tuple renvoyé par load-french-dictionary
letters, t = load_french_dictionary()

# on fait une fonction qui prend en argument le mot de l'utilisateur 
#cette fonction renvoie la liste des mots similaire au mot de l'utilisateur 
def find_similar_words(word):
	# on cree un set des mots similaires
	# et pas une liste, pour eviter les doublons
	# on ne veut pas mettre suggerer plusieurs fois le meme mot
	similar_words = set()
	# on parcourt chaque caractere du mot de l'utilisateur (index i)
	for i in range(len(word) + 1):
		# pour chaque lettre de l'alphabet
		for l in letters:
			# SUBSTITUTION
			# si la lettre a substituer est la meme que celle qui est deja la
			# on ne fait rien. cependant si elle est differente, on fait la substitution
			if i < len(word) and l != word[i]:
				# on cree un nouveau mot, ou la lettre a l'index i est remplacee par la lettre l
				new_word = word[:i] + l + word[i + 1:]
				# si ce nouveau mot artificiel existe, on le rajoute a la liste des mots similaires
				if new_word in t:
					similar_words.add(new_word)
			# ADDITION
			# on cree un nouveau mot, ou on rajoute la lettre l a l'indice i, en preservant toutes les lettres qui sont deja dans le mot
			n_word = word[:i] + l + word[i:]
			# encore une fois, si ce mot artificiel existe, on le rajoute dans notre set
			if n_word in t:
				similar_words.add(n_word)
		# SUBSTRACTION
		# on cree un nouveau mot ou la lettre a l'indice i disparait
		N_word = word[:i] + word[i + 1:]
		# encore une fois, si ce nouveau mot artificiel existe, on le rajoute a notre set
		if N_word in t: 
			similar_words.add(N_word)
	
	# on veut proposer a l'utilisateur les mots commencant par la premier lettre de son mot en priorite
	# parce que souvent, il ne se trompe sur la premiere lettre
	# on cree deux listes qui vont contenir les mots commencant par la premiere lettre et ceux ne commencant pas par la premiere lettre
	same_first_letter = []
	not_same_first_letter = []
	# on parcourt les mots dans notre set
	for w in similar_words:
		# si le mot commence par la premiere lettre du mot de l'utilisateur
		if w.startswith(word[0]):
			# on le met dans la liste correspondante
			same_first_letter.append(w)
		# sinon
		else:
			# on le met dans l'autre liste
			not_same_first_letter.append(w)
	# on redefinit la variable 'similar_words' comme etant la concatenation
	# de ces deux listes, ou la premiere liste est bien celle contenant les mots
	# commencant par la premiere lettre du mot de l'utilisateur
	similar_words = same_first_letter + not_same_first_letter
	# on retourne notre liste
	return similar_words

@app.route('/', methods=['GET'])
def hello_world():
	# l'utilisateur fait une requete HTTP sur notre serveur
	# a l'adresse http://localhost:5000/?term=<mot-de-l-utilisateur>
	# la syntaxe de FLASK nous permet de recuperer le mot de l'utilisateur
	# en faisant 'word = request.args.get('term')
	word = request.args.get('term')
	# on appelle notre fonction pour recuperer les mots similaires au mot de l'utilisateur
	terms = find_similar_words(word)
	print(word)
	print(terms)
	# on transforme notre liste de mots en sa representation JSON
	response=jsonify(terms)
	response.headers.add('Access-Control-Allow-Origin', '*') 
	return response
