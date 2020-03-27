# -*- coding: utf-8 -*-
from PIL import Image, ImageGrab
# import Image
import os
# 图片资源copy库 
import shutil
import  zlib
# 图片资源 压缩库
import tinify

# https://tinypng.com/developers 申请key网站
# 这个是tinify 的秘钥 (  每个邮箱可以申请一个 申请蛮快 2分钟就可以拿到)
tinify.key = 'K05B1h8L5QY58BDd2pTYbRz5StjfpnMc'

# 当前的脚本的目录, 如果使用需要改为自己存放脚本的父级目录
pathCurrent =  '/Users/apple/Desktop/Category/image' 
# 内存和图片面积的比值设定

# 这个是脚本对图片压缩之后存放压缩后的图片的目录 
dstPath = '/Users/apple/Desktop/Category/newImage'


# 查找内存图片比某个大于多少kb 
# 找出没有压缩的图片
# 找出某个图片所占用的内存比例


neicunofSizeRateMax = 0.2;
neicunofSizeRateTooMax = 0.05;
errorAtt = []
# 单位是kb
neicunofMax = 20
allNeiCun = 0
alleNeiCunBigThan = 0
imageNum = 0
bigImageNum = 0
imageRateTooBig = 0

# 查找比例不正确的图片
def findneicunSizeRate(path):
    global imageRateTooBig
    for root, dirs, files in os.walk(path):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        # print(files)
        # 找到所有的文件
        for file in files:
            if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('gif') or file.endswith(
                    'png') or file.endswith('bmp'):
            # if file.endswith('jpeg') or file.endswith('gif') or file.endswith('png') or file.endswith('bmp'):
                fileObj = root + '/' + file
                try:
                    im = Image.open(fileObj)
                except IOError:
                    errorAtt.append(fileObj)
                else:
                    imageW = im.size[0]
                    imageH = im.size[1]
                    imagWH = imageW * imageH
                    # 图片的byte 数
                    n = os.path.getsize(fileObj)
                    # 图片的kb 数量
                    nOfKb = n / 1024.00
                    # allNeiCun
                    # 内存和图片面积的比值
                    imageSizeN = n * 1.0 / imagWH
                    # 内存和图片面积的比值
                    imageSizeN = n * 1.0 / imagWH
                    if imageSizeN > neicunofSizeRateMax:
                    
                        imageRateTooBig += 1
                        print("图片的内存和面积比值 %.2f 宽度%.1f 高度%.1f 内存大小 %f.2 kb  片名称:%s   " % (imageSizeN,imageW,imageH,nOfKb, fileObj))


# 找到内存过大的图片
def findneicunIsBig(path):
    global allNeiCun
    global alleNeiCunBigThan
    global errorAtt
    global  imageNum
    global bigImageNum

    for root, dirs, files in os.walk(path):
        # print(root) #当前目录路径
        # print(dirs) #当前路径下所有子目录
        # print(files)
        # 找到所有的文件
        for file in files:
             if file.endswith('jpg') or file.endswith('jpeg') or file.endswith('gif') or file.endswith(
                    'png') or file.endswith('bmp'):
            #  if file.endswith('jpeg') or file.endswith('gif') or file.endswith('png') or file.endswith('bmp'):
                fileObj = root + '/' + file
                imageNum = imageNum + 1
                try:
                    im = Image.open(fileObj)
                except IOError:
                    errorAtt.append(fileObj)
                else:
                    imageW = im.size[0]
                    imageH = im.size[1]
                    imagWH = imageW * imageH
                    # 图片的byte 数
                    n = os.path.getsize(fileObj)
                    # 图片的kb 数量
                    nOfKb = n / 1024.00
                    # allNeiCun
                    allNeiCun += nOfKb
                    # 内存和图片面积的比值
                    imageSizeN = n * 1.0 / imagWH
                    if nOfKb > neicunofMax:
                        source = tinify.from_file(fileObj)
                        source.to_file(os.path.join(dstPath, file))

                        print("内存占用大于%.f kb  内存大小是: %.2f kb  的图片名称是 %s  " % (neicunofMax, nOfKb, file))
                        bigImageNum += 1
                        alleNeiCunBigThan = alleNeiCunBigThan + nOfKb


def compressImages(uncompress_images):
    for pngDict in uncompress_images:
        source = tinify.from_file(pngDict['path'])
        source.to_file(os.path.join(dest_file, pngDict['name']))

def replace_file(new_path, old_path):
    pngs = getPngFileNames(source_file)
    for name in os.listdir(new_path):
        for pngDict in pngs:
            if pngDict['name'] == name:
                shutil.copyfile(os.path.join(new_path, name), pngDict['path'])



print("请输入1还是2来选择")
print("请输入1 代表 指定目录下面的图片进行分析")
print("请输入2 代表 当前目录下的图片进行分析")
# select =  raw_input();
select = int(input("Enter a number (1或者2) : "))

if select == 1:
    path2 = "/Users/wanggang/Downloads/douyuWork1"
    print("请输入3 代表 比例分析")
    print("请输入4 代表 大小分析")
    print("请输入5 代表 比例和大小都分析")

    select1 = int(input("Enter a number (3 或 4 或 5) : "))
    # if select1 == 3:
    #     findneicunSizeRate(path2)
    # elif select1 == 4:
    #     findneicunIsBig(path2)
    # else:
    #     findneicunSizeRate(path2)
    #     findneicunIsBig(path2)

elif select == 2:
    findneicunSizeRate(pathCurrent)
    findneicunIsBig(pathCurrent)
else:
    print("输入的数字有误,只能输入1或者2")


print("项目中总的图片的内存大小 %.3f M\n 项目中的大于%.0fkb的内存的大小是 %.3f M\n项目总的图片张数 %.0f 大于限制的内存(比如大于20kb)的图片的张数是 %.0f张\n内存比例大于预设值(即这部分图片还有压缩空间)的图片张数是 %.0f 张 " % (allNeiCun/1024.000, neicunofMax, alleNeiCunBigThan/1024.000,imageNum,bigImageNum,imageRateTooBig))
print("下面是pillow 处理异常的图片")
print(errorAtt)
