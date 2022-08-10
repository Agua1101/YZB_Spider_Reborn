#coding=UTF-8
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import Conv1D, MaxPooling1D, Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
import keras
import numpy as np
import pandas as pd
import jieba
from db_connect import *
from conf import config as conf

df = pd.read_excel(conf.item_file)
with open(conf.stop_word,encoding='utf-8')as r:
    stopwords=[i.replace('\n','') for i in r.readlines()]
X = df.iloc[:,0]
Y = df.iloc[:,1:]
X = [' '.join(jieba.lcut(i)) for i in X.tolist()]



MAX_SEQUENCE_LENGTH = 30 # 每条新闻最大长度
EMBEDDING_DIM = 200 # 词向量空间维度
VALIDATION_SPLIT = 0.16 # 验证集比例
TEST_SPLIT = 0.2 # 测试集比例

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)
sequences = tokenizer.texts_to_sequences(X)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
# labels = to_categorical(np.asarray(Y))
labels = Y

print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

p1 = int(len(data)*(1-VALIDATION_SPLIT-TEST_SPLIT))
p2 = int(len(data)*(1-TEST_SPLIT))
x_train = data[:p1]
y_train = labels[:p1]
x_val = data[p1:p2]
y_val = labels[p1:p2]
x_test = data[p2:]
y_test = labels[p2:]
print('train docs: '+str(len(x_train)))
print('val docs: '+str(len(x_val)))
print('test docs: '+str(len(x_test)))

model = keras.Sequential()
model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
model.add(Dropout(0.2))
model.add(Conv1D(250, 3, padding='valid', activation='relu', strides=1))
model.add(MaxPooling1D(3))
model.add(Flatten())
model.add(Dense(EMBEDDING_DIM, activation='relu'))
model.add(Dense(labels.shape[1], activation='sigmoid'))
model.summary()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(x_train,y_train,epochs=5)

# model.save('word_vector_cnn.h5')
# print(model.evaluate(x_test, y_test))


def random_pick(some_list, probabilities):
    import random

    item_list = some_list
    gailv = probabilities
    cc = []
    for i in range(3):
        x = random.uniform(0, 1)
        # print(x)
        cumulative_probability = 0.0
        for item, item_probability in zip(item_list, gailv):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                item_list.remove(item)
                gailv.remove(item_probability)
                cc.append(item)
                break
    return cc

def predict(text):
    title_list = ['A01','A02','A03','A04','A05','A06','A07','A08','A09','A10','A11','A12','A13','A14','A15','A16','A17','A18','A19','A99','B01','B02','B03','B04','B05','B06','B07','B08','B09','B99','C01','C02','C03','C04','C05','C06','C07','C08','C09','C10','C11','C12','C13','C14','C15','C16','C17','C18','C19','C20','C21','C22','C23','C99']
    text_cut = jieba.lcut(text)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(text_cut)
    sequences = tokenizer.texts_to_sequences(text_cut)
    word_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(word_index))
    data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    # print(data)
    predict_first = model.predict(data).tolist()
    # print(predict_first)
    # predict_end = []
    for i in predict_first[0:1]:
        # predict_num = []
        result_list = [round(x,3) for x in i]
        # print(result_list)
        predict_num = random_pick(title_list, result_list)
        # predict_end = getListMaxNumIndex(result_list)
        # n = 0
        # for i in range(3):
            # if len(predict_end) >= 3:
            #     break
            # item_index = predict_first.index(max(predict_first))
            # predict_end.append(item_index)
            # predict_first.pop(item_index)
            # else:
            #     predict_end.append(0)
            # n += 1
        # if not predict_end:
        #     predict_end.append(predict_first.index(max(predict_first)))
        # print(predict_end,len(predict_end))
        # for i in predict_end:
        #     predict_num.append(title_list[i])
        return predict_num

if __name__ == '__main__':

    print(predict('渝北区公安分局网络系统建设采购（网上下载）(项目编号=14A574)-竞争性谈判公告'))
    print(predict('莆田龙兴招标代理有限公司中小学校作业本政府采购中标公告-PTLX20140701-1'))
    print(predict('福建农林大学电磁炉、厨具设备采购项目-FJJF20140162-1中标公告-FJJF20140162-1'))
    print(predict('灵武市城市公用事业管理中心政府大楼消防设施维护的更换项目中标公告'))
    print(predict('山东华标招标有限公司关于文昌馨苑小学数字化校园建设公开招标公告'))
    print(predict('灵武市城市公用事业管理中心下水井盖项目中标公告'))





