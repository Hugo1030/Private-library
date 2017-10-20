# -*- coding:utf-8 -*-

import jieba.posseg as pseg
from collections import Counter, defaultdict
import jieba
import random


def generate(lm):
    x = random.random()
    s_ = 0.0
    for word, prob in lm.items():
        s_ += prob
        if s_ >= x:
            return word

# f为所读取的文件；ngram 为gram个数；N为生成句子的词数
def ngram_lm(f, ngram=2, N=100):
    # 设置行的计数，在超过一定限值之后停止文件读取
    line_no = 0
    max_line = 5000

    # dct用于保存语ngram语言模型的概率
    # P(w_i|w_1, w_2, ... w_(i-1)) = P(w_i) * P(w_i|w_1, w_2, ... w_(ngram-1))
    # 键为context，即w_1, w_2, ... w_(ngram-1)组成的tuple；值为在context的条件下w_i的概率分布
    dct = defaultdict(Counter)

    # 对words的左侧进行填充（padding）
    start_token = "<s>"
    # 逐行读取文件，防止一次读取造成内存不足
    for line in open(f):
        line_no += 1
        if line_no >= max_line:
            break
        # 开始分词
        words = list(jieba.cut(line.strip()))
        # 左侧用(ngram - 1)个start_token进行填充（padding）
        padded_words = [start_token] * (ngram - 1) + words

        # context 是 w_1, w_2, ... w_(ngram-1)
        # word 是各种可能的 w_i
        for i in range(len(words)):
            context = padded_words[i: i+ngram-1]
            word = words[i]
            # list 不能作为key，将其转换为tuple
            dct[tuple(context)][word] += 1

    # 将dct中Counter的计数转换为概率
    for context, counter in dct.items():
        s = float(sum(counter.values()))
        for word in counter.keys():
            counter[word] /= s

    # 生成N个词ngram；句首为 ngram-1 个 "<s>"
    l = [start_token] * (ngram - 1)
    for i in range(N):
        context = l[-ngram+1:]
        counter = dct[tuple(context)]
        # 如果上下文有相应的w_i
        if counter:
            word = generate(counter)
            l.append(word)
        # 如果没有相应的下文，则另起一段，从"<s>" 重新开始
        else:
            l.append("\n\n")
            l += [start_token] * (ngram - 1)

    sentence = "".join(l)
    return sentence

print(ngram_lm(f="yzp_blog.csv", ngram=4, N=200))
