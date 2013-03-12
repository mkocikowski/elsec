#!/bin/bash

# You can just copy the commands below and paste them into your shell command
# line. They will populate test indices which are used in the TUTORIAL.md
# file. 

curl -XDELETE 'http://localhost:9200/elsec_test_index_1'
curl -XDELETE 'http://localhost:9200/elsec_test_index_2'
curl -XPUT 'http://localhost:9200/elsec_test_index_1' -d '{"settings": {"index": {"number_of_replicas": 0, "number_of_shards": 1}}}'
curl -XPUT 'http://localhost:9200/elsec_test_index_2' -d '{"settings": {"index": {"number_of_replicas": 0, "number_of_shards": 1}}}'
curl -XPOST 'http://localhost:9200/_aliases/' -d '{"actions": [{ "add" : {"index": "elsec_test_index_1", "alias": "twitter" } }]}'
curl -XPUT 'http://localhost:9200/elsec_test_index_1/tweet/1' -d '{"user" : "kimchy", "post_date" : "2009-11-15T14:12:12", "message" : "trying out Elastic Search 1"}'
curl -XPUT 'http://localhost:9200/elsec_test_index_1/tweet/2' -d '{"user" : "elsec", "post_date" : "2010-11-15T14:12:12", "message" : "trying out Elastic Search 2"}'
curl -XPUT 'http://localhost:9200/elsec_test_index_1/tweet/3' -d '{"user" : "elsec", "post_date" : "2011-11-15T14:12:12", "message" : "trying out Elastic Search 3"}'
curl -XPUT 'http://localhost:9200/elsec_test_index_1/tweet/4' -d '{"user" : "elsec", "post_date" : "2012-11-15T14:12:12", "message" : "trying out Elastic Search 4"}'
curl -XPUT 'http://localhost:9200/elsec_test_index_1/tweet/5' -d '{"user" : "kimchy", "post_date" : "2013-11-15T14:12:12", "message" : "trying out Elastic Search 5"}'
curl -XPOST 'http://localhost:9200/elsec_test_index_1,elsec_test_index_2/_flush'