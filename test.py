import requests
from lxml import etree

if __name__ == '__main__':
	s = requests.session()
	#url = imput ('輸入蘋果日報網站')
	url = "http://www.appledaily.com.tw/column/article/139/rnews/20151019/714285/"
	r = requests.get( url )
	tree = etree.HTML( r.text )
	target1 = tree.xpath('//*[@id="h1"]')
	target2 = tree.xpath('//*[@id="bcontent"]')
	print ('主標題:' + target1[0].text)
	print ('內文:' + target2[0].xpath('string()'))	#先將原始碼叫出，再使用'string()'把裡面的br忽略掉，只取純文字
	
	i = target2[0].xpath('string()')
	len(i)

	if i > 20:		
		print('aaaa')


