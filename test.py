import time

from driverOperation import driverInit

"""
不登陆第一次62条
不登陆第二次62条
"""
driver = driverInit("D:")
urls = """https://item.jd.com/100030406260.html
https://item.jd.com/100018174388.html
https://item.jd.com/1093727503.html
https://item.jd.com/10039171554300.html
https://item.jd.com/100014989462.html
https://item.jd.com/28205255000.html
https://item.jd.com/100027845283.html
https://item.jd.com/100016821199.html
https://item.jd.com/100027319141.html
https://item.jd.com/10031227352707.html
https://item.jd.com/100038842281.html
https://item.jd.com/10063390396560.html
https://item.jd.com/49549202698.html
https://item.jd.com/100027044600.html
https://item.jd.com/100005868501.html
https://item.jd.com/100048852887.html
https://item.jd.com/100023060293.html
https://item.jd.com/5267712.html
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
count = 1
driver.get("https://passport.jd.com/new/login.aspx")
input()
while True:
    try:
        for url in urls:
            driver.get(url)
            count += 1
            print(count, driver.title)
            time.sleep(5)
    except:
        a = 1
