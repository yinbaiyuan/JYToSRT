#!/usr/bin/env python3

import json
import os

def readFile(fileName = ''):
	f = open(fileName)
	str = f.read()
	f.close()
	return str

def writeFile(fileName = '',fileStr = ''):
	f = open(fileName, "w")
	f.write(fileStr)
	f.close()

def analyseFile(jsonStr = ''):
	json_obj = json.loads(jsonStr)
	texts = json_obj['materials']['texts']
	tracks = json_obj['tracks']
	subtitleDic = {}
	for textInfo in texts:
		tKey = textInfo['id']
		tValue = {'content':textInfo['content']}
		subtitleDic[tKey] = tValue
	for trackInfo in tracks:
		segments = trackInfo['segments']
		for segment in segments:
			mId = segment['material_id']
			if mId in subtitleDic.keys():
				subtitleInfo = subtitleDic[mId]
				subtitleInfo['start'] = segment['target_timerange']['start']
				subtitleInfo['duration'] = segment['target_timerange']['duration']
				subtitleDic[mId] = subtitleInfo
	subtitleDic = sorted(subtitleDic.items(), key = lambda x:x[1]['start'],reverse=False)
	return subtitleDic

def msToTimeStr(t = 0):
	res = ''
	ms = t % 1000
	sec = t // 1000 % 60
	min = t // 1000 // 60 % 60
	hour = t // 1000 // 60 // 60
	res += "%02d" % hour + ':' + "%02d" % min + ':' + "%02d" % sec + ',' + "%03d" % ms
	return res
	
def createSrt(subtitleDic = {}):
	srtStr = ''
	subtitleCount = 1
	for subtitle in subtitleDic:
		srtStr += str(subtitleCount)
		srtStr += '\n'
		subtitleCount += 1
		startTimeStr = msToTimeStr(subtitle[1]['start'])
		endTimeStr = msToTimeStr(subtitle[1]['start'] + subtitle[1]['duration'])
		srtStr += startTimeStr + ' --> ' + endTimeStr
		srtStr += '\n'
		srtStr += subtitle[1]['content']
		srtStr += '\n' 
		srtStr += '\n'
	return srtStr

def createTxt(subtitleDic = {}):
	txtStr = ''
	for subtitle in subtitleDic:
		txtStr += subtitle[1]['content']
		txtStr += '\n'
	return txtStr


def createTitle(subtitleDic = {}):
	title = ''
	titleLength = 0
	for subtitle in subtitleDic:
		title += subtitle[1]['content'] + ' '
		if len(title)>20:
			break
	return title

def findTemplates():
	rootFolder = os.path.expanduser('~') + '/Movies/JianyingPro/videocut/'
	result = []
	if not os.path.exists(rootFolder):
		return result
	for folder in os.listdir(rootFolder):
		tFile = rootFolder + folder + '/template.json'
		if os.path.exists(tFile):
			result.append(tFile)
	return result
		

def main():
	templates = findTemplates()
	if len(templates) == 0:
		print('未找到可处理的字幕文件')
		return
	titleList = []
	subtitleDicList = []
	for template in templates:
		jsonStr = readFile(template)
		subtitleDic = analyseFile(jsonStr)
		title = createTitle(subtitleDic)
		if len(title)>0:
			titleList.append(title)
			subtitleDicList.append(subtitleDic)
	subtitleCount = len(titleList)
	if subtitleCount > 0 :
		print('共找到'+str(len(titleList))+'个字幕文件，分别为：')
	else:
		print('未找到可处理的字幕文件')
		return
	
	titleIndex = 1
	for title in titleList:
		print(str(titleIndex) + ' ' + title)
		titleIndex += 1
	
	inputTitleIndex = input("请输入需要导出的字幕序号:") #B站用户UID
	inputTitleIndex = int(inputTitleIndex)
	if inputTitleIndex <= 0 or inputTitleIndex > subtitleCount :
		print('序号输入错误，程序结束')
		return
	print(inputTitleIndex)
	subtitleDic = subtitleDicList[inputTitleIndex]
	subtitleStr = createSrt(subtitleDic)
	subtitleTxt = createTxt(subtitleDic)
	
	inputTitle = input("请输入导出文件名:")
	exportFolder = os.path.expanduser('~') + '/Desktop/'
	srtTitle = exportFolder + str(inputTitle) + '.srt'
	txtTitle = exportFolder + str(inputTitle) + '.txt'
	print('saved ' + srtTitle)
	writeFile(srtTitle,subtitleStr)
	print('saved ' + txtTitle)
	writeFile(txtTitle,subtitleTxt)
	
if __name__=="__main__":
	main()