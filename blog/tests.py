from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from blog.views import post_list, cv_page, cv_new

# Create your tests here.

# Test CV page and test New CV Entry page


class CVTest(TestCase):
    def test_cv_page_displays_correct_sections(self):
        # Name, Bio, Sections
        request = HttpRequest()
        response = cv_page(request)
        html = response.content.decode('utf8').strip()
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Ben Gray\'s Django Coursework Blog</title>',
                      html)

        # Check HTML for:
        #   1. Title
        self.assertIn('<h1>Ben Gray</h1>', html)

        #   2. Each Section
        self.assertIn('<div id="section-education">', html)
        self.assertIn('<div id="section-work">', html)
        self.assertIn('<div id="section-skills">', html)
        self.assertIn('<div id="section-interests">', html)
        self.assertIn('<div id="section-misc">', html)

        self.assertTrue(html.endswith('</html>'))

    def test_cv_form_includes_correct_fields(self):
        # Form Fields
        request = HttpRequest()
        response = cv_new(request)
        html = response.content.decode('utf8').strip()
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>Ben Gray\'s Django Coursework Blog</title>',
                      html)

        # Check HTML for:

        #   1. Header
        self.assertIn('<h2>New CV Entry</h2>', html)

        #   2. Sections
        self.assertIn('<li>Bio (Overwrites)</li>', html)
        self.assertIn('<li>Education</li>', html)
        self.assertIn('<li>Work Experience</li>', html)
        self.assertIn('<li>Additional Skills/Achievements</li>', html)
        self.assertIn('<li>Interests</li>', html)
        self.assertIn('<li>Miscellaneous</li>', html)

        #   3. Section Input
        self.assertIn('id="id_section"', html)

        #   4. Text Input
        self.assertIn('id="id_text"', html)

        #   5. Date Inputs
        self.assertIn('id="id_start_date"', html)
        self.assertIn('id="id_end_date"', html)

        #   6. Submit Button
        self.assertIn('<button type="submit" class="save', html)

        self.assertTrue(html.endswith('</html>'))
