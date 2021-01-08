import unittest

from selenium import webdriver


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://localhost")

    def testCorrectLoginIncorrectPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("wrongpass")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        msg_field = self.driver.find_elements_by_xpath("//div[@class='msg']")
        msg_field_text = msg_field.pop().text
        assert msg_field_text == 'Incorrect username/password!'

    def testCorrectLoginEmptyPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert password_field.get_attribute("validationMessage") == "Please fill out this field."

    def testEmptyLoginCorrectPassword(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Login']").click()
        assert username_field.get_attribute("validationMessage") == "Please fill out this field."

    def tearDown(self):
        self.driver.close()


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1/pythonlogin/register")

    def testEmptyUsernameCorrectPasswordCorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert username_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameEmptyPasswordCorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()
        email_field.send_keys("test@test.com")

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert password_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameCorrectPasswordEmptyEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert email_field.get_attribute("validationMessage") == "Please fill out this field."

    def testCorrectUsernameCorrectPasswordIncorrectEmail(self):
        username_field = self.driver.find_element_by_id("username")
        username_field.clear()
        username_field.send_keys("test")

        password_field = self.driver.find_element_by_id("password")
        password_field.clear()
        password_field.send_keys("test")

        email_field = self.driver.find_element_by_id("email")
        email_field.clear()

        self.driver.find_element_by_xpath("//input[@type='submit' and @value='Register']").click()
        assert email_field.get_attribute("validationMessage") == "Please fill out this field."

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
