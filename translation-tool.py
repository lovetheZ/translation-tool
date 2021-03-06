from selenium import webdriver
import time
from pyquery import PyQuery as pq
import pyautogui
import time
import tesserocr
from PIL import Image
from PIL import ImageGrab
from pymongo import MongoClient

client = MongoClient()
db = client['words']
collection = db['ENwords']

def get_words():
    try:
        bingo = True
        while bingo:
            x_1_1, y_1_1 = pyautogui.position()
            time.sleep(1)
            x_1_2, y_1_2 = pyautogui.position()

            if (x_1_1 == x_1_2) & (y_1_1 == y_1_2):
                # print('point one success')
                print('p1:', x_1_1, y_1_1)
            else:
                x_1_1 = None
                y_1_1 = None
                print('point one fault')

            time.sleep(2)

            if (x_1_1 != None) & (y_1_1 != None):
                # print('choosing the point two....');

                x_2_1, y_2_1 = pyautogui.position()
                # print('x_2_1:',x_2_1,'y_2_1:',y_2_1)
                time.sleep(1)
                x_2_2, y_2_2 = pyautogui.position()
                # print('x_2_2:', x_2_2, 'y_2_2:', y_2_2)
                if (x_2_1 == x_2_2) & (y_2_1 == y_2_2):
                    # print('point two success')
                    print('p2:', x_2_1, y_2_1)
                    bingo = False
                else:
                    x_2_1 = None
                    y_2_1 = None
                    print('point two fault')
            else:
                print('fault')

        bbox = (x_1_1 - 5, y_1_1 - 5, x_2_1 - 5, y_2_1 - 5)
        im = ImageGrab.grab(bbox)
        im.save('pp.png')
        image = Image.open('pp.png')
        text = tesserocr.image_to_text(image)
        text = text.strip('\n')
        print(text)
        return text
    except:
        print('get_words error!')
        return None

def get_source(words):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        #是否显示浏览器操作结果
        browser=webdriver.Chrome(chrome_options=options)
        url = 'http://fanyi.youdao.com/'
        browser.get(url)
        input = browser.find_element_by_id('inputOriginal')
        input.send_keys(('%s') % (words))
        time.sleep(1)
        source = browser.page_source
        file = open('source.txt', 'a', encoding='utf-8')
        file.write(source)
        file.close()
        return source
    except:
        print('get_source error!')
        return None

def translation(page_source):
    try:
        doc = pq(page_source)
        items = doc('.dict__relative').text()
        return items
    except:
        print('translation error!')
        return None

def save_words(words,transing):
    word={}
    word['EN']=words
    word['CN']=transing
    collection.insert_one(word)

if __name__ == '__main__':
    while True:
        switch=input()
        if (switch=='on'):
            words=get_words()
            page_source=get_source(words)
            transing=translation(page_source)
            print(transing)
            save_words(words,transing)
        else:
            pass