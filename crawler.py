from GoogleNews import GoogleNews


def searchName(num):
    stockname = open("table.csv", 'r')
    for row in stockname:
        if row.split(',')[0] == num:
            return row.split(',')[1]


def crawler(num):
    googlenews = GoogleNews()
    googlenews.setlang('cn')
    googlenews.setencode('utf-8')
    googlenews.setperiod(period='1d')

    name = searchName(num)
    googlenews.search(name)
    result = googlenews.result()

    send = '最新相關新聞：\n'
    i = 1
    for n in range(len(result)):
        send = send + str(i) + '. [' + result[n]['title'] + '](' + result[n]['link'] + ")\n"+result[n]['media']+" 更新時間： " + result[n][
            'date'] + "\n"
        i += 1
    return send
