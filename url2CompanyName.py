import re
import time

import ddddocr

from driverOperation import xpath

docr = ddddocr.DdddOcr()


def getShopInfoUrl(driver):
    """
    从商品链接获取到商铺链接
    :return:
    """
    pageSource = xpath(driver, """//*[@id="crumb-wrap"]/div/div[2]/div[2]/div[1]""").get_attribute("outerHTML")
    shopUrls = re.findall('href="(.*?)"', pageSource)
    shopInfoUrl = shopUrls[0]
    shopInfoUrl = "https:" + shopInfoUrl
    return shopInfoUrl


def sendValCode(driver):
    """
    输入验证码
    :return:
    """
    while "验证码为空" in driver.page_source or "验证码错误" in driver.page_source or "验证码过期" in driver.page_source or "验证码" in driver.page_source:
        xpath(driver, """//*[@id="verifyCodeImg"]""").screenshot("D:/验证码.png")
        with open('D:/验证码.png', 'rb') as f:
            img_bytes = f.read()
        valCode = docr.classification(img_bytes)
        xpath(driver, """//*[@id="verifyCode"]""").clear()
        xpath(driver, """//*[@id="verifyCode"]""").send_keys(valCode)  # 输入验证码
        xpath(driver, """//*[@id="wrap"]/div/div[2]/div/form/ul/li[5]/button""").click()  # 确定
        time.sleep(1)


def url2ShopName(driver, jdUrl):
    if driver.current_url != jdUrl:
        driver.get(jdUrl)
    driver.execute_script("window.scrollBy(0,300)")
    # //*[@id="popbox"]/div/div[1]/h3/a
    # //*[@id="popbox"]/div/div[1]/h3/a
    #
    shopName = xpath(driver, """//*[@id="popbox"]/div/div[1]/h3/a""").text
    return shopName


# https://mall.jd.com/showLicence-1000406242.html
def url2Company(driver, jdUrl):
    """
    从商品链接得到公司名
    :param jdUrl:
    :return:
    """
    baseUrl = "https://mall.jd.com/showLicence-{}.html"
    if driver.current_url != jdUrl:
        driver.get(jdUrl)
    shopINfoUrl = getShopInfoUrl(driver)
    # 进入店铺详情
    driver.get(shopINfoUrl)
    # 进入资质信息页面
    source = xpath(driver, """/html/body/div[2]/div/div/div[1]""").get_attribute("outerHTML")
    if "showLicence" in source:
        tempurl = re.findall('showLicence-(.*?).html', source)[0]
        tempurl = baseUrl.format(tempurl)
    else:
        # print("改商铺没有企业资质")
        return ""
    driver.get(tempurl)
    # 输入验证码
    sendValCode(driver)
    # 企业名称
    companyName = xpath(driver, """//*[@id="wrap"]/div/div[2]/div/ul/li[2]/span""").text
    return companyName


def getCurrentTime():
    time_tuple = time.localtime(time.time())
    return "{}年{}月{}日{}点{}分{}秒".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                       time_tuple[5])


if __name__ == "__main__":
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
    urls = urls.split("\n")
    for url in urls:
        print(getCurrentTime())
        print(url)
        print(url2Company(driver, url))
