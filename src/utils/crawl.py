import io
from datetime import datetime

import pytesseract
import requests
from bs4 import BeautifulSoup as BSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from src.utils.supports import (get_date, get_date_test, get_str_date_test,
                                get_time_start)
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Thay path trong .env
# .env = cp .env.template .env
wd = webdriver.Chrome(service=Service(
    ChromeDriverManager(print_first_line=False).install()),
                      options=options)


def get_src(msv):
    wd.get('http://sinhvien.epu.edu.vn/TraCuuThongTin.aspx')

    # pass capcha
    img = wd.find_element(By.CSS_SELECTOR, '#imgSecurityCode1')
    src = img.get_attribute('src')

    response = requests.get(src)
    img = Image.open(io.BytesIO(response.content))

    extract = pytesseract.image_to_string(img)

    # lấy thông tin sinh viên
    wd.find_element(
        By.XPATH,
        "//*[@id='ctl00_ContentPlaceHolder_txtMaSoSV']").send_keys(msv)
    wd.find_element(
        By.XPATH,
        "//*[@id='ctl00_ContentPlaceHolder_txtSercurityCode1']").send_keys(
            extract[:4])

    wait = WebDriverWait(wd, 10)
    wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
             "#ctl00_ContentPlaceHolder_btnTraCuuThongTin"))).click()

    # đến trang thời khóa biểu
    src_timetest = wd.find_element(
        By.CSS_SELECTOR,
        "#TblDanhSachSinhVien > tbody > tr:nth-child(2) > td:nth-child(8) > a"
    ).get_attribute("href")
    src_timetable = wd.find_element(
        By.CSS_SELECTOR,
        "#TblDanhSachSinhVien > tbody > tr:nth-child(2) > td:nth-child(7) > a"
    ).get_attribute("href")

    return (src_timetable, src_timetest)


def get_test_timetable(msv, src):
    wd.get(src)

    # chạy vòng for để lấy kỳ 1 và 2 năm học
    lst_data = []
    for hk in range(1, 5):
        select = Select(
            wd.find_element(By.CSS_SELECTOR,
                            "#ctl00_ContentPlaceHolder_cboHocKy3"))
        select.select_by_index(hk)

        wait = WebDriverWait(wd, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "#ctl00_ContentPlaceHolder_btnSearch"))).click()
        try:
            table = wd.find_element(By.CSS_SELECTOR, "#detailTbl > tbody")

            tags_tr = table.find_elements(By.TAG_NAME, 'tr')

            for tags_td in tags_tr[1:]:
                data = tags_td.find_elements(By.TAG_NAME, 'td')
                if datetime.now().date() < get_date_test(data[5].text):
                    info = {
                        "classname": data[1].text.strip(),
                        "subject": data[2].text,
                        "date": data[5].text,
                        "time": data[7].text,
                        "room": data[8].text,
                        "time_start": get_time_start(data[7].text),
                        "date_start": get_str_date_test(data[5].text),
                        "student_id": msv
                    }
                    lst_data.append(info)
        except Exception:
            pass

    return lst_data


def get_class_timetable(msv, src):
    labels = [
        'weekday', 'class_code', 'subject', 'class_time', 'teacher',
        'classroom', 'date_fromto', 'date_start', 'time_start', 'student_id'
    ]

    wd.get(src)

    lst_data = []
    for i in range(1, 5):
        select = Select(
            wd.find_element(By.CSS_SELECTOR,
                            "#ctl00_ContentPlaceHolder_cboHocKy3"))

        # chạy vòng for để lấy kỳ 1 và 2 năm học
        select.select_by_index(i)

        wait = WebDriverWait(wd, 2)
        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "#ctl00_ContentPlaceHolder_btnSearch"))).click()

        # Chuyển về bs4 để duyệt nhanh hơn
        bs_obj = BSoup(wd.page_source, 'html.parser')
        try:
            rows = bs_obj.find(id='detailTbl').find('tbody').find_all('tr')

            for tags_td in rows[1:]:
                try:
                    tag_td_index_2 = tags_td.find_all('td')[2]
                    weekday = tags_td.find_all('td')[0]
                except Exception:
                    pass
                for tr in tag_td_index_2.find_all('tr'):
                    data = [weekday.getText()]
                    for td in tr.find_all('td'):
                        data.append(td.get_text().replace('\n', '').strip())

                    if 'Môn học đã kết thúc' not in data[2]:
                        data[2] = ' '.join(data[2].split())
                        date_str = data[6]
                        data.append(get_date(date_str))
                        data[6] = ' '.join(data[6].split())
                        time_str = data[3]
                        data.append(get_time_start(time_str))
                        data.append(msv)

                        lst_data.append(dict(zip(labels, data)))
        except Exception:
            pass

    return lst_data


def get_data(msv: str):
    count = 0
    while True:
        count = count + 1
        if count == 5:
            print("Khong vao duoc trang hoac msv ko dung")
            return {'msv': False}
        try:
            src_timetable, src_timetest = get_src(msv)
            break
        except Exception as ex:
            print(ex)
            pass

    count = 0
    while True:
        count = count + 1
        if count == 5:
            print("Khong lay duoc testtable")
            return {'msv': False}
        try:
            testtable = get_test_timetable(msv, src_timetest)
            break
        except Exception as ex:
            print(ex)
            pass

    count = 0
    while True:
        count = count + 1
        if count == 5:
            print("Khong vao duoc trang thoi khoa bieu")
            return {'msv': False}
        try:
            timetable = get_class_timetable(msv, src_timetable)
            break
        except Exception as ex:
            print(ex)
            pass

    print("TIMETABLE", timetable)
    print("TESTTABLE", testtable)
    wd.close()
    return testtable, timetable


get_data('18810310312')
