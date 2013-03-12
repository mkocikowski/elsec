Intro
-----
This is a tutorial on basic use of the tool. For installation instructions see
the "README.md" file in the main project directory. 

The goal of the project is to provide an easy to use, interactive command line
(terminal) client to Elasticsearch, with behavior similar to 'mysql' or 'psql'
clients. The tool is to give a safe (read-only) way to explore data in ES
indices, addressing use cases common among non-technical, non-administrator
users. Anyone capable of using the mysql client to dig around a mysql database
should be able to use the 'elsec' to look at data in an ES index.

Preparation
-----------
This tutorial uses an Elasticserach (version >= 0.19.9) instance running on
localhost. Setup commands are in the "tutorial.sh" file in the main
project directory, just copy and paste them in your terminal. This will create
2 indices, an alias, and put 5 documents into the index. 

Start
-----
First, check if 'elsec' is installed correctly, and the you have the version
you expect, by typing 'elsec -v' on the command line. This is what your
terminal window should look like: 

    bash:$ elsec -v
    0.9.1
    bash:$ 

You get basic help with:

    bash:$ elsec -h

Time to get started! You have the Elasticsearch server running on localhost on port 9200: 

    bash:$ elsec localhost:9200 
    Indices: [u'elsec_test_index_1', u'elsec_test_index_2'], aliases: [u'twitter']
    bash:$

This shows you what you can connect to. Connect to 'twitter': 

    bash:$ elsec localhost:9200 twitter
    Type 'help' for help. Exit with Control-D. 
    localhost:9200/twitter/> 

Now you are running the client. The prompt 'localhost:9200/twitter/>' shows
you what you are connected to. You can exit the client at any time with
Control-D. Pressing the 'TAB' key twice will show you the list of commands:

    localhost:9200/twitter/> 
    exit      help      open      search    version   view      count     
    localhost:9200/twitter/>

The two most important commands are 'search' and 'count'. They take [Lucene
queries](http://lucene.apache.org/core/old_versioned_docs/versions/2_9_1/queryparsersyntax.html) 
as their input. Type in 'sea' and press 'TAB' once - the command will be
completed to 'search '. Now you can press 'TAB' twice more, and you will see
the list of fields in the index. This is the basic way for exploring and
index, for finding out what fields are there: 

    localhost:9200/twitter/> search tweet.
    tweet.post_date  tweet.user       tweet.message    
    localhost:9200/twitter/> search tweet.

Now complete the query, ending the line with ";" and hit enter:

    localhost:9200/twitter/> search tweet.user:kimchy;
    curl -XPOST 'http://localhost:9200/twitter/_search' -d '{
        "fields": [
            "_id"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }'
    >
    {
        "_shards": {
            "failed": 0, 
            "successful": 2, 
            "total": 2
        }, 
        "hits": {
            "hits": [
                {
                    "_id": "1", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet"
                }, 
                {
                    "_id": "5", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet"
                }
            ], 
            "max_score": 1.5108256, 
            "total": 2
        }, 
        "timed_out": false, 
        "took": 62
    }
    localhost:9200/twitter/> 

What you see here is key to using 'elsec'. The first part is the call which is made to the Elasticsearch server: 

    curl -XPOST 'http://localhost:9200/twitter/_search' -d '{
        "fields": [
            "_id"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }'

The purpose of displaying this call is so that you can share it with others,
and so that you can modify it to build more complex queries. You can copy that
call, and execute it straight from the command line (open a separate terminal
window first): 

    bash:$ curl -XPOST 'http://localhost:9200/twitter/_search' -d '{
    >     "fields": [
    >         "_id"
    >     ], 
    >     "from": 0, 
    >     "query": {
    >         "query_string": {
    >             "default_field": "_all", 
    >             "query": "tweet.user:kimchy"
    >         }
    >     }, 
    >     "size": 10
    > }'
    {"took":2,"timed_out":false,"_shards":{"total":2,"successful":2,"failed":0},"hits":{"total":2,"max_score":1.5108256,"hits":[{"_index":"elsec_test_index_1","_type":"tweet","_id":"1","_score":1.5108256},{"_index":"elsec_test_index_1","_type":"tweet","_id":"5","_score":1.5108256}]}}bash:$ 

You can also take the request body, which is this part: 

    {
        "fields": [
            "_id"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }

and modify it, and paste it into Elasticsearch HEAD, or back into elsec. For
example, if you want to show 'message' field along with the '_id' field of
results, modify the request to read (note the "message" element in the
"fields" list): 

    {
        "fields": [
            "_id", 
            "message"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }

In elsec, type 'search' and paste the above request, followed by ";" and hit enter:

    localhost:9200/twitter/> search {
    >     "fields": [
    >         "_id", 
    >         "message"
    >     ], 
    >     "from": 0, 
    >     "query": {
    >         "query_string": {
    >             "default_field": "_all", 
    >             "query": "tweet.user:kimchy"
    >         }
    >     }, 
    >     "size": 10
    > };
    curl -XPOST 'http://localhost:9200/twitter/_search' -d '{
        "fields": [
            "_id", 
            "message"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }'
    >
    {
        "_shards": {
            "failed": 0, 
            "successful": 2, 
            "total": 2
        }, 
        "hits": {
            "hits": [
                {
                    "_id": "1", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet", 
                    "fields": {
                        "message": "trying out Elastic Search 1"
                    }
                }, 
                {
                    "_id": "5", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet", 
                    "fields": {
                        "message": "trying out Elastic Search 5"
                    }
                }
            ], 
            "max_score": 1.5108256, 
            "total": 2
        }, 
        "timed_out": false, 
        "took": 3
    }
    localhost:9200/twitter/> 

In example above, you modified the 'fields' element of the request. However,
you may pass any valid Elasticsearch request to 'search' and 'count'
functions. Elsec does not help you in building complex requests because it is
a tool for exploring: geting to know the structure of the index, for seeing
how many documents are there that match certain criteria, and for having a
look at a sample set of these. 

You can view any document with the 'view' command, passing it the id of the document: 

    localhost:9200/twitter/> view 1
    http://localhost:9200/twitter/tweet/1
    curl -XGET 'http://localhost:9200/twitter/tweet/1'
    >
    {
        "_id": "1", 
        "_index": "elsec_test_index_1", 
        "_source": {
            "message": "trying out Elastic Search 1", 
            "post_date": "2009-11-15T14:12:12", 
            "user": "kimchy"
        }, 
        "_type": "tweet", 
        "_version": 1, 
        "exists": true
    }
    localhost:9200/twitter/> 

Again, you see the curl call first, and then the response. You can also use
the 'open' command, which will try to display the document in your web browser
(may or may not work).


Editing
-------
If you are comfortable using the VIM text editor, there is an 'easier'
(relative to previous statement) way to modify your queries. Elsec always
'remembers' the previous request, and you can edit that request and execute
the modified request with the 'edit' command. Let's get a fresh start: 

    localhost:9200/twitter/> search tweet.user:kimchy;

The command above will execute a search (I'm omitting the response here), and
'elsec' will remember that request. Now if you type just 'search' and hit
enter, that request will be executed again (you could also do 'count'):

    localhost:9200/twitter/> search 
    curl -XPOST 'http://localhost:9200/twitter/_search' -d '{
        "fields": [
            "_id"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }'
    >
    {
        "_shards": {
            "failed": 0, 
            "successful": 1, 
            "total": 1
        }, 
        "hits": {
            "hits": [
                {
                    "_id": "1", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet"
                }, 
                {
                    "_id": "5", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet"
                }
            ], 
            "max_score": 1.5108256, 
            "total": 2
        }, 
        "timed_out": false, 
        "took": 1
    }
    localhost:9200/twitter/> 

To modify the request, and to run the modified request, do 'edit'. I will not
show the screen shots here, but the 'edit' command will open vim, with the
request body open for editing. The file on which you will be modifying is
called "/tmp/elsec"; the content of that file is what will get passed on as
the body of the request when VIM exits. This means that you can edit the file,
hit 'ZZ', and be done with it. But with a bit of VIM magic you can use
template files, autocomplete, all kinds of magic: but this is up to you and
your mad VIM skillz. 

Let's just say I'll do edit and add the 'message' field to the response (I'm
not showing the VIM session between the 'edit' command and the response). This
is just like the 'copy and paste' example in the section above, but without
having to do the 'copy and paste':

    localhost:9200/twitter/> edit
    curl -XPOST 'http://localhost:9200/twitter/_search' -d '{
        "fields": [
            "_id", 
            "message"
        ], 
        "from": 0, 
        "query": {
            "query_string": {
                "default_field": "_all", 
                "query": "tweet.user:kimchy"
            }
        }, 
        "size": 10
    }'
    >
    {
        "_shards": {
            "failed": 0, 
            "successful": 1, 
            "total": 1
        }, 
        "hits": {
            "hits": [
                {
                    "_id": "1", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet", 
                    "fields": {
                        "message": "trying out Elastic Search 1"
                    }
                }, 
                {
                    "_id": "5", 
                    "_index": "elsec_test_index_1", 
                    "_score": 1.5108256, 
                    "_type": "tweet", 
                    "fields": {
                        "message": "trying out Elastic Search 5"
                    }
                }
            ], 
            "max_score": 1.5108256, 
            "total": 2
        }, 
        "timed_out": false, 
        "took": 1
    }
    localhost:9200/twitter/> 

When you exit 'elsec', the 'current' request gets saved to '~/.elsec_request',
so when you start 'elsec' again, you can go with 'search' or 'edit' straight
away. 

Future
------
We'll be working on a graphical query builder. 
