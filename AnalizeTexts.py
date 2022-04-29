
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
    def SaveDictionary(self):
        file = open('Dict.txt','w')
        for i in self.diction:
            line = i[0]+'#'
            for j in i[1]:
                line += j+'#'
            line+='\n'
            file.write(line)
        file.close()

    def LoadDictionory(self):
        file = open('Dict.txt','r')
        filesdata = file.readlines()
        for i in filesdata:
            line = i.split('#')
            self.AddDict(line[0],line[1:-1])
        file.close()

    def __init__(self):
        self.diction = []
        self.LoadDictionory()

    def AddDict(self,name,dict=[]): #добавление словаря
        if type(dict) != list:
            self.diction.append([name,[dict]])
        else:
            self.diction.append([name,dict])

    def AddWords(self,numb,words): #добавление слова/слов в словарь
        self.diction[numb][1].extend(words)

    def Show(self):
        for i in self.diction:
            print("Словарь",i[0],":", i[1])

def analis(txt):
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

fileDoc = docx.Document('Text.docx')
text=''
for paragraph in fileDoc.paragraphs:
    text+=paragraph.text
#text = 'Посол Израиля 21 на Украине Йоэль Лион признался, что пришел в шок, узнав о решении властей Львовской области объявить 2019 год годом лидера запрещенной в России Организации украинских националистов (ОУН) Степана Бандеры. Свое заявление он разместил в Twitter. «Я не могу понять, как прославление тех, кто непосредственно принимал участие в ужасных антисемитских преступлениях, помогает бороться с антисемитизмом и ксенофобией. Украина не должна забывать о преступлениях, совершенных против украинских евреев, и никоим образом не отмечать их через почитание их исполнителей», — написал дипломат. 11 декабря Львовский областной совет принял решение провозгласить 2019 год в регионе годом Степана Бандеры в связи с празднованием 110-летия со дня рождения лидера ОУН (Бандера родился 1 января 1909 года). В июле аналогичное решение принял Житомирский областной совет. В начале месяца с предложением к президенту страны Петру Порошенко вернуть Бандере звание Героя Украины обратились депутаты Верховной Рады. Парламентарии уверены, что признание Бандеры национальным героем поможет в борьбе с подрывной деятельностью против Украины в информационном поле, а также остановит «распространение мифов, созданных российской пропагандой». Степан Бандера (1909-1959) был одним из лидеров Организации украинских националистов, выступающей за создание независимого государства на территориях с украиноязычным населением. В 2010 году в период президентства Виктора Ющенко Бандера был посмертно признан Героем Украины, однако впоследствии это решение было отменено судом. '
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