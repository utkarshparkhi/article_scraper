from article_scraper.constant import DB_CONFIG


def dump_data(article, url, **kwargs):
    data = {"url": url, "text": article, "processed": False}
    data.update(kwargs)
    if DB_CONFIG.review_col.find_one({"url": url}) is None:
        x = DB_CONFIG.review_col.insert_one(data)
        return x
    else:
        ex_data = DB_CONFIG.review_col.find_one({"url": url})
        if 'queries' in ex_data.keys():
            data['queries'] = list(set(data['queries'] + ex_data['queries']))
        x = DB_CONFIG.review_col.update_many({"url": url}, {"$set": data})
        return x
