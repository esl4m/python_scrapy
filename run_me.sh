#!/bin/bash

# --- Crawl the login page --- #
scrapy crawl login -o upwork_login.jl

# --- Crawl the home page --- #
scrapy crawl upwork -o upwork_data.jl
