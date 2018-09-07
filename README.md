# MonaCoin Balance Watcher
![screenshot from 2018-09-07 16-55-55](https://user-images.githubusercontent.com/36693422/45206123-2db2f280-b2bf-11e8-840f-0272ee7dbcf8.png)

### Useage
以下のソースコードを参照
```#!/usr/bin/python
# -*- Coding: utf-8 -*-

from monacoin_balance_watcher import MonaCoinBalanceWatcher, WatchingStatusObject

if __name__ == '__main__':
	watching_status_object = WatchingStatusObject() #このオブジェクトを使って値の読み出しをスレッド外から行う
	mona_coin_balance_watcher = MonaCoinBalanceWatcher('sample_target_addresses.txt',watching_status_object,api_interval = 1.0)

	mona_coin_balance_watcher.setDaemon(True) #メインスレッドと一緒にkillするならTrue
	mona_coin_balance_watcher.start()

	from pprint import pprint
	#1秒ごとに監視結果を表示
	while True:
		time.sleep(1)
		pprint(watching_status_object.data)
```


### Requirements
 * requests

### Author
#####  https://twitter.com/GuriTech.com

