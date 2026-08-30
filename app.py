import os

def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return query

def delete_user(user_id):
    os.system("rm -rf /data/" + user_id)