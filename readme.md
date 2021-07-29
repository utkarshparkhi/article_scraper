#Article Scraper

###Setting Up
add db configuration in file `constant/DB_CONFIG.py`
```python
review_client = pymongo.MongoClient("DB_PATH")
review_db = review_client["DB_NAME"]
review_col = review_db["COLLECTION_NAME"]
```

add custom search configuration in file `constant/custom_search.py`
```python
API_KEY = "CUSTOM SEARCH API KEY"
SEARCH_ID = "SEARCH ENGINE ID"
```

###Running the Crawler
1) open python console and run the following
   ```python
    import run_crawler
    run_rawler.add_queries(["PRODUCT_1","PRODUCT_2"])
    ```
2) run the following command in terminal<br>
    `scrapy crawl {spider_name} -a product="product_name"`<br>
   spider name can be `GSM`,`ndtv`and `verge`