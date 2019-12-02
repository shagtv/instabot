import time
from getpass import getpass
from random import randint

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common import keys


class InstaBot:
    def __init__(self, username, password, web_driver):
        self.username = username
        self.password = password
        self.bot = web_driver

    def __del__(self):
        """
        Close a browser on exit
        :return: None
        """
        self.bot.close()

    def login(self):
        """
        Login on instagram
        :return: None
        """
        self.bot.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        self.__wait(3, 5)
        email = self.bot.find_element_by_name('username')
        password = self.bot.find_element_by_name('password')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(keys.Keys.RETURN)
        self.__wait(3, 5)

        buttons = self.bot.find_elements_by_tag_name('button')
        for button in buttons:
            if button.text == 'Not Now':
                button.click()
                self.__wait(3, 5)

    def like_followings(self):
        """
        Like last following's posts
        :return: None
        """
        total_liked = 0
        for _ in range(10):
            total_liked += self.like_all_on_page()
            self.bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            self.__wait(3, 5)
        print('{} [posts] were liked'.format(total_liked))

    def like_tag(self, tag):
        """
        Like some posts by tag
        :param tag:
        :return: None
        """
        total_liked = 0
        tag_link = 'https://www.instagram.com/explore/tags/{}/'.format(tag)
        self.bot.get(tag_link)
        self.__wait(3, 5)

        for _ in range(2):
            self.bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            self.__wait(3, 5)

        links = self.bot.find_elements_by_tag_name('a')
        links = [link.get_attribute('href') for link in links if '/p/' in link.get_attribute('href')]

        print('{} links were found'.format(len(links)))

        for link in links:
            self.bot.get(link)
            self.__wait(3, 5)
            total_liked += self.like_all_on_page()

        print('{} [posts] were liked'.format(total_liked))

    def like_all_on_page(self):
        """
        Click all like buttons on the page
        :return: total liked pages
        """
        total_liked = 0
        likes = self.bot.find_elements_by_class_name('glyphsSpriteHeart__outline__24__grey_9')
        for like in likes:
            try:
                like.click()
            except StaleElementReferenceException as err:
                print('Error on like: {}'.format(err))

            total_liked += 1
            self.__wait(10, 15)
        return total_liked

    @staticmethod
    def __wait(min_sec, max_sec):
        """
        Wait some seconds to load page or avoid blocking the account
        :param min_sec:
        :param max_sec:
        :return: None
        """
        time.sleep(randint(min_sec, max_sec))


if __name__ == '__main__':
    print('Welcome to Twitter bot')
    instagram_username = input('Enter your Instagram username or email: ')
    instagram_password = getpass('Enter your password: ')

    mode = int(input('Enter like mode 1) followings 2) by tag: '))
    hashtag = ''
    if mode == 2:
        hashtag = input('hashtag: ')

    driver_type = int(input('Choose webdriver 1) Chrome 2) Firefox: '))
    if driver_type == 1:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()

    if instagram_username and instagram_password:
        bot = InstaBot(instagram_username, instagram_password, driver)
        bot.login()
        if mode == 2 and hashtag:
            bot.like_tag(hashtag)
        else:
            bot.like_followings()
