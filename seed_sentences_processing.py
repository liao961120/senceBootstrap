import jieba
import unicodedata
import re

from itertools import chain
def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def seed2keys2(sentence, stopwords, l_window=6, r_window=6):
    # Extract target_word
    lemma_reg = re.compile(r'<(.+?)>')
    target_word = lemma_reg.search(sentence).group(1)

    # Cleaning
    sentence = delete_punctuation(sentence)
    sentence = sentence.replace('<', '')
    sentence = sentence.replace('>', '')
    
    # Segmentation
    tokens = jieba.lcut(sentence)
    #tokens = list(set(tokens))
    
    # Remove stop words & punc
    for tk in tokens:
        if tk in stopwords:
            tokens.remove(tk)
    
    text = ''.join(tokens)
    idx = text.find(target_word)
    if idx != 1:
        l_idx = 0 if (idx - l_window < 0) else (idx - l_window)
        r_idx = len(text) if (idx + r_window + len(target_word) < len(text)) else (idx + r_window + len(target_word))
        text = text[l_idx:r_idx]        
    
    return([target_word, text])




def seed2keys(sentence, stopwords):
    # Extract target_word
    lemma_reg = re.compile(r'<(.+?)>')
    target_word = lemma_reg.search(sentence).group(1)

    # Cleaning
    sentence = delete_punctuation(sentence)
    sentence = sentence.replace('<', '')
    sentence = sentence.replace('>', '')
    
    # Segmentation
    tokens = jieba.lcut(sentence)
    tokens = list(set(tokens))
    
    # Remove stop words & punc
    for tk in tokens:
        if tk in stopwords:
            tokens.remove(tk)
    
    tokens.insert(0, target_word)
    return(tokens)


def has_punctuation(string):
    regexp = re.compile(r'[^0-9A-Za-z\u4E00-\u9FFF]+')
    
    has_punc = False
    if regexp.search(string):
        has_punc = True
    return(has_punc)


def delete_punctuation(text):
    """删除标点符号"""
    text = re.sub(r'[^0-9A-Za-z\u4E00-\u9FFF]+', '', text)
    return(text)


## Get stopwords
with open('stop_words.txt') as f:
    stopwords = f.readlines()
stopwords = [x.strip() for x in stopwords] 
stopwords = set(stopwords)

"""
#text = posts[0]['content']


# Text cleaning: remove punctuations
text = unicodedata.normalize('NFKC', text)
text = delete_punctuation(text)
text = text.strip('\n')

# Remove stop words
tokens = jieba.lcut(text)
for tk in tokens:
    if tk in stopwords:
        tokens.remove(tk)
"""