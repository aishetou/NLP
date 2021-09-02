
from flask import Flask, render_template ,request
import nltk
from nltk.corpus import stopwords
import string
import re
from nltk.tokenize import sent_tokenize
import heapq

app = Flask(__name__)

@app.route('/')
def summ():
    return render_template('page.html',lang="Arabic",dir="rtl",input="النص",output="الملخص",num="عدد جمل الملخص",button="تلخيص")


        
@app.route('/<l>')
def lg(l=None):
        if (l=="French") :
            d="ltr"
            input="texte à résumer"
            output="Résumé"
            num="Le nombre de phrases souhaité"
            button="Résumer"
        elif (l=="English")   :
            d="ltr"   
            input="Text to summarize"
            output="Summary"
            num="Number of sentences wanted" 
            button="Summarize"  
        else :
            d="rtl"
            input="النص"
            output="الملخص"
            num="عدد جمل الملخص"
            button="تلخيص" 
        return render_template('page.html', lang=l,dir=d,input=input,output=output,num=num,button=button)



@app.route('/<lang>', methods=['POST'])

def my_form_post(lang=None):
    if (lang=="French") :
                d="ltr"
                input="texte à résumer"
                output="Résumé"
                num="Le nombre de phrases souhaité"
                button="Résumer"
    elif (lang=="English")   :
                d="ltr"   
                input="Text to summarize"
                output="Summary"
                num="Number of sentences wanted" 
                button="Summarize"  
    else :
                d="rtl"
                input="النص"
                output="الملخص"
                num="عدد جمل الملخص"
                button="تلخيص"

      
    text = request.form.get('text')
    num_sentences= int(request.form.get('num_sentences'))
    stop_words=nltk.corpus.stopwords.words(lang)
    punctuation = set(string.punctuation)


#Enlever les espaces , les majuscules et les retours a la ligne
    t=text.lower().strip('\t\n')

#Enlever les stop words et la ponctuation puis faire la Tokenization en mots et en phrases du texte 
    words = [word for word in t.split() if word not in stop_words and punctuation ]
    sentences = sent_tokenize(t.lower())
    
 #Calculer les frequences des mots --> dictionnaire (cle - mot,valeur - la frequence)
    word_frequency = {}
    
    for word in words:
            if word not in word_frequency.keys():
                    word_frequency[word] = 1 
            else:
                    word_frequency[word] += 1 
    

#Weighted frequency 
    
    for word in word_frequency.keys():
            word_frequency[word] = (word_frequency[word]/len(words))

#calculate the scores for each sentence by adding weighted frequencies of its words
    scores = {}
    for sent in sentences:
        sentence = sent.split(" ")
        for word in sentence:  
            if len(sentence) < 60:     
                if word.lower() in word_frequency.keys():
                    if sent not in scores.keys():
                        scores[sent] = word_frequency[word.lower()]
                    else:
                        scores[sent] += word_frequency[word.lower()]
    
#Les n meilleures phrases
    summary_sentences = heapq.nlargest(num_sentences, scores, key=scores.get)
    
#Ordre des phrases suivant le contexte
    Order = []
    sum = []
    i=0
    j = 0
    while i<len(summary_sentences):
        if(summary_sentences[i] in sentences):
                Order.append(sentences.index(summary_sentences[i]))
        i += 1
    while j<len(sorted(Order)):
        sum.append(sentences[sorted(Order)[j] ])
        j+=1
    summary = ' '.join(sum)



######################

    return render_template("page.html",lang=lang,input=input,output=output,num=num,button=button,text_input=text ,summary = summary ,dir=d)

  
 
if __name__ == '__main__':
  app.run(debug=True)


