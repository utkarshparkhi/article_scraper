#Article Scraper

###Setting Up
1. add db configuration in file `constant/DB_CONFIG.py`
```python
review_client = pymongo.MongoClient("DB_PATH")
review_db = review_client["DB_NAME"]
review_col = review_db["COLLECTION_NAME"]
```

2. add custom search configuration in file `constant/custom_search.py`
```python
API_KEY = "CUSTOM SEARCH API KEY"
SEARCH_ID = "SEARCH ENGINE ID"
```

3. install dependencies<br>
   `pip install -r article_scraper/requirements.txt`

###Running the Crawler
1) open python console and run the following
   ```python
    import run_crawler
    run_rawler.add_queries(["PRODUCT_1","PRODUCT_2"])
    ```
2) run the following command in terminal<br>
    `scrapy crawl {spider_name} -a product="product_name"`<br>
   spider name can be `GSM`,`ndtv`and `verge`