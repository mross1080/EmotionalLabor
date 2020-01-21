from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import os
taggee_class = "taggee"


class TagFinder():
    def __init__(self):
        self.in_between_wait = .3
        self.driver = self.setup_selenium_driver()
        self.taggees = {}

    def setup_selenium_driver(self):
        usr = os.getenv('fbusername')
        pwd = os.getenv('fbpassword')
        driver = webdriver.Firefox(
            executable_path='/Users/mattross/webdriver/gecko/v0.26.0/geckodriver-v0.26.0-macos/geckodriver')

        # driver = webdriver.Chrome()
        driver.get('https://www.facebook.com/')
        print("Opened facebook")
        sleep(.1)

        username_box = driver.find_element_by_id('email')
        username_box.send_keys(usr)
        print("Email Id entered")
        sleep(.21)

        password_box = driver.find_element_by_id('pass')
        password_box.send_keys(pwd)
        print("Password entered")

        login_box = driver.find_element_by_id('loginbutton')
        login_box.click()

        sleep(.1)

        return driver

    def get_name_of_tagger(self, driver):
        while True:
            try:
                tager = driver.find_element_by_class_name(taggee_class).text
                if tager is not None:
                    return tager
            except Exception as e:

                print("Could not load page fast enough, trying again {}".format(e))
                self.in_between_wait += .1
                print("increasing global wait time to {}".format(self.in_between_wait))
                sleep(self.in_between_wait)

    def find_all_tagged_photos(self):

        driver = self.driver
        driver.get("https://www.facebook.com/Ross.Ross.1080/photos")

        tags = driver.find_elements_by_class_name('fbPhotoStarGridElement')
        tags[0].click()

        sleep(1)
        print("starting iteration ")
        for i in range(2000):
            tager = self.get_name_of_tagger(driver)

            if tager not in self.taggees.keys():
                self.taggees[tager] = 1
                print("You have been tagged by {} ".format(tager))
            else:
                self.taggees[tager] += 1
            # print("You have been tagged by {} {}  times ".format(tager,taggees[tager]))
            driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_RIGHT)
            sleep(self.in_between_wait)

        print("Done")
        input('Press anything to quit')
        driver.quit()
        print("Finished")

        print("Done Iterating through FB Photos, displaying counts now.....\n\n\n\n")

        for tager in self.taggees.keys():
            print("You have been tagged by {} {}  times ".format(tager, self.taggees[tager]))


def main():
    tagFinder = TagFinder()
    tagFinder.find_all_tagged_photos()


if __name__ == '__main__':
    main()
