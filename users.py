from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['instagram']
instagram = db.instagram


def following():
    user = input("Input user name:")
    result = instagram.find({'$and': [{"user": user}, {'user_status': 'following'}]},
                            {'user': False, 'user_status': False, '_id': False})
    for user in result:
        pprint(user)


def follower():
    user = input("Input user name:")
    result = instagram.find({'$and': [{"user": user}, {'user_status': 'follower'}]},
                            {'user': False, 'user_status': False, '_id': False})
    for user in result:
        pprint(user)


if __name__ == '__main__':
    following()
    follower()
