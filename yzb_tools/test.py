import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient(host="39.107.25.250", port=27017,username="admin",password="caigou2003")


print(myclient.list_database_names())


db = myclient['bid_test']

cols = db['yzb_test']

ccc = cols.find()
for i in ccc:
    print(i)


# cols.insert_many([{'id': 333, 'title': 'zhongguo dsadsazhaobiao', 'url': 'www.abdsadsac.com', 'tags': ['3', '6', '9']},
#                   {'id': 444, 'title': 'zhongguo dsadsazhaobiao', 'url': 'www.abdsadsac.com', 'tags': ['3', '6', '9']}])
print('------------------------')
# cols.update_one({'id':333},{'$set':{'title':'xiugaihou','url':'www.www.www.com'}})
# 查询的时候返回的是一个list
fff = cols.find({'id':{'$gt':340}})
print(fff)
for i in fff:
    print(i)

# ccc = cols.find()
# for i in ccc:
#     print(i)