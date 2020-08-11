from bs4 import BeautifulSoup
import requests

class Stock:
    #建構式
    def __init__(self, *stock_nums):
        self.stock_nums = stock_nums
        # print(self.stock_nums)
    #爬取
    def scrape(self):
        result = list()
        for stock_num in self.stock_nums:
            response = requests.get("https://tw.stock.yahoo.com/q/q?s=" + stock_num)
            soup = BeautifulSoup(response.text.replace("加到投資組合", ""), "lxml")
            #資料日期 stock_date
            stock_date = soup.find("font", {"class": "tt"}).getText().strip()[-9:]
            #取得成交價
            tables = soup.findAll("table")[2]
            tds = tables.findAll("td")[0:11]
            result.append((stock_date,) + tuple(td.getText().strip() for td in tds)
)
        return result




stock = Stock("2330","2404")
# print(stock.scrape())
stock.save(stock.scrape())