from selenium import webdriver
import unittest
import time


class CVTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def admin_login(self):
        # Log in to admin to enable write/edit
        self.browser.get("http://localhost:8000/admin")
        self.browser.find_element_by_id("id_username").send_keys("ben")
        self.browser.find_element_by_id("id_password").send_keys(
            "k3$*Z^8EgSFiHfc^R^$T")
        self.browser.find_element_by_tag_name("form").submit()
        time.sleep(1)

    def test_cv_form(self):
        # Test adding an item to the cv

        # Login to admin
        self.admin_login()

        # User loads the correct page
        self.browser.get('http://localhost:8000/cv/new')

        # User sees the title allows them to create a new item
        title_text = self.browser.find_element_by_tag_name('h2').text
        self.assertIn("New", title_text)

        # User reads section numbers
        header_text = self.browser.find_element_by_tag_name('h4').text
        self.assertIn("Sections", header_text)

        section_list = self.browser.find_element_by_tag_name(
            'ol').get_attribute('innerHTML')
        for section in [
                "Bio", "Education", "Work", "Skills", "Interests", "Misc"
        ]:
            self.assertIn(section, section_list)

        # User is invited to input a section number
        section_input = self.browser.find_element_by_id("id_section")
        section_input.send_keys("2")

        entry_text = "Ecotricity - Bill Resolution Specialist"

        # User inputs some text
        text_input = self.browser.find_element_by_id("id_text")
        text_input.send_keys(entry_text)

        # User inputs a start and end date
        start_date_input = self.browser.find_element_by_id("id_start_date")
        start_date_input.send_keys("dd/mm/yyyy")

        end_date_input = self.browser.find_element_by_id("id_end_date")
        end_date_input.send_keys("dd/mm/yyyy")

        # Check the user can submit the form
        save_button = self.browser.find_elements_by_class_name("save")
        self.assertTrue(len(save_button) > 0)

        # User submits form data
        self.browser.find_element_by_tag_name("form").submit()

        # Wait for entry to be added
        time.sleep(1)

        # User goes to CV page
        self.browser.get("http://localhost:8000/cv")

        # User finds correct section
        section = self.browser.find_element_by_id("section-work")
        self.assertTrue(
            section.find_element_by_tag_name("h4").text == "Work Experience")

        # User reads recently inputted item under correct section
        section_entries = section.find_elements_by_tag_name("li")
        self.assertTrue(
            any(entry.text == entry_text for entry in section_entries))


if __name__ == '__main__':
    unittest.main(warnings='ignore')