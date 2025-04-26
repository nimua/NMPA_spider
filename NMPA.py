import time
from DrissionPage import Chromium
from bs4 import BeautifulSoup
from openpyxl import Workbook


def save_to_excel(data, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "sheet1"
    ws.append(["字段", "值"])
    for item in data:
        ws.append([item[0], item[1]])
    wb.save(filename)
def spider(browser, item_list):
    for item in item_list:
        item.click()
        time.sleep(10)
        tab_item = browser.get_tabs()[0]
        soup = BeautifulSoup(tab_item.html, 'html.parser')
        table = soup.find('table', {'class': 'el-table__body'})
        rows = table.find_all('tr')
        data = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                data.append((key, value))
                save_to_excel(data, f"{data[0][1]}.xlsx")
        tab_item.close()

if __name__ == '__main__':
    browser = Chromium()
    url = "https://www.nmpa.gov.cn/datasearch/home-index.html#category=ylqx"
    tab = browser.latest_tab
    tab.get(url)
    tab.eles('@class=el-input__inner')[1].input("乙型肝炎病毒")
    tab.ele('@class=el-button el-button--default').click()

    time.sleep(3)
    tab1 = browser.get_tabs()[0]
    item_list=tab1.eles('@class=el-button el-button--primary el-button--mini')
    while item_list==10:
        spider(browser, item_list)
        tab1.eles('@class=el-icon el-icon-arrow-right')[0].click()
        item_list = tab1.eles('@class=el-button el-button--primary el-button--mini')

    spider(browser, item_list)


