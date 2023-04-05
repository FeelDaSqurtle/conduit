import random
import time
import csv

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class TestConduit(object):
    # Böngésző megnyitás / bezárása funkció

    def setup_method(self):
        time.sleep(1)
        service = Service(executable_path='ChromeDriver/chromedriver.exe')
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(service=service, options=options)

        URL_main = "http://localhost:1667/#/"
        self.browser.get(URL_main)
        self.browser.implicitly_wait(5)
        self.browser.set_script_timeout(6)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()
        time.sleep(1)

    # Kisegítő metódusok

    def login(self):
        login_credentials = []
        with open('vizsgaremek/Vizsgaremek_Python/login_credentials.csv', 'r') as login_file:
            login_table = csv.reader(login_file, delimiter=',')
            next(login_table)
            for row in login_table:
                login_credentials.append(row)
        Login_btn = self.browser.find_element(By.XPATH, "//a[@href='#/login']")
        Login_btn.click()

        Password_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Password']")
        Email_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Email']")
        Signin_lgn_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
        assert Password_input.get_attribute('type') == "password"
        assert Signin_lgn_btn.is_displayed()

        current_credentials = random.choice(login_credentials)
        Email_input.send_keys(current_credentials[0])
        Password_input.send_keys(current_credentials[1])
        Signin_lgn_btn.click()

    def logout(self):
        time.sleep(1)
        Logout_btn = WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.XPATH, "//i[@class='ion-android-exit']")))
        assert Logout_btn.is_displayed()
        Logout_btn.click()

    def read_file(self, filename):
        global file_list
        file_list = []
        with open('vizsgaremek/Vizsgaremek_Python/'+str(filename), 'r') as opened_file:
            file_table = csv.reader(opened_file, delimiter=',')
            next(file_table)
            for row in file_table:
                file_list.append(row)

    def go_to_profile(self):
        time.sleep(2)
        self.browser.get('http://localhost:1667/#/@ChangedTestUser/')
        time.sleep(2)
        self.browser.refresh()
        time.sleep(2)
        edit_profile_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Edit Profile')]")
        assert edit_profile_btn.is_displayed()

    # Főoldal és gombjai vendégként

    def test_guest_home_page_items(self):
        Home_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Home')]")
        Conduit_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'conduit')]")
        Login_btn = self.browser.find_element(By.XPATH, "//a[@href='#/login']")
        Signup_btn = self.browser.find_element(By.XPATH, "//a[@href='#/register']")
        Pupular_tags = self.browser.find_elements(By.XPATH, "//p[text()='Popular Tags']/following-sibling::div//a[@class='tag-pill tag-default']")
        assert Conduit_btn.is_displayed()
        assert Login_btn.is_displayed()
        assert Signup_btn.is_displayed()
        assert Home_btn.is_displayed()

    # Adatkezelési nyilatkozat használata

    def test_accept_cookies(self):
        accept_cookies_btn = self.browser.find_element(By.XPATH, "//div[@class='cookie__bar__buttons']//button[contains(@class, 'accept')]")
        decline_cookies_btn = self.browser.find_element(By.XPATH, "//div[@class='cookie__bar__buttons']//button[contains(@class, 'decline')]")
        learn_more_btn = self.browser.find_element(By.XPATH, "//a[text()='Learn More...']")
        assert accept_cookies_btn.is_displayed() and decline_cookies_btn.is_displayed()
        accept_cookies_btn.click()
        time.sleep(1)
        assert not len(self.browser.find_elements(By.XPATH, "//div[@class='cookie__bar__buttons']//button[contains(@class, 'accept')]"))

    # Regisztráció

    def test_registration_page(self):

        # Beolvasás fileból
        self.read_file('signup_credentials.csv')
        
        # Regisztráció próbálkozások
        for attempt in file_list:
            Signup_btn = self.browser.find_element(By.XPATH, "//a[@href='#/register']")
            Signup_btn.click()

            Username_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Username']")
            Email_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Email']")
            Password_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Password']")
            Signup_reg_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]")
            Have_an_account_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Have an account?')]")
            Home_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Home')]")
            Conduit_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'conduit')]")
            Login_btn = self.browser.find_element(By.XPATH, "//a[@href='#/login']")
            Signup_btn = self.browser.find_element(By.XPATH, "//a[@href='#/register']")

            assert Password_input.get_attribute('type') == "password"
            assert Signup_reg_btn.is_displayed()

            Username_input.send_keys(attempt[0])
            Email_input.send_keys(attempt[1])
            Password_input.send_keys(attempt[2])
            Signup_reg_btn.click()

            success_icon = self.browser.find_element(By.XPATH, "//div[@class='swal-icon--success__ring']")
            popup_ok_btn = self.browser.find_element(By.XPATH, "//button[@class='swal-button swal-button--confirm']")
            time.sleep(1)
            assert success_icon.is_displayed() and popup_ok_btn.is_displayed()
            popup_ok_btn.click()
            time.sleep(2)
            self.logout()

    # Bejelentkezés

    def test_multiple_login(self):
        # Beolvasás fileból
        self.read_file('signup_credentials.csv')
        
        # Bejelentkezés próbálkozások
        for attempt in file_list:
            Login_btn = self.browser.find_element(By.XPATH, "//a[@href='#/login']")
            Login_btn.click()

            Password_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Password']")
            Email_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Email']")
            Signin_lgn_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
            Need_an_account_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Need an account?')]")
            Home_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'Home')]")
            Conduit_btn = self.browser.find_element(By.XPATH, "//a[contains(text(), 'conduit')]")
            Login_btn = self.browser.find_element(By.XPATH, "//a[@href='#/login']")
            Signup_btn = self.browser.find_element(By.XPATH, "//a[@href='#/register']")

            assert Password_input.get_attribute('type') == "password"
            assert Signin_lgn_btn.is_displayed()

            Email_input.send_keys(attempt[1])
            Password_input.send_keys(attempt[2])
            Signin_lgn_btn.click()

            self.logout()

    # Meglévő adat módosítás

    def test_data_change(self):
        # Bejelentkezés
        self.login()

        # Adatmódosítás
        profile_setting_btn = self.browser.find_element(By.XPATH, "//a[@href='#/settings']")
        profile_setting_btn.click()

        profile_pic_URL_input = self.browser.find_element(By.XPATH, "//input[@placeholder='URL of profile picture']")
        username_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Your username']")
        bio_input = self.browser.find_element(By.XPATH, "//textarea[@placeholder='Short bio about you']")
        update_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Update Settings')]")

        profile_pic_URL_input.clear()
        profile_pic_URL_input.send_keys('https://seeklogo.com/images/G/Galactic_Empire-logo-7A19A28ABA-seeklogo.com.png')
        username_input.clear()
        username_input.send_keys('ChangedTestUser')
        bio_input.clear()
        bio_input.send_keys('This is my modified bio')
        update_btn.click()

        successful_update_icon = self.browser.find_element(By.XPATH, "//div[@class='swal-icon--success__ring']")
        popup_ok_btn = self.browser.find_element(By.XPATH, "//button[@class='swal-button swal-button--confirm']")
        assert successful_update_icon.is_displayed()
        popup_ok_btn.click()

        # Böngésző frissítés és ellenőrzés
        self.browser.refresh()
        profile_pic_URL_input = self.browser.find_element(By.XPATH, "//input[@placeholder='URL of profile picture']")
        username_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Your username']")
        bio_input = self.browser.find_element(By.XPATH, "//textarea[@placeholder='Short bio about you']")
        assert profile_pic_URL_input.get_attribute('value') == 'https://seeklogo.com/images/G/Galactic_Empire-logo-7A19A28ABA-seeklogo.com.png'
        assert username_input.get_attribute('value') == 'ChangedTestUser'
        assert bio_input.get_attribute('value') == 'This is my modified bio'

    # Ismételt és sorozatos adatbevitel adatforrásból (új cikkek írása)

    def test_new_articles(self):
        # Bejelentkezés
        self.login()

        # Új cikk írása

        # beolvasás fileból
        self.read_file('multiple_articles.csv')
        # új cikk publikálása
        for article in file_list:
            new_article_btn = self.browser.find_element(By.XPATH, "//a[@href='#/editor']")
            new_article_btn.click()

            title_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Article Title']")
            about_input = self.browser.find_element(By.XPATH, "//input[contains(@placeholder, 'about')]")
            article_body_input = self.browser.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Write your article')]")
            tag_input = self.browser.find_element(By.XPATH, "//input[@placeholder='Enter tags']")
            publish_btn = self.browser.find_element(By.XPATH, "//button[contains(text(), 'Publish')]")

            title_input.send_keys(article[0])
            about_input.send_keys(article[1])
            article_body_input.send_keys(article[2])
            tag_input.send_keys(article[3])
            publish_btn.click()
            time.sleep(1)

            # ellenőrzés hogy a cikk a megfelelő adatokkal jött létre
            title_check = self.browser.find_element(By.XPATH, "//h1")
            body_check = self.browser.find_element(By.XPATH, "//div//p")
            tag_check = self.browser.find_elements(By.XPATH, "//a[@class='tag-pill tag-default']")
            tag_list = article[3].split(';')
            tag_list.pop(-1)

            assert title_check.text == article[0]
            assert body_check.text == article[2]
            for tag in tag_check:
                assert tag.text in tag_list

    # Új adat bevitel (új komment írása)

    def test_new_comment(self):
        self.login()

        article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
        random.choice(article_list).click()

        comment_body = self.browser.find_element(By.XPATH, "//textarea[contains(@placeholder, 'Write a comment')]")
        post_comment_btn = self.browser.find_element(By.XPATH, "//button[@class='btn btn-sm btn-primary']")

        comment = 'This is a test comment!'
        comment_body.send_keys(comment)
        post_comment_btn.click()

        time.sleep(1)

        comment_list = self.browser.find_elements(By.XPATH, "//p[@class='card-text']")
        comment_texts = []
        for comm in comment_list:
            comment_texts.append(comm.text)

        assert comment in comment_texts

    # Adatok lementése felületről (Adott felhasználó cikkeinek kimentése)

    def test_save_articles_to_file(self):
        # Bejelentkezés
        self.login()
        time.sleep(1)

        # Adott userhez navigálás
        self.browser.get('http://localhost:1667/#/@testuser1/')
        self.browser.refresh()
        time.sleep(1)

        # Adatok kimentése
        article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")

        with open('vizsgaremek/Vizsgaremek_Python/saved_article_details.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author', 'CreationDate', 'Body'])
            for x in range(len(article_list)):
                article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
                current_article = article_list[x]
                current_article.click()
                time.sleep(1)
                title = self.browser.find_element(By.XPATH, "//h1")
                author = self.browser.find_element(By.XPATH, "//a[@class='author']")
                date = self.browser.find_element(By.XPATH, "//span[@class='date']")
                article_body = self.browser.find_element(By.XPATH, "//div[@class='row article-content']/*/*/p")
                writer.writerow([title.text, author.text, date.text.replace(",", "."), article_body])
                self.browser.back()
                time.sleep(1)

        # Ellenőrzés title alapján

        self.browser.get('http://localhost:1667/#/@testuser1/')
        self.browser.refresh()
        time.sleep(1)

        saved_title_list = []
        with open('vizsgaremek/Vizsgaremek_Python/saved_article_details.csv', 'r') as file:
            title_table = csv.reader(file)
            next(title_table)
            for row in title_table:
                saved_title_list.append(row[0])
        time.sleep(1)
        article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
        for x in range(2):
            assert article_list[x].text in saved_title_list

    # Több oldalas lista bejárása

    def test_list_traversal(self):
        # Bejelentkezés
        self.login()

        # Feed ellenőrzése hogy vannak cikkek és léptető gombok
        article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
        assert len(article_list) >= 1
        page_btns = self.browser.find_elements(By.XPATH, "//ul[@class='pagination']//li")
        for button in page_btns:
            body = self.browser.find_element(By.XPATH, "//body")
            body.send_keys(Keys.END)
            if button.get_attribute('class') != 'page-item active':
                clickable_button = self.browser.find_elements(By.XPATH, "//li//a[@class='page-link']")[page_btns.index(button)]
                clickable_button.click()
                time.sleep(1)
                article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
                assert len(article_list) >= 1

    # Adat vagy adatok törlése

    def test_delete_my_articles(self):
        # Bejelentkezés
        self.login()
        time.sleep(1)

        # Profilhoz navigálás
        self.go_to_profile()

        # Cikkek törlése

        article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
        for x in range(len(article_list)):
            article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
            current_article = article_list[0]
            current_article.click()
            deleted_btn = WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.XPATH, "//i[@class='ion-trash-a']")))
            deleted_btn.click()
            self.go_to_profile()

        article_list = self.browser.find_elements(By.XPATH, "//a[@class='preview-link']//h1")
        assert len(article_list) == 0

#     # Kijelentkezés

#     def test_logout(self):
#         # Bejelentkezés
#         self.login()

#         # Kijelentkezés
#         Logout_btn = self.browser.find_element(By.XPATH, "//i[@class='ion-android-exit']")
#         assert Logout_btn.is_displayed()
#         Logout_btn.click()
#         Login_btn = self.browser.find_element(By.XPATH, "//a[@href='#/login']")
#         Signup_btn = self.browser.find_element(By.XPATH, "//a[@href='#/register']")
#         assert Login_btn.is_displayed()
#         assert Signup_btn.is_displayed()

#     # Adatok listázása (kimentés listába és megnézzük hogy nem üres-e a lista)(popular tag-ek)

#     def test_list_data(self):
#         # Bejelentkezés
#         self.login()

#         # Popular tag-ek kilistázása
#         tags_list = self.browser.find_elements(By.XPATH, "//div[@class='sidebar']//div[@class='tag-list']//a")
#         assert len(tags_list) > 1

