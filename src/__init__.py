from src.app import create_app
import pymysql
app = create_app('sqlite:///test.db')
# app = create_app('mysql+pymysql://bbb0a323508cb9:e0aac45a@us-cdbr-east-04.cleardb.com/heroku_aea8a1d64f8ff0c')

if __name__ == "__main__":
    app.run()
