import json
# from run_crawler import add_queries


def read_models(filename):
    f = open(filename, 'r')
    data = f.read()
    data = data.split('\n')
    clubbed_d = []
    print(len(data))
    for i in range(0, len(data), 2):
        intent = data[i + 1].strip('\t').split('\t')
        store_path = intent[0]
        facets = json.loads(intent[1])

        clubbed_d.append({"query": data[i], "store": store_path, "facets": facets})
    return clubbed_d


def get_queries_model_name(queries):
    qmn = []
    for query in queries:
        if query['store'] != "tyy/4io":
            continue
        model_name = False
        brand_name = False
        for facet in query['facets']:
            if facet['fk'] == 'model_name':
                model_name = facet['fv']

            if facet['fk'] == 'brand':
                brand_name = facet['fv']
        if model_name:
            qmn.append({"query": query['query'], "model": model_name, })
            if brand_name:
                qmn[-1].update({"brand": brand_name})
    return qmn


def get_queries(qmn):
    queries = []
    products = []
    for q in qmn:
        if 'brand' in q.keys():
            queries.append([q['query'], " ".join([q['brand'], q['model']])])
            products.append(" ".join([q['brand'], q['model']]))
        else:
            queries.append([q['query'], q['model']])
            products.append(q['model'])

    products = set(products)
    qdict = dict(zip(products, [set() for i in range(len(products))]))
    for q in queries:
        qdict[q[1]].add(q[0])
        qdict[q[1]].add(q[1])
    return list(products), qdict


queries_intent = read_models("mobile_intent_queries.txt")
processed_queries = get_queries_model_name(queries_intent)
products, qdict = get_queries(processed_queries)
# add_queries(products[0:10], qdict)
