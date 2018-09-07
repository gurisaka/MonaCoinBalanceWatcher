#!/usr/bin/python
# -*- Coding: utf-8 -*-

import time
import requests
import sys
import json
from threading import Thread

class MonaCoinBalanceWatcher(Thread):
	def __init__(self, addresses_list_file_path, watching_status_object,api_interval = 1.0):
		super(MonaCoinBalanceWatcher,self).__init__()
		self.__target_addresses = MonaCoinBalanceWatcher.__load_target_addresses(addresses_list_file_path)
		self.__previous_time_balance_list = {}
		self.__init_fetch_addresses_info()
		self.watching_status_object = watching_status_object
		self.__API_INTERVAL = api_interval

	def __init_fetch_addresses_info(self):
		for target_address in self.__target_addresses:
			target_address_info = MonaCoinBalanceWatcher.__fetch_address_info(target_address)
			if target_address_info == {}:
				continue
			self.__previous_time_balance_list[target_address] = target_address_info['balance']

	@classmethod
	def __load_target_addresses(cls, addresses_list_file_path):
		addresses = []

		with open(addresses_list_file_path, 'r') as file:
			addresses = file.read().split('\n')
			if addresses[-1] == '':
				addresses = addresses[:-1]

		return addresses

	@classmethod
	def __fetch_address_info(cls, target_address):
		api_url = 'https://mona.chainsight.info/api/addr/' + target_address + ''
		response = requests.get(api_url)

		if response.status_code != 200:
			sys.stderr.write('API Requests Failed : https://mona.chainsight.info/api/addr/' + target_address + ' @status code:' + str(response.status_code))
			print('API Requests Failed : https://mona.chainsight.info/api/addr/' + target_address + ' @status code:' + str(response.status_code))

			return {}

		return json.loads(response.text)

	@classmethod
	def __compare_now_and_previous_balance(cls, target_address, previous_time_balance):
		target_address_info = MonaCoinBalanceWatcher.__fetch_address_info(target_address)

		if len(target_address_info.keys()) == 0:
			return False

		if float(target_address_info['balance']) != float(previous_time_balance):
			return True

		return False

	def run(self):
		while True:
			for target_address in self.__target_addresses:
				previous_time_balance = self.__previous_time_balance_list[target_address]
				self.watching_status_object.data[target_address] = MonaCoinBalanceWatcher.__compare_now_and_previous_balance(target_address,previous_time_balance)
				time.sleep(self.__API_INTERVAL)
				self.watching_status_object.data['time'] = time.time()

class WatchingStatusObject(object):
	def __init__(self):
		self.data = {}