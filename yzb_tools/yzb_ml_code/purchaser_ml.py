#coding=UTF-8
# %matplotlib inline
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import jieba as jb
import re
from conf import config as conf
# from sklearn.externals import joblib

plt.rcParams['font.sans-serif'] = ['SimHei']
df = pd.read_excel(conf.ml_file)
# df.columns = ['id','review','cat']
df['review'] = df['p_name'].map(str)+df['c_name'].map(str)
df['cat'] = df['sort']
df = df[['cat', 'review']]
# print("数据总量: %d ." % len(df))
df.sample(8)

# print("在 cat 列中总共有 %d 个空值." % df['cat'].isnull().sum())
# print("在 review 列中总共有 %d 个空值." % df['review'].isnull().sum())
# df[df.isnull().values==True]
df = df[pd.notnull(df['review'])]

d = {'cat':df['cat'].value_counts().index, 'count': df['cat'].value_counts()}
df_cat = pd.DataFrame(data=d).reset_index(drop=True)
# print(df_cat)

# df_cat.plot(x='cat', y='count', kind='bar', legend=False,  figsize=(8, 5))
# plt.title("类目数量分布")
# plt.ylabel('数量', fontsize=18)
# plt.xlabel('类目', fontsize=18)
# plt.show()

df['cat_id'] = df['cat'].factorize()[0]
cat_id_df = df[['cat', 'cat_id']].drop_duplicates().sort_values('cat_id').reset_index(drop=True)
cat_to_id = dict(cat_id_df.values)
id_to_cat = dict(cat_id_df[['cat_id', 'cat']].values)
df.sample(10)

# print(cat_id_df)

# 定义删除除字母,数字，汉字以外的所有符号的函数
def remove_punctuation(line):
    line = str(line)
    if line.strip() == '':
        return ''
    rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5]")
    line = rule.sub('', line)
    return line


def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


# 加载停用词
stopwords = stopwordslist(conf.stop_word)

#删除除字母,数字，汉字以外的所有符号
df['clean_review'] = df['review'].apply(remove_punctuation)
df.sample(10)

#分词，并过滤停用词
df['cut_review'] = df['clean_review'].apply(lambda x: " ".join([w for w in list(jb.cut(x)) if w not in stopwords]))
df.head()

from collections import Counter
from wordcloud import WordCloud


# def generate_wordcloud(tup):
#     wordcloud = WordCloud(background_color='white',
#                           font_path='simhei.ttf',
#                           max_words=50, max_font_size=40,
#                           random_state=42
#                           ).generate(str(tup))
#     return wordcloud
#
#
# cat_desc = dict()
# for cat in cat_id_df.cat.values:
#     text = df.loc[df['cat'] == cat, 'cut_review']
#     text = (' '.join(map(str, text))).split(' ')
#     cat_desc[cat] = text
#
# fig, axes = plt.subplots(4, 2, figsize=(30, 38))
# k = 0
# for i in range(4):
#     for j in range(2):
#         cat = id_to_cat[k]
#         most100 = Counter(cat_desc[cat]).most_common(100)
#         ax = axes[i, j]
#         ax.imshow(generate_wordcloud(most100), interpolation="bilinear")
#         ax.axis('off')
#         ax.set_title("{} Top 100".format(cat), fontsize=30)
#         k += 1

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(norm='l2', ngram_range=(1, 2))
features = tfidf.fit_transform(df.cut_review)
labels = df.cat_id
# print(features.shape)
# print('-----------------------------')
# print(features)

from sklearn.feature_selection import chi2


N = 2
# for cat, cat_id in sorted(cat_to_id.items()):
#     features_chi2 = chi2(features, labels == cat_id)
#     indices = np.argsort(features_chi2[0])
#     feature_names = np.array(tfidf.get_feature_names())[indices]
#     unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
#     bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
    # print("# '{}':".format(cat))
    # print("  . Most correlated unigrams:\n       . {}".format('\n       . '.join(unigrams[-N:])))
    # print("  . Most correlated bigrams:\n       . {}".format('\n       . '.join(bigrams[-N:])))

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

X_train, X_test, y_train, y_test = train_test_split(df['cut_review'], df['cat_id'], random_state=0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)




from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.model_selection import cross_val_score

models = [
    RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
    LinearSVC(),
    MultinomialNB(),
    LogisticRegression(random_state=0),
]
CV = 5
# cv_df = pd.DataFrame(index=range(CV * len(models)))
entries = []
for model in models:
    model_name = model.__class__.__name__
    accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))

cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])

import seaborn as sns

# sns.boxplot(x='model_name', y='accuracy', data=cv_df)
# sns.stripplot(x='model_name', y='accuracy', data=cv_df,
#               size=8, jitter=True, edgecolor="gray", linewidth=2)
# plt.show()

print(cv_df.groupby('model_name').accuracy.mean())


# joblib.dump(clf,'./saved_model/clf.pkl')
# clf = joblib.load('./saved_model/clf.pkl')


def myPredict(sec):
    format_sec=" ".join([w for w in list(jb.cut(remove_punctuation(sec))) if w not in stopwords])
    pred_cat_id=clf.predict(count_vect.transform([format_sec]))
    predict = id_to_cat[pred_cat_id[0]]
    # print('\n')
    # print('-------预测结果---------')
    # print(predict)
    # print('-----------------------')
    return predict


if __name__ == '__main__':

    myPredict('宁津县黄河大街供水管道采购项目 宁津县黄河大街供水管道采购项目废标公告 2019年05月21日 11:54【 公告概要： 公告信息： 采购项目名称 宁津县黄河大街供水管道采购项目 品目 采购单位 宁津县水务局 行政区域 德州市 公宁津县水务局')

