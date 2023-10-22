#!/usr/bin/env python
# -*- coding:utf-8 -*- 
#
# @name   : Infoga - Email Information Gathering
# @url    : http://github.com/m4ll0k
# @author : Momo Outaadi (m4ll0k)

from lib.output import *
from lib.request import *
from lib.parser import *

class Google(Request):
	def __init__(self,target):
		Request.__init__(self)
		self.target = target

	def search(self):
		test('Searching "%s" in Google...'%(self.target))
		base_url = 'https://www.google.com/search?q=intext:%22%40{target}%22&num=50'.format(
			target=self.target)
		mails = []
		# First 350 results (page 0 to 6)
		for page in range(0, 7):
			url = base_url + "&start=" + str(page)
			try:
				resp = self.send(
					method = 'GET',
					url = url
					)
				if "detected unusual traffic" in resp.text:
					break
				for email in self.getemail(resp.content,self.target):
					if email not in mails:
						mails.append(email)
			except:
				pass
		return mails

	def getemail(self,content,target):
		return parser(content,target).email()
