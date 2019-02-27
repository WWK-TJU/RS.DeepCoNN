# -*- coding:utf-8 -*-
'''
Data pre process

@author:
Chong Chen (cstchenc@163.com)

@ created:
25/8/2017
@references:
'''

import os
import json
import pandas as pd
import pickle
import numpy as np

# https://www.cnblogs.com/fmgao-technology/p/9078918.html　对pickle详细解释
TPS_DIR = '../data/music'
TP_file = os.path.join(TPS_DIR, 'Digital_Music_5.json')

f= open(TP_file)
users_id=[]
items_id=[]
ratings=[]
reviews=[]
np.random.seed(2017)

control = 0
for line in f:
    # if control < 50:
    #     control += 1
        js=json.loads(line)
        if str(js['reviewerID'])=='unknown':
            print "unknown"
            continue
        if str(js['asin'])=='unknown':
            print "unknown2"
            continue
        reviews.append(js['reviewText'])
        users_id.append(str(js['reviewerID'])+',')
        items_id.append(str(js['asin'])+',')
        ratings.append(str(js['overall']))

data=pd.DataFrame({'user_id':pd.Series(users_id),
                   'item_id':pd.Series(items_id),
                   'ratings':pd.Series(ratings),
                   'reviews':pd.Series(reviews)})[['user_id','item_id','ratings','reviews']]

# print data
'''计算每个user_id and item_id 在数据中出现的次数'''
def get_count(tp, id):
    playcount_groupbyid = tp[[id, 'ratings']].groupby(id, as_index=False)
    count = playcount_groupbyid.size()
    return count

usercount, itemcount = get_count(data, 'user_id'), get_count(data, 'item_id')
# print usercount
'''取出每一个user_id and item_id 的 id'''
unique_uid = usercount.index
unique_sid = itemcount.index

# print unique_uid
'''就是把每一个user_id and item_id做成字典'''
item2id = dict((sid, i) for (i, sid) in enumerate(unique_sid))
user2id = dict((uid, i) for (i, uid) in enumerate(unique_uid))
# print user2id
# print item2id
'''这个其实就是吧user_id and item_id 数字化'''
def numerize(tp):
    uid = map(lambda x: user2id[x], tp['user_id'])
    sid = map(lambda x: item2id[x], tp['item_id'])
    tp['user_id'] = uid
    tp['item_id'] = sid
    return tp

data=numerize(data)
tp_rating=data[['user_id','item_id','ratings']]

# print tp_rating

# 数据的行数
n_ratings = tp_rating.shape[0]



test = np.random.choice(n_ratings, size=int(0.20 * n_ratings), replace=False)
test_idx = np.zeros(n_ratings, dtype=bool)
test_idx[test] = True
'''tp_1 and tp_train分别是(数据中包含)无评论信息的测试数据和训练数据'''
tp_1 = tp_rating[test_idx]
tp_train= tp_rating[~test_idx]
'''data and data2分别是(数据中包含)有评论信息的测试数据和训练数据'''
data2=data[test_idx]
data=data[~test_idx]


n_ratings = tp_1.shape[0]
test = np.random.choice(n_ratings, size=int(0.50 * n_ratings), replace=False)

test_idx = np.zeros(n_ratings, dtype=bool)
test_idx[test] = True

tp_test = tp_1[test_idx]
tp_valid = tp_1[~test_idx]
# 其实这块的是是三个数据集都是没有评论信息的
tp_train.to_csv(os.path.join(TPS_DIR, 'music_train.csv'), index=False,header=None)
tp_valid.to_csv(os.path.join(TPS_DIR, 'music_valid.csv'), index=False,header=None)
tp_test.to_csv(os.path.join(TPS_DIR, 'music_test.csv'), index=False,header=None)

user_reviews={}
item_reviews={}
user_rid={}
item_rid={}

# print data.values
# ['user_id','item_id','ratings','reviews']
for i in data.values:
    if user_reviews.has_key(i[0]):
        user_reviews[i[0]].append(i[3])
        user_rid[i[0]].append(i[1])
    else:
        user_rid[i[0]]=[i[1]]
        user_reviews[i[0]]=[i[3]]
    if item_reviews.has_key(i[1]):
        item_reviews[i[1]].append(i[3])
        item_rid[i[1]].append(i[0])
    else:
        item_reviews[i[1]] = [i[3]]
        item_rid[i[1]]=[i[0]]


'''data2 是测试集合，这快代码不合理吧，user_rid[i[0]]=[0]这样的话没出现的user都评论第0个item去了
没出现的item都评论都被第0个user评论了， item_reviews[i[1]] = [0]'''
# for i in data2.values:
#     if user_reviews.has_key(i[0]):
#         l=1
#     else:
#         user_rid[i[0]]=[0]
#         user_reviews[i[0]]=['0']

#     if item_reviews.has_key(i[1]):
#         l=1
#     else:
#         item_reviews[i[1]] = [0]
#         item_rid[i[1]]=['0']

# print user_reviews
# print item_reviews
# print user_rid
# print item_rid
# print np.shape(item_reviews[0])
pickle.dump(user_reviews, open(os.path.join(TPS_DIR, 'user_review'), 'wb'))
pickle.dump(item_reviews, open(os.path.join(TPS_DIR, 'item_review'), 'wb'))
pickle.dump(user_rid, open(os.path.join(TPS_DIR, 'user_rid'), 'wb'))
pickle.dump(item_rid, open(os.path.join(TPS_DIR, 'item_rid'), 'wb'))

usercount, itemcount = get_count(data, 'user_id'), get_count(data, 'item_id')

# print usercount
# print np.sort(np.array(usercount.values))
#
# print np.sort(np.array(itemcount.values))
