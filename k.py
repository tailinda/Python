import requests
from lxml import etree

if __name__ == '__main__':
	s = requests.session()
	url = input ('http://www.appledaily.com.tw/column/article/139/rnews/20151019/714285/')
	r = requests.get( url )
	tree = etree.HTML( r.text )
	target1 = tree.xpath('//*[@id="h1"]')
	target2 = tree.xpath('//*[@id="bcontent"]')
	print = ('主標題:' + target1)
	print = ('內文:' + target2)

