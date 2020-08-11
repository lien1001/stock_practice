from bs4 import BeautifulSoup
import requests
import pymysql

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

    def save(self, stocks):
        db_settings = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "1234",
            "db": "stock",
            "charset": "utf8"
        }
        heroku_settings = {
            "host": "us-cdbr-east-02.cleardb.com/heroku_3a814c1e0821fab",
            "port": 3306,
            "user": "bf0f326f6057a5",
            "password": "79f39978",
            "db": "heroku_3a814c1e0821fab",
            "charset": "utf8"
        }

        try:
            # conn = pymysql.connect(**db_settings)
            conn = pymysql.connect(**heroku_settings)

            with conn.cursor() as cursor:
                sql = """INSERT INTO market(
                                market_date,
                                stock_name,
                                market_time,
                                final_price,
                                buy_price,
                                sell_price,
                                ups_and_downs,
                                lot,
                                yesterday_price,
                                opening_price,
                                highest_price,
                                lowest_price)
                         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                for stock in stocks:
                    cursor.execute(sql, stock)
                conn.commit()
        except Exception as ex:
            print("Exception:", ex)

if __name__ == "__main__":
    stock = Stock("2330","2404")
    # print(stock.scrape())
    stock.save(stock.scrape())
