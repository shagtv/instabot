from selenium import webdriver
from selenium.webdriver.common import keys
import time
from getpass import getpass
from random import randint


class InstaBot:
    def __init__(self, username, password, bot):
        self.username = username
        self.password = password
        self.bot = bot

    def __del__(self):
        self.bot.close()

    def login(self):
        bot = self.bot
        bot.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        time.sleep(3)
        email = bot.find_element_by_name('username')
        password = bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        time.sleep(3)

        buttons = bot.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Not Now':
                button.click()
                time.sleep(3)

    def like_followings(self):
        bot = self.bot
        total_liked = 0
        for _ in range(10):
            total_liked += self.like_all()
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(randint(3, 5))
        print('{} [posts] were liked'.format(total_liked))

    def like_tag(self, tag):
        bot = self.bot
        total_liked = 0
        tag_link = 'https://www.instagram.com/explore/tags/{}/'.format(tag)
        bot.get(tag_link)
        time.sleep(randint(3, 5))

        for _ in range(2):
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(randint(3, 5))

        links = bot.find_elements_by_tag_name('a')
        links = [link.get_attribute('href') for link in links if '/p/' in link.get_attribute('href')]

        print('{} links were found'.format(len(links)))

        for link in links:
            bot.get(link)
            time.sleep(randint(3, 5))
            total_liked += self.like_all()

        print('{} [posts] were liked'.format(total_liked))

    def like_all(self):
        bot = self.bot
        total_liked = 0
        likes = bot.find_elements_by_class_name('glyphsSpriteHeart__outline__24__grey_9')
        for like in likes:
            try:
                like.click()
                total_liked += 1
                time.sleep(randint(10, 15))
            except:
                time.sleep(randint(50, 60))
        return total_liked


if __name__ == '__main__':
    print('Welcome to Twitter bot')
    username = input('Enter your Instagram username or email: ')
    password = getpass('Enter your password: ')

    mode = int(input('Enter like mode 1) followings 2) by tag: '))
    hashtag = ''
    if mode == 2:
        hashtag = input('hashtag: ')

    driver_type = int(input('Choose webdriver 1) Chrome 2) Firefox: '))
    if driver_type == 1:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()

    if username and password:
        bot = InstaBot(username, password, driver)
        bot.login()
        if mode == 2 and hashtag:
            bot.like_tag(hashtag)
        else:
            bot.like_followings()
