import configparser
import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

config = configparser.ConfigParser()
configPath = r"./data/config.ini"
config.read(configPath)
implicitlyWait = int(config['asd']['implicitlyWait'])


def xpath(dr, val):
    """
    driver.find_element_by_xpath 便捷方法
    """
    return dr.find_element(by=By.XPATH, value=val)


def driverInit(path):  # 浏览器初始化
    """
    driver初始化
    :return: driver
    """
    # 打开谷歌浏览器
    chrome_options = webdriver.ChromeOptions()
    settings = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,  # 另存为pdf，1 是默认打印机
        "isHeaderFooterEnabled": True,  # 是否勾选页眉和页脚
        # "customMargins": {},
        # "marginsType": 2,#边距（2是最小值、0是默认）
        # "scaling": 100,
        # "scalingType": 3,
        # "scalingTypePdf": 3,
        # "isLandscapeEnabled": True,  # 若不设置该参数，默认值为纵向
        "isCssBackgroundEnabled": True,
        "mediaSize": {
            "height_microns": 297000,
            "name": "ISO_A4",
            "width_microns": 210000,
            "custom_display_name": "A4"
        },
    }
    chrome_options.add_argument('--enable-print-browser')
    # chrome_options.add_argument('--headless') #headless模式下，浏览器窗口不可见，应当可提高效率
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': r'{}'.format(path)  # 此处填写你希望文件保存的路径,可填写your file path默认下载地址
    }
    chrome_options.add_argument('--kiosk-printing')  # 静默打印，无需用户点击打印页面的确定按钮
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () => undefined
                            })
                          """})
    driver.implicitly_wait(implicitlyWait)
    driver.set_window_size(1280, 720)
    return driver


def switchWindow(driver, number):  # 切换窗口
    """
    使焦点位于第N个标签页， 顺序为打开的先后顺序
    :param driver:
    :param number:
    :return:
    """
    handles = driver.window_handles
    driver.switch_to.window(handles[number - 1])


def addNewTab(driver, url=""):
    """
    新建标签页，但焦点不会移动
    :param driver:
    :param url:
    :return:
    """
    js = "window.open('{}','_blank');"
    driver.execute_script(js.format(url))


def screenShotAll(driver, name, sleepTime=0):
    """
    打印页面
    :param driver:
    :param name: 保存的文件名，不用添加.pdf后缀
    :param sleepTime:
    :return:
    """
    driver.execute_script("window.scrollTo(0,0)")
    driver.execute_script("window.scrollTo(0,100000)")
    time.sleep(sleepTime)
    driver.execute_script(
        'document.title="{}.pdf";window.print();'.format(name))
    driver.execute_script("window.scrollTo(0,0)")
