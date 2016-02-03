import requests
from lxml import etree

if __name__ == '__main__':
	s = requests.session()
	b = 1
	
	url = "http://www.appledaily.com.tw/column/article/139/rnews/20151019/714285/"
	r = requests.get( url )
	tree = etree.HTML( r.text )
	target1 = tree.xpath('//*[@id="h1"]')
	target2 = tree.xpath('//*[@id="bcontent"]')
	print ('主標題:' + target1[0].text)

	i = target2[0].xpath('string()')

	for a in i:	#將文字一個一個叫出
		b += 1	#累加
		print('%s' %a, end = "")	#結束字元為空格
		if (b > 25) :	
			print()
			b = 1

	#print ('內文:' + target2[0].xpath('string()'))	#先將原始碼叫出，再使用'string()'把裡面的br忽略掉，只取純文字

#ctrl+? = 所框起的註解，或移除註解