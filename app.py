import os

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

def unsafe_eval(user_input):
    return eval(user_input)