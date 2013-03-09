#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import urllib2
from MLStripper import remove_tags
from datetime import date
from PlurkAPI import PlurkAPI

key_file = open("config.json", "r")
key = json.load(key_file)
key_file.close()

def get_quote_from_wikiquote():
	
	wikiapi = "http://%s.wikiquote.org/w/api.php?format=%s&action=%s&page=%s"
	today = date.today()
	
	request = urllib2.urlopen(wikiapi % 
				(
					"zh",
					"json",
					"parse",
					"Wikiquote:每日名言/%s月%s日" % (today.month, today.day)
				),
				timeout = 80)
	data = request.read()
	data = json.loads(data)
	data = remove_tags(data["parse"]["text"]["*"])
	data = data[:-6]

	return data + "\n\nvia Wikiquote"

if __name__ == "__main__":
	data = get_quote_from_wikiquote()

	plurk = PlurkAPI(key["APP_KEY"], key["APP_SECRET"])
	plurk.authorize(key["ACCESS_TOKEN"], key["ACCESS_TOKEN_SECRET"])

	plurk.callAPI("/APP/Timeline/plurkAdd", {'content' : data.encode("UTF-8"), 'qualifier' : ':'})
