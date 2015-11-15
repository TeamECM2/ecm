from topia.termextract import tag
from topia.termextract import extract
import pickle

def extractTokens(para):

	tagger = tag.Tagger()
	tagger.initialize()
	extractor = extract.TermExtractor()
	extractor.tagger
	extractor = extract.TermExtractor(tagger)
	extractor.filter = extract.permissiveFilter
	extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=1)
	#print 'Key Words:',
	a=[]
	for i in extractor(para):
		a.append(i[0])
		#print '  ',i[0], 
	return a


para = pickle.load(open("../save.p", "rb"))
#para = "the god is angry at the dog"
a = extractTokens(para)
print (a)
pickle.dump(a, open("../temp.p", "wb"))