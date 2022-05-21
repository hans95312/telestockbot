from pyrogram import Client
import pyrogram

import candlestickChart
from crawler import crawler
import dailyPrice as dp
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


api_id = 888888888
api_hash = "999999999"
bot_token = "11111111"

app = Client("test", bot_token=bot_token, api_id=api_id, api_hash=api_hash)


def intimeReport(num):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome("/Users/linchenghan/Downloads/chromedriver 2", options=chrome_options)

    driver.get("https://pchome.megatime.com.tw/stock/sid"+str(num)+".html")
    button = driver.find_element_by_id("fancybox-close")
    button.click()

    info = driver.find_element_by_id("StockChart")
    info.screenshot("intimereport.png")


def vconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    # take minimum width
    w_min = min(img.shape[1] for img in img_list)

    # resizing images
    im_list_resize = [cv2.resize(img,
                                 (w_min, int(img.shape[0] * w_min / img.shape[1])),
                                 interpolation=interpolation)
                      for img in img_list]
    # return final image
    return cv2.vconcat(im_list_resize)


def is_stock(input):
    stock = []
    stocklist = open("table.csv", "r")
    for row in stocklist:
        stock.append(row.split(',')[0])
    if input in stock:
        return True
    else:
        return False



@app.on_message()
def log(client, message):
    stock = str(str(message).split(',')[-2].split(":")[1][2:-1])

    if stock[0:3] == "add" or stock[0:3] == "Add":
        stock = stock[4:].split()
        successful = []
        fail = []

        for a in stock:
            if is_stock(a):
                old_stocklist = open("stockList.txt", "r")
                lines = old_stocklist.readlines()
                old_stocklist.close()
                temp_list = []
                for line in lines:
                    temp_list.append(line)
                if a + '\n' in temp_list:
                    fail.append(a)
                    continue
                temp_list.append(a + "\n")
                temp_list.sort()
                new_stocklist = open("stockList.txt", "w")
                for t in temp_list:
                    new_stocklist.write(t)
                new_stocklist.close()
                successful.append(a)
            else:
                fail.append(a)

        successfulMsg = "added: "
        for s in successful:
            successfulMsg = successfulMsg + s + " "
        failMsg = "fail: "
        for f in fail:
            failMsg = failMsg + f + " "
        if len(successful) == 0 and len(fail) != 0:
            app.send_message(769880776, failMsg)
        elif len(successful) != 0 and len(fail) == 0:
            app.send_message(769880776, successfulMsg)
        else:
            app.send_message(769880776, successfulMsg + "\n" + failMsg)

    elif stock[0:6] == "delete" or stock[0:6] == "Delete":
        stock = stock[7:] + "\n"

        old_stocklist = open("stockList.txt", "r")
        lines = old_stocklist.readlines()
        old_stocklist.close()

        if stock in lines:
            new_stocklist = open("stockList.txt", "w")
            for l in lines:
                if l != stock:
                    new_stocklist.write(l)
            new_stocklist.close()
            app.send_message(769880776, "delete " + stock[:-1] + " success.")
        else:
            app.send_message(769880776, stock[:-1] + " not in list.")

    elif stock[0:6] == "search" or stock[0:6] == "Search":
        stock = stock[7:]
        stock_list = [stock]
        if is_stock(stock):
            candlestickChart.show_candelstick(stock)
            dp.daily_report(stock_list)
            msg = crawler(stock)

            img1 = cv2.imread("candlestickchat.png")
            img2 = cv2.imread("mytable.png")
            sendimg = vconcat_resize([img2, img1])
            cv2.imwrite('sendimg.jpg', sendimg)

            app.send_photo(769880776, 'sendimg.jpg')
            app.send_message(769880776, msg, parse_mode=pyrogram.enums.ParseMode.MARKDOWN,
                             disable_web_page_preview=True)
        else:
            app.send_message(769880776, "cannot find it!")

    elif stock[0:5] == "focus" or stock[0:5] == "Focus":
        stocklist = open("stockList.txt", "r")
        lines = stocklist.readlines()
        msg = "focus stock: "
        for line in lines:
            msg = msg + line[:-1] + " "
        app.send_message(769880776, msg)

    elif stock[0:5] == "chart" or stock[0:5] == "Chart":
        stock = stock[6:]
        intimeReport(stock)
        app.send_photo(769880776, 'intimereport.png')
    else:
        app.send_message(769880776, "Cannot understand your instruction! \nPlease retry!")


app.run()
