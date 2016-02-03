import json

open_file = open('camera.json','r',encoding='utf-8')	#將檔案讀取成字串
s = open_file.read()
print(s)
open_file.close()

project = json.loads(s)

user_input = input ('請輸入所要查詢的路名')
user_input = user_input.replace('路','')
user_input = user_input.replace('口','')

print('行政區\t測照方向\t\t測照地點')	#\t代表縮排
print('='*50)
for a in project:
	if user_input in a ['測照地點']:
		print( '%s\t%s\t\t%s'%(a['行政區'],a['測照方向'],a['測照地點'] ))