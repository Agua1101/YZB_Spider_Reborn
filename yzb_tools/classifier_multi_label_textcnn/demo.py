import predict
from db_connect import *
from conf import config as conf


d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)


# 识别品目demo
def predict_one(sentence):
    items= predict.get_label(sentence)
    # print(items)
    try:
        item_cn = ','.join([d_save.runSql_select(f'select name from t_item where code = "{item}"')[0][0] for item in items])
    except:
        return '未识别到品目'
    if item_cn:
        return f'识别到品目： {item_cn}'
    else:
        return '未识别到品目'






if __name__ == '__main__':
    sentences = '浙江航空开发有限责任公司3号库改造项目招标公告'
    print('----------------------------')
    print(f'标题：{sentences}')
    print(predict_one(sentences))
    print('----------------------------')







