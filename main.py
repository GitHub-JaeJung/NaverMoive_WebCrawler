from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import re
import math
import numpy
import pandas as pd
import os


query_txt = input('1.크롤링 할 영화의 제목을 입력하세요: ')
query_url = 'https://movie.naver.com'

cnt = int(input('2.크롤링 할 리뷰건수는 몇건입니까?: '))
page_cnt = math.ceil(cnt / 10)

f_dir = input("3.파일을 저장할 폴더명만 쓰세요(예:c:\\temp\\):")

now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)

f_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.txt'
fc_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.csv'
fx_name = f_dir + s + '-' + query_txt + '\\' + s + '-' + query_txt + '.xls'

path = "c:/temp/chromedriver_240/chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get(query_url)
time.sleep(2)

element = driver.find_element_by_id("ipt_tx_srch")
element.send_keys(query_txt)
driver.find_element_by_xpath("""//*[@id="jSearchArea"]/div/button""").click()
driver.find_element_by_xpath("""//*[@id="old_content"]/ul[2]/li/dl/dt/a""").click()

driver.find_element_by_link_text("평점").click()

driver.switch_to.frame('pointAfterListIframe')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

page_cnt = math.ceil(cnt / 10)

score2 = []
review2 = []
name2 = []
date2 = []
like_list = []
like2 = []
dislike2 = []
dwlist2 = []

count = 0
click_count = 1

while (click_count <= page_cnt):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    score_result = soup.find('div', class_='score_result').find('ul')
    slist = score_result.find_all('li')
    for li in slist:

        count += 1

        f = open(f_name, 'a', encoding='UTF-8')

        score = li.find('div', class_='star_score').find('em').get_text()
        print("1.별점:", "*" * int(score), ": ", score)
        score2.append(score)
        f.write("\n")
        f.write("1.별점:" + score + "\n")

        review = li.find('div', class_='score_reple').find('p').get_text()
        print("2. 리뷰내용:", review)
        f.write("2. 리뷰내용:" + review + "\n")
        review2.append(review)

        dwlist = li.find('div', class_='score_reple').find_all('em')
        name = dwlist[0].find('span').get_text()
        print("3. 작성자:", name)
        f.write("3. 작성자:" + name + "\n")
        name2.append(name)

        date = dwlist[1].text
        print('4. 작성일자:', date)
        f.write("4. 작성일자:" + date + "\n")
        date2.append(date)

        like_list = li.find('div', class_='btn_area').find_all('strong')
        like = like_list[0].text
        print('5. 공감:', like)
        f.write("5. 공감:" + like + "\n")
        like2.append(like)

        dislike = like_list[1].text
        print('6. 비공감:', dislike)
        f.write("6. 비공감:" + dislike + "\n")
        dislike2.append(dislike)
        print("\n")

        if count == cnt:
            break

    click_count += 1

    if click_count > page_cnt:
        break
    else:
        driver.find_element_by_link_text("%s" % click_count).click()

naver_movie = pd.DataFrame()
naver_movie['별점'] = score2
naver_movie['리뷰 내용'] = review2
naver_movie['작성자'] = name2
naver_movie['작성일자'] = date2
naver_movie['공감 횟수'] = like2
naver_movie['비공감 횟수'] = dislike2

# csv 저장
naver_movie.to_csv(fc_name, encoding="utf-8-sig", index=True)

# xls 저장
naver_movie.to_excel(fx_name, index=True)

print("1.파일 저장 완료: txt 파일명 : %s " % f_name)
print("2.파일 저장 완료: csv 파일명 : %s " % fc_name)
print("3.파일 저장 완료: xls 파일명 : %s " % fx_name)

driver.close()