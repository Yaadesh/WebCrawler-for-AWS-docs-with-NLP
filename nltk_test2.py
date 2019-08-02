from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import nltk

def process(data):
	#raw = open(file).read()
	
	tokens = word_tokenize(data)
	#print('word_tokenize output')
	#print(tokens)
	words = [w.lower() for w in tokens]

	porter = nltk.PorterStemmer()
	stemmed_tokens = [porter.stem(t) for t in words]
	#print("STEMMED")
	#print(stemmed_tokens)

	stop_words = set(stopwords.words('english'))
	filtered_tokens = [ w for w in stemmed_tokens if not w in stop_words]

	count = nltk.defaultdict(int)
	for word in filtered_tokens:
		count[word] +=1
	#print(count['dynamodb'])
	print('process method')
	return count;

def cos_sim(a,b):
	dot_product = np.dot(a,b)
	norm_a = np.linalg.norm(a)
	norm_b = np.linalg.norm(b)
	print('cos_sim')
	return dot_product / (norm_a * norm_b)

def getSimilarity(cust_summary, blog_data):
	print('getSimilarity')
	dict1 = process(cust_summary)
	dict2 = process(blog_data)
	all_words_list = []
	for key in dict1:
		all_words_list.append(key)
	for key in dict2:
	    all_words_list.append(key)
	all_words_list_size = len(all_words_list)

	v1 = np.zeros(all_words_list_size, dtype = np.int)
	v2 = np.zeros(all_words_list_size, dtype = np.int)
	i=0
	for (key) in all_words_list:
		v1[i] = dict1.get(key,0)
		v2[i] = dict2.get(key,0)
		i = i +1
	return cos_sim(v1,v2);

if __name__ == '__main__':
	dict1 = process("/Users/vyaade/Desktop/doc1.txt")
	dict2 = process("/Users/vyaade/Desktop/doc2.txt")
	dict3 = process("/Users/vyaade/Desktop/doc3.txt")
	print("similarity between doc1 and doc2",getSimilarity(dict1,dict2))
	print("similarity between doc1 and doc3",getSimilarity(dict1,dict3))
