import sys
import os
import time


from rakuten_seller.sheet_handler.consts import *


import gspread
from oauth2client.service_account import ServiceAccountCredentials

current_path = os.path.abspath(os.getcwd())

class SheetHandler(object):
	def __init__(
		self,
		sheet_name,
		config_folder = "./config/",
		config_files = ["client_secret.json"]
		):
		# use creds to create a client to interact with the Google Drive API
		self.scope = [
		"https://spreadsheets.google.com/feeds", 
		"https://www.googleapis.com/auth/spreadsheets",
		"https://www.googleapis.com/auth/drive.file", 
		"https://www.googleapis.com/auth/drive"
		]
		
		
		self.current_config_file = -1
		self.config_folder = config_folder
		self.config_files = config_files
		self.sheet_name = sheet_name

		self._getCredentials()
		self._authorize()
		self.config_files_tries = 0

	def _getCredentials(self):
		#wait 5 secs between each cred use
		time.sleep(5)
		
		if(self.current_config_file == len(self.config_files) - 1):
			self.current_config_file = 0
		else:
			self.current_config_file += 1
		config_file = self.config_folder + self.config_files[self.current_config_file]
		message = "Using {} credentials files".format(config_file) 
		print(message)
		self.creds = ServiceAccountCredentials.from_json_keyfile_name(config_file, self.scope)
	
	def _authorize(self):
		try:
			self.client = gspread.authorize(self.creds)
		except Exception as e:
			message = "couldn't _authorize connection ,APIError {}".format(e) 
			print(message)

	def _connectToSheet(self, sheet_number):
		try:
			print("connecting to {} , sheet number {}".format(self.sheet_name, sheet_number))
			self.sheet = self.client.open(self.sheet_name).get_worksheet(sheet_number)
		except Exception as e:
			message = "couldn't open sheet number {} in {} ,APIError : {}".format(sheet_number, self.sheet_name, e)
			print(message)

	def _nextConfigFile(self):
		message = "trying next config file"
		print(message)
		self.config_files_tries += 1
		self._getCredentials()
		self._authorize()

	def writeToSheet(self, sheet_number, data):
		self._connectToSheet(sheet_number)
		new_entry = data
		row_index = self.sheet.row_count		
		message = "new_entry :{}, row_index: {}".format(new_entry, row_index)
		print(message)		
		try:
			self.sheet.insert_row(new_entry, row_index)
			self.config_files_tries = 0
			return True
		except Exception as e:
			message = "couldn't write new_entry :{}, row_index: {} to file, APIError: {}".format(new_entry, row_index,e) 
			print(message)
			if(self.config_files_tries == len(self.config_files)):
				message = "tried all config files"
				print(message)
				return False
			else:
				message = "trying next config file"
				self._nextConfigFile()
				result = self.writeToSheet(sheet_number, *args)
			return result