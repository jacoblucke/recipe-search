# recipe-search
Uses python to webscrape recipe data, and libcurl to POST the data to Elasticsearch

Recipe sites currently supported:
allrecipes.com

mappings5.json - json file used to create the Elasticsearch index with the appropriate mappings for how the data is webscraped

scrape.py - either accepts manually input data or webscrapes, and then POSTs data to Elasticsearch using ./esJson
  run: python scrape.py

elasticsearchJson.cpp - uses libcurl to either PUT or POST to Elasticsearch
  compile: g++ elasticsearchJson.cpp -lcurl -o esJson
