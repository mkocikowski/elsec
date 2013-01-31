# -*- coding: utf-8 -*-

REQUEST = {
    "query": None, 
    "fields": ['_id'], 
    "from": 0, 
    "size": 10, 
}

QQS = {
    "query_string": {
        "query": None,
        "default_field": "_all", 
#         "default_operator": "OR", 
#         "analyzer": "standard", 
#         "allow_leading_wildcard": True, 
#         "lowercase_expanded_terms": True, 
#         "enable_position_increments": True, 
#         "fuzzy_prefix_length": 0, 
#         "fuzzy_min_sim": 0.5, 
#         "phrase_slop": 0, 
#         "boost": 1.0, 
#         "analyze_wildcard": True, 
#         "auto_generate_phrase_queries": False, 
#         "minimum_should_match": "20%", 
#         "lenient": True, 
    }
}
