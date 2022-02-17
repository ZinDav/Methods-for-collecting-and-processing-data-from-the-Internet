from pymongo import MongoClient

def find_item(self, uid):
    follower = self.mongobase['instagramcom']
    following = self.mongobase['instagramcom']
    for f in follower.find({'main_user_id': uid}):
        pprint(f)
    for f in following.find({'main_user_id': uid}):
        pprint(f)
