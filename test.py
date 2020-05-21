import unittest
from app import app, homepage, questions, collect_responses, survey_end, summary
from surveys import satisfaction_survey
from flask import session

class TestFlaskSurvey(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "secret"
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    def test_get_method_on_homepage(self):
        with self.client as client:
            '''tests valid method'''
            response = client.get('/')
            self.assertTrue(response.status_code == 200)

    def test_post_method_on_homepage(self):
        with self.client as client:
            '''tests invalid request method'''
            response = client.post('/')
            self.assertTrue(response.status_code != 200)

    def test_invalid_method_on_questions(self):
        with self.client as client:
            '''tests invalid requests method'''
             response = client.put('/questions/0')
             self.assertTrue(response.status_code != 200)

