from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import os
# taggee_class = "taggee"
taggee_class = "_hli"


class TagFinder():
    def __init__(self):
        self.in_between_wait = .05
        self.driver = self.setup_selenium_driver()
        self.taggees = {}
        self.successful_retrievals = 0
        self.first_url = ""

    def setup_selenium_driver(self):
        usr = os.getenv('fbusername')
        pwd = os.getenv('fbpassword')
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

        driver = webdriver.Chrome(executable_path=DRIVER_BIN)
        # driver = webdriver.Firefox(
        #     executable_path='/Users/mattross/webdriver/gecko/v0.26.0/geckodriver-v0.26.0-macos/geckodriver')

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

                    try:
                        tag_date = driver.find_element_by_class_name("_39g5").text
                        if not self.taggees[tager]["last_tagged"]:
                            self.taggees[tager]["last_tagged"] = tag_date
                        self.taggees[tager]["first_tagged"] = tag_date
                    except Exception as e:
                        # print(e)
                        print("")
                        # print("could not get date ")


                    # Manage Current Speed Of Timer
                    if self.successful_retrievals < 6:
                        self.successful_retrievals += 1
                    else:
                        # print("Retrieved 6 photos in a row successfully, resetting sleep timer")
                        self.successful_retrievals = 0
                        self.in_between_wait = .05

                    if driver.current_url != self.first_url:
                        return tager
                    else:
                        self.stop_iteration_and_display_data()
            except Exception as e:

                # print("Could not load page fast enough, trying again {}".format(e))
                self.in_between_wait += .1
                # print("increasing global wait time to {}".format(self.in_between_wait))
                sleep(self.in_between_wait)
                driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_RIGHT)

    def find_all_tagged_photos(self):

        driver = self.driver
        profile_url = "https://www.facebook.com/Ross.Ross.1080/photos"
        # profile_url = "https://www.facebook.com/steviedunbardude/photos"
        # profile_url = "https://www.facebook.com/morgan.mueller.14/photos"
        driver.get(profile_url)
        #driver.get("https://www.facebook.com/dana.elkis/photos")
        sleep(.5)
        driver.find_element_by_css_selector('body').click()
        tags = driver.find_elements_by_class_name('fbPhotoStarGridElement')
        sleep(1)
        tags[0].click()

        sleep(1)
        print("starting iteration ")


        for i in range(300):

            tager = self.get_name_of_tagger(driver)

            if not self.first_url:
                self.first_url = driver.current_url
            if tager not in self.taggees.keys():
                self.taggees[tager] = {"tag_count": 1, "first_tagged": "", "last_tagged": ""}


                print("You have been tagged by {} count is at {}".format(tager,len(self.taggees.keys())))
            else:
                self.taggees[tager]["tag_count"] += 1
            # print("You have been tagged by {} {}  times ".format(tager,taggees[tager]))
            driver.find_element_by_css_selector('body').send_keys(Keys.ARROW_RIGHT)
            sleep(self.in_between_wait)

        self.stop_iteration_and_display_data()

    def stop_iteration_and_display_data(self):

        self.driver.quit()

        print("Done Iterating through FB Photos, displaying counts now.....\n\n\n\n")
        sleep(1)

        for tager in self.taggees.keys():
            print("You have been tagged by {} , {} times ".format(tager, self.taggees[tager]["tag_count"]))
            print("The first time you were tagged by them was {}".format(self.taggees[tager]["first_tagged"]))
            print("The last time you were tagged by them was {}".format(self.taggees[tager]["last_tagged"]))
            print("-----------------------------------------------------------------------------")
        exit()


def main():
    tagFinder = TagFinder()
    tagFinder.find_all_tagged_photos()


if __name__ == '__main__':
    main()
