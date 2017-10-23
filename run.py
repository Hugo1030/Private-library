import jieba
import random
from collections import Counter, defaultdict

def generate_lm(filepath,ngram):

    lm = defaultdict(Counter)

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        words = jieba.cut(line.strip()) #用 jieba 分词，去掉空格
        words = [i for i in words] #jieba 返回的是 generator，无法知道长度，需要转成 list
        words = ['<S>'] * ngram + words #句首padding，添加ngram个'<S>'

        for i in range(ngram, len(words)): # 从第 n 个词开始
            context = words[(i-ngram):i] # 当前词前面的 n 个词（上文）
            word = words[i] # 当前词
            lm[''.join(context)][word] += 1 # 统计 “前 n 个词+当前词”（即ngram词组） 出现的频率, lm[key][value]

    # 算出每个 ngram 词组的归一化词频
    for key in lm.keys():
        k = lm[key]
        s = float(sum(k.values()))
        for word,cnt in k.items():
            k[word] /= s

    return lm

def generate_word(context,lm):
    r = random.random()
    s_ = 0.0
    for (word, prob) in lm[context].items():
        s_ += prob
        if s_ >= r:
            return word

def generate_sentence(lm, ngram):
    para = ''
    lastwords=['<S>'] * ngram
    for i in range(100):
        word = generate_word(''.join(lastwords),lm)
        if not word:
            break;
        para += word
        lastwords.append(word)
        if len(lastwords) > ngram:
            lastwords.pop(0)
    return para
