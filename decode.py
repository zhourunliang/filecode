import os
import re
import base64
import config

decodeList = []

def getAllFile(path, fileList=[]):
    get_dir = os.listdir(path)  #遍历当前目录，获取文件列表
    for i in get_dir:
        sub_dir = os.path.join(path,i)  # 把第一步获取的文件加入路径
        # print(sub_dir)
        if os.path.isdir(sub_dir):     #如果当前仍然是文件夹，递归调用
            getAllFile(sub_dir, fileList)
        else:
            ax = os.path.abspath(sub_dir)  #如果当前路径不是文件夹，则把文件名放入列表
            # print(ax)
            fileList.append(ax)
    return fileList


def getAllDir(path, dirList=[]):
    get_dir = os.listdir(path)  #遍历当前目录，获取文件列表
    for i in get_dir:
        sub_dir = os.path.join(path,i)        # 把第一步获取的文件加入路径
        if os.path.isdir(sub_dir):     #如果当前仍然是文件夹，递归调用并加入列表
            ax = os.path.abspath(sub_dir)
            dirList.append(ax)
            getAllDir(sub_dir, dirList)
        else:
            continue
    return dirList

def encode(path):
    basename = os.path.basename(path)
    # print(basename)
    dirname = os.path.dirname(path)
    # print(dirname)
    new_name = base64.urlsafe_b64encode(basename.encode(encoding="utf-8")).decode()
    # print(new_name)
    old_dir = path
    # print(old_dir)
    new_dir = os.path.join(dirname,str(new_name))
    # print(new_dir)
    os.rename(old_dir,new_dir)

def decode(path):
    basename = os.path.basename(path)
    # print(basename)
    dirname = os.path.dirname(path)
    # print(dirname)
    new_name = base64.urlsafe_b64decode(basename).decode()
    # print(new_name)
    old_dir = path
    # print(old_dir)
    new_dir = os.path.join(dirname,str(new_name))
    # print(new_dir)
    try:
        os.rename(old_dir,new_dir)
        decodeList.append(new_dir)
    except BaseException as e:
        print('异常 {}'.format(e))
        # 回滚
        print(decodeList)
        rollBack()
        return False

def rollBack():
    decodeList.sort(key = lambda i:len(i),reverse=True) 
    for i in decodeList:
        encode(i)
    with open(config.path+'/lock', "wb") as code:
        code.write('is lock'.encode('utf-8'))
    print('回滚完成')


def main():
    fileList = []
    dirList = []
    path = config.path

    if os.path.exists(path+'/lock'):
        os.remove(path+'/lock')
        allDirList = getAllDir(path, dirList)
        allDirList.sort(key = lambda i:len(i),reverse=True) 
        # print(allDirList)
        for i in allDirList:
            r = decode(i)
            if r is False:
                return False

        allFileList = getAllFile(path, fileList)
        allFileList.sort(key = lambda i:len(i),reverse=True) 
        # print(allFileList)
        for i in allFileList:
            r = decode(i)
            if r is False:
                return False
        print('解码完成')
    else:
        print('已解码')

if __name__ == '__main__':
    main()

