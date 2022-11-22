class Question(): 
    def __init__(self, category, q_type, difficulty, question, correct_answer, incorrect_answers = []):
        self.category = category
        self.q_type = q_type
        self.difficulty = difficulty
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers

    def get_category(self):
        return self.category
    def get_type(self):
        return self.q_type
    def get_difficulty(self):
        return self.difficulty
    def get_correct_answer(self):
        return self.correct_answer
    def get_question(self):
        return self.question
    def get_incorrect_answers(self):
        return self.incorrect_answers


    