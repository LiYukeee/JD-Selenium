"""
输入一个京东商品网址，爬取其数据并保存
"""
import os
import re
import time

import img2pdf
from PIL import Image

from driverOperation import xpath
from fileOperation import createFold
import configparser

config = configparser.ConfigParser()
configPath = r"./data/config.ini"
config.read(configPath)
createFold('./data')
createFold('./data/temp')
createFold('./data/pdf')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
count = 0
# https://img11.360buyimg.com/n1/jfs/t1/88138/35/33158/116749/640bdd90F07e4ec50/d57a30a5b8b102b5.jpg # 高清
# https://img11.360buyimg.com/n5/jfs/t1/88138/35/33158/116749/640bdd90F07e4ec50/d57a30a5b8b102b5.jpg
"""
src="//img11.360buyimg.com/n5/jfs/t1/51539/38/22932/70818/640826b0F37d69863/e05133587a6f476f.jpg"
"""


def showImage(driver, basePath):
    """
    保存展示图片
    :return:
    """
    pageSource = xpath(driver, """//*[@id="spec-list"]/ul""").get_attribute("outerHTML")
    imgUrls = re.findall('src="(.*?)"', pageSource)
    for i in range(len(imgUrls)):
        ############### 直接下载图片方法，但读取出错
        # tempUrl = imgUrls[i]
        # tempUrl = 'https:' + tempUrl
        # tempUrl = tempUrl.replace("360buyimg.com/n5", "360buyimg.com/n1")  # 转换为高清图片的网址
        # r = requests.get(tempUrl, headers=headers)
        # f = open("{}/展示{}.bmp".format(basePath, i), 'wb')
        # f.write(r.content)
        # f.close()
        # time.sleep(0.1 + random.random() / 3)  # 加入随机等待时间
        ################ 截屏方法
        xpath(driver, """//*[@id="spec-img"]""").screenshot("{}/展示{}.bmp".format(basePath, i))
        # 点击下一张
        if i != len(imgUrls) - 1:  # 最后一个图片无需再点击下一张
            try:
                xpath(driver, """//*[@id="spec-list"]/ul/li[{}]/img""".format(i + 2)).click()
            except:
                try:
                    xpath(driver, """//*[@id="spec-backward"]/i""").click()
                    time.sleep(1)
                    xpath(driver, """//*[@id="spec-list"]/ul/li[{}]/img""".format(i + 2)).click()
                except:
                    a = 1
        time.sleep(0.2)


def getImage(driver, jdUrl, basePath):
    if driver.current_url != jdUrl:
        driver.get(jdUrl)
    driver.execute_script("window.scrollBy(0,-300)")
    time.sleep(0.2)
    # 主界面截取图片
    driver.get_screenshot_as_file(r'{}/主图.png'.format(basePath))
    # 商品详情
    driver.execute_script("window.scrollBy(0,800)")
    time.sleep(0.3)
    xpath(driver, """//*[@id="detail"]/div[2]/div[1]/div[1]""").screenshot(r'{}/详情1.png'.format(basePath))
    xpath(driver, """//*[@id="detail"]/div[1]/ul/li[2]""").click()
    xpath(driver, """//*[@id="detail"]/div[2]""").screenshot(r'{}/详情2.png'.format(basePath))
    # 抓取展示图片
    showImage(driver, basePath)


def png2png(basePath, num):
    """
    将temp中的png图片拼合\n
    :param basePath: 路径
    :param num: 一行显示多少个展示图片
    :return:
    """
    # 获取图片列表
    img1 = Image.open(r'{}/主图.png'.format(basePath))
    img21 = Image.open(r'{}/详情1.png'.format(basePath))
    img22 = Image.open(r'{}/详情2.png'.format(basePath))
    img3 = Image.open(r'{}/展示0.bmp'.format(basePath))
    img3List = []
    i = 0
    while True:
        if os.path.exists(r'{}/展示{}.bmp'.format(basePath, i)):
            img3List.append(r'{}/展示{}.bmp'.format(basePath, i))
        else:
            break
        i += 1
    img1Size = img1.size
    img21Size = img21.size
    img22Size = img22.size
    img3Size = img3.size
    # 生成新图片
    newPNG = Image.new("RGB",
                       (max([img1Size[0], img21Size[0], img3Size[0] * num]),
                        img1Size[1] + img21Size[1] + img22Size[1] + (int(len(img3List) / num) + 1) * img3Size[1]),
                       color='white')
    newPNG.paste(img1, (0, 0))
    newPNG.paste(img21, (0, img1Size[1]))
    newPNG.paste(img22, (0, img1Size[1] + img21Size[1]))
    start = img1Size[1] + img21Size[1] + img22Size[1]
    for i in range(len(img3List)):
        width = i % num
        length = int(i / num)
        img30 = Image.open(img3List[i])
        newPNG.paste(img30, (width * img3Size[0], start + length * img3Size[1]))
        img30.close()
    newPNG.save("{}/总图.png".format(basePath))
    img1.close()
    img21.close()
    img22.close()
    img3.close()


def png2pdf(basePath, pdfName):
    """
    将图片转化为PDF
    :param basePath: 路径
    :param pdfName:要保存为的pdf文件名
    :return:
    """
    with open("{}/{}.pdf".format(basePath, pdfName), "wb") as file:
        file.write(img2pdf.convert('{}/总图.png'.format(basePath)))
        file.close()
    return "{}/{}.pdf".format(basePath, pdfName)


def delFileContainX(path, X):
    fileList = os.listdir(path)
    for file in fileList:
        if X in file:
            os.remove(os.path.join(path, file))


def url2Data(driver, itemUrl):
    """
    输入链接保存数据
    :param itemUrl: 京东商品链接
    :return:
    """
    name = re.findall("""[1-9]\d*""", itemUrl)[0]  # 提取商品id
    tempPath = "./data/temp/{}".format(name)
    createFold(tempPath)
    # 保存图片
    getImage(driver, itemUrl, tempPath)
    # 获取店铺名
    shopName = xpath(driver, """//*[@id="popbox"]/div/div[1]/h3/a""").text
    # 合并图像
    png2png(tempPath, 4)
    # 转换为pdf
    pdfPath = png2pdf(tempPath, "{}违规证明".format(shopName))
    # rmdir(tempPath)
    if config['asd']['removeImage'] == '1':
        delFileContainX(tempPath, 'png')
        delFileContainX(tempPath, 'bmp')
    return os.path.abspath(pdfPath)


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                       time_tuple[5])


if __name__ == '__main__':
    from driverOperation import driverInit

    driver = driverInit(r"D:/")
    urls = """https://item.jd.com/5267712.html
https://item.jd.com/100021533599.html
https://item.jd.com/20165821485.html
https://item.jd.com/100021533647.html
https://item.jd.com/71067792011.html
https://item.jd.com/10024713897841.html
https://item.jd.com/10056133859501.html
https://item.jd.com/100019367050.html
https://item.jd.com/10067467053183.html
https://item.jd.com/10068997156561.html
https://item.jd.com/10068366620696.html
https://item.jd.com/100049591851.html
https://item.jd.com/10068555685267.html
    """
    urls = urls.split('\n')
    count = 0
    while True:
        for url in urls:
            try:
                url2Data(driver, url)
                count += 1
                print(getCurrentTime())
                print("成功", count, driver.title)
                time.sleep(0)
            except:
                count += 1
                print("失败", count, driver.title)
