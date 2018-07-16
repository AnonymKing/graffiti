# -*- coding: utf-8 -*-
# @Author: KING
# @Date:   2017-12-31 22:01:16
# @Last Modified by:   KING
# @Last Modified time: 2018-04-29 12:08:34

import os
choice = -1

def name_init(iterms, path):
	k = 1
	for i in iterms:
		j = "__@1314_@#$$@#@#__%s"%str(k) + i[i.rfind('.'):]
		os.rename(os.path.join(path,i),os.path.join(path,j))
		k += 1
	
def way_num(iterms, path):
	try:
		k = int(input('请输入起始值: '))
	except:
		print('输入错误，默认起始值为 1')
		k = 1
	for i in iterms:
		try:
			j = "%s"%str(k) + i[i.rfind('.'):]
			os.rename(os.path.join(path,i),os.path.join(path,j))
		except:
			pass
		finally:
			k += 1

def way_headnum(iterms, path):
	try:
		k = int(input('请输入起始值: '))
	except:
		print('输入错误，默认起始值为 1')
		k = 1
	for i in iterms:
		try:
			j = "%s"%str(k) + "、" + str(i)
			os.rename(os.path.join(path,i),os.path.join(path,j))
		except:
			pass
		finally:
			k += 1
		
def way_replace(iterms, path):
	string = str(input('输入要被删除的字符串: '))
	for i in iterms:
		j = i.replace(string, "", 1)
		os.rename(os.path.join(path,i),os.path.join(path,j))


def way_add(iterms, path):
	string = str(input('输入要追加字符串: '))
	for i in iterms:
		dot = i.rfind('.')
		j = i[:dot+1] + string + i[dot:]
		os.rename(os.path.join(path,i),os.path.join(path,j))


def getChoice():
	global choice
	try:
		choice = int(input('请输入批量重命名方式: '))
	except :
		print("Error ", end="")
		getChoice()

		
def choose_way():
	user = str(os.environ["TEMP"].split("\\")[2])
	print("\n=====欢迎您，亲爱的 %s ====="%user)
	print("  1、纯数字批量命名")
	print("  2、去除重复字符串")
	print("  3、末尾追加字符串")
	print("  4、文件头添加数字")
	print("==============================")
	
	choice = getChoice()
	return choice
	
# 以文件创建时间为序
def getFileList(path):
	iterms = os.listdir(path)
	iterms = sorted(iterms, key=lambda x:(os.stat(path + "/" + x).st_ctime))
	
	return iterms


def getPath():
	# path = 'E:\\IDM_Download\\Video\\temp'
	path = str(input('文件夹位置：'))
	while os.path.isdir(path) == False:
		print('文件夹路径错误，请检查！')
		path = str(input('文件夹位置：'))
	
	return path
		
	
	
def main():
	path = getPath()
	print(path)
	global choice
	choose_way()
	print(choice)
	if choice == 1:
		name_init(getFileList(path), path)
		way_num(getFileList(path), path)
	elif choice == 2:
		way_replace(getFileList(path), path)
	elif choice == 3:
		way_add(getFileList(path), path)
	elif choice == 4:
		way_headnum(getFileList(path), path)
	else:
		print('亲，指令无法解析...')
	

if __name__ == '__main__':
	main()
