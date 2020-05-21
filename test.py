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
        answers = []
        with self.client.session_transaction() as session:
            session[self.session_key] = answers

        with self.client as client:
            number_of_answers = len(answers)
            response = client.get(f"/questions/{number_of_answers + 1}")
            # should return re-direct status code
            self.assertTrue(response.status_code == 302)
            self.assertIn(f'/questions/{number_of_answers}', response.headers["Location"])

    def test_if_all_questions_answered(self):
        '''Test if number of questions equals number of answers to prevent question skips'''
        with self.client.session_transaction() as session:
            session[self.session_key] = [True] * len(satisfaction_survey.questions)

        answers = session[self.session_key]
        with self.client as client:
            number_of_answers = len(answers)
            response = client.post(f"/questions/{number_of_answers}")
            self.assertTrue(response.status_code == 302)


# test responses
    def test_invalid_method_on_responses(self):
        '''Test invalid method'''
        with self.client as client:
            response = client.get('/responses')
            self.assertFalse(response.status_code == 200)

    def test_invalid_answer(self):
        '''Test impossible answer from option'''
        with self.client.session_transaction() as session:
            session[self.session_key] = []

        answer = {}
        with self.client as client:
            response = client.post("/responses", data=answer)
            self.assertTrue(response.status_code == 302)

    def test_prompt_next_question(self):
        '''Test if next question is rendered if not last question'''
        responses = [True]
        with self.client.session_transaction() as session:
            # single response should redirect to question 2
            session[self.session_key] = responses
        answer = {'option': True}
        with self.client as client:
            response = client.post('/responses', data=answer)
            self.assertTrue(response.status_code == 302)
            self.assertIn(f"/questions/{len(responses) +1}", response.headers["Location"])
            # self.assertIn(f"/questions/{len(responses) +1}", response.data.decode("utf-8"))

    def test_promt_servey_end(self):
        '''Test if survey end is rendered after the last question is completed'''
        responses = [True, True, True]
        with self.client.session_transaction() as session:
            # response should redirect to survey end
            session[self.session_key] = responses
        answer = {'option': True}
        with self.client as client:
            response = client.post('/responses', data=answer)
            self.assertTrue(response.status_code == 302)
            self.assertIn("/survey_end", response.headers['location'])


# test survey_end
    def test_valid_method_on_survey_end(self):
        '''Test Valid method'''
        with self.client as client:
            response = client.get('/survey_end')
            self.assertTrue(response.status_code == 200)

    def test_invalid_method_on_survey_end(self):
        '''Test invalid method'''
        with self.client as client:
            response = client.get('/survey_end')
            self.assertFalse(response.status_code != 200)


# test summary
    def test_invalid_method_on_summary(self):
        '''Test invalid method'''
        with self.client as client:
            response = client.post('/summary')
            self.assertTrue(response.status_code != 200)

    def test_valid_method_on_summary(self):
        with self.client as client:
            response = client.get('/summary')
            self.assertTrue(response.status_code == 200)
