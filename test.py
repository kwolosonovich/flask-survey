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
        '''tests valid method'''
        with self.client as client:
            response = client.get('/')
            self.assertTrue(response.status_code == 200)

    def test_post_method_on_homepage(self):
        '''tests invalid request method'''
        with self.client as client:
            response = client.post('/')
            self.assertTrue(response.status_code != 200)

    def test_invalid_method_on_questions(self):
        '''tests invalid requests method'''
        with self.client as client:
             response = client.put('/questions/0')
             self.assertTrue(response.status_code != 200)


