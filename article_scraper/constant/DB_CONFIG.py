import pymongo
review_client = pymongo.MongoClient("mongodb://localhost:27018/")
review_db = review_client["review_db"]
review_col = review_db["reviews"]
