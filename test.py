import unittest
from app import app, homepage, questions, collect_responses, survey_end, summary
from surveys import satisfaction_survey
from flask import session, jsonify

class TestFlaskSurvey(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "secret"
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        self.session_key = "responses"

# test homepage route
    def test_get_method_on_homepage(self):
        '''Tests valid method'''
        with self.client as client:
            response = client.get('/')
            self.assertTrue(response.status_code == 200)

    def test_post_method_on_homepage(self):
        '''Tests invalid request method'''
        with self.client as client:
            response = client.post('/')
            self.assertTrue(response.status_code != 200)

# test question route
    def test_invalid_method_on_questions(self):
        '''Tests invalid requests method'''
        with self.client as client:
             response = client.put('/questions/0')
             self.assertTrue(response.status_code != 200)

    def test_question_id_greater_than_number_of_responses(self):
        '''Test impossible guestion_id param'''
        with self.client.session_transaction() as session:
            session[self.session_key] = []

        answers = session[self.session_key]
        with self.client as client:
            number_of_answers = len(answers)
            response = client.post(f"/questions/{number_of_answers + 1}")
            # should return re-direct status code
            self.assertTrue(response.status_code == 302)

    def test_if_all_questions_answered(self):
        with self.client.session_transaction() as session:
            session[self.session_key] = [True] * len(satisfaction_survey.questions)

        answers = session[self.session_key]
        with self.client as client:
            number_of_answers = len(answers)
            response = client.post(f"/questions/{number_of_answers}")
            self.assertTrue(response.status_code == 302)
#
#     def test_impossible_satisfaction_survey_len(self):
#         '''Test impossible satisfaction survey length'''
#         assert False
#
#     def test_invalid_redirect_function(self):
#         '''Test invalid redirect'''
#         assert False
#
# # test responses route
#     def test_get_method_on_responses(self):
#         '''Test invalid method'''
#         with self.client as client:
#             response = client.get('/responses')
#             self.assertFalse(response.status_code == 200)
#
#
#     def test_impossible_responses(self):
#         '''Test impossible responses from session[SESSION_KEY]'''
#         assert False
#
#     def test_impossible_answer(self):
#         '''Test impossible answer from option'''
#         assert False
#
#     def test_impossible_survey_length(self):
#         '''Test impossible survey_length from satisfaction_survey.questions'''
#         assert False
#
# # test survey_end
#     def test_invalid_method_on_survey_end(self):
#         '''Test invalid method'''
#         with self.client as client:
#             response = client.get('/survey_end')
#             self.assertFalse(response.status_code != 200)
#
#     def test_invalid_render_template_response(self):
#         '''Test invalid response'''
#         assert False
#
    def test_invalid_method_on_summary(self):
        '''Test invalid method'''
        with self.client as client:
            response = client.post('/summary')
            self.assertTrue(response.status_code != 200)

    def test_valid_method_on_summary(self):
        with self.client as client:
            response = client.get('/summary')
            self.assertTrue(response.status_code == 200)
