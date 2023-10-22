#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#
# @name   : Infoga - Email Information Gathering
# @url    : http://github.com/m4ll0k
# @author : Momo Outaadi (m4ll0k)

from json import loads
from lib.output import *
from lib.request import *
from lib.parser import *

class Pwned(Request):
	def __init__(self,email):
		Request.__init__(self)
		self.email = email

	def search(self):
		url = "https://api.haveibeenpwned.com/unifiedsearch/{email}".format(
			email=self.email.replace('@','%40'))
		try:
			resp = self.send(
				method = 'GET',
				url = url
				)
			if resp.status_code == 200:
				return loads(resp.content)
			return None
		except Exception as e:
			pass