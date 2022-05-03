
import docx
import string
import nltk
from nltk.corpus import stopwords
from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)

class dictionaries:
    def __init__(self): 
        self.diction = []
        self.LoadDictionory()

    def SaveDictionary(self): #сохранение словаря в файл
        file = open('narkotiki','w')
        for i in self.diction:
            line = i[0]+'#'
            for j in i[1]:
                line += j+'#'
            line+='\n'
            file.write(line)
        file.close()

    def LoadDictionory(self): #загрузка словаря из файля в систему
        file = open('narkotiki.txt','r')
        filesdata = file.readlines()
        for i in filesdata:
            line = i.split('#')
            self.AddDict(line[0],line[1:-1])
        file.close()

    def AddDict(self,name,dict=[]): #добавление словаря
        if type(dict) != list:
            self.diction.append([name,[dict]])
        else:
            self.diction.append([name,dict])

    def AddWords(self,numb,words): #добавление слова/слов в словарь
        self.diction[numb][1].extend(words)

    def Show(self): #вывод словарей
        for i in self.diction:
            print("Словарь",i[0],":", i[1])

def analis(txt): #анализ текста (процентное соотношение)
    numb = len(dictionary.diction)
    NumbOfWords = len(txt.split())
    for i in range (numb):
        coun = 0
        for j in dictionary.diction[i][1]:
            coun += txt.count(j)
        print('Процентное соотношение по словарю',dictionary.diction[i][0],':',coun/NumbOfWords*100,'%')

dictionary = dictionaries()

#nltk.download('stopwords')

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

fileDoc = docx.Document('Text.docx') #загрузка текста из вордовского документа в систему
text=''
for paragraph in fileDoc.paragraphs:
    text+=paragraph.text
doc = Doc(text)

doc.segment(segmenter) #разбивает на токены(слова, знаки припинания)
doc.tag_morph(morph_tagger) #определяет часть речи
for token in doc.tokens:    #приводит всё к начальной форме(слова, знаки и прочее)
    token.lemmatize(morph_vocab)

doc.parse_syntax(syntax_parser)  #определяет связи
doc.tag_ner(ner_tagger)  #извлечение сущностей
for span in doc.spans:   #нормализация сущностей
   span.normalize(morph_vocab)

text_new = ''    
stop = stopwords.words("russian")
rubbish = string.punctuation + '—' + '«' + '»'
for _ in doc.tokens:                             #вывод слов без мусора
    if _.lemma in rubbish or _.lemma in stop or  _.lemma.isdigit():
        continue
    text_new += ' ' + _.lemma
    #print(_.lemma)

#print(text_new)

dictionary.Show()
analis(text_new)


'''for _ in doc.tokens:  #вывод слов и знаков в начальной форме
    print(_.lemma)'''

'''for _ in doc.spans:  #вывод сущностей в начальной форме
   print( _.normal)'''