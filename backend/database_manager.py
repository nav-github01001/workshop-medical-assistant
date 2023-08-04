"""
Database Manager for VoxFlow
"""

import sqlite3
from random import choice, randint
from string import printable
from time import time as time_since_unix_epoch
import tomllib
import jwt
from pyargon2 import hash as pwd_hash_function

with open("./config.toml") as f:
    config = tomllib.loads(f.read())


class DatabaseManager:
    """
    for easy db management
    """

    def __init__(self) -> None:
        self.conn = sqlite3.connect("./backend/data.db")
        self.cursor = self.conn.cursor()

    def _create_salt(self):
        salt = ""
        for _ in range(512):
            salt += choice(list(printable[:93]))
        return salt

    def _create_user_snowflake(self):
        return int(time_since_unix_epoch()) * 100000 + randint(0, 99999)
    
    def _create_message_snowflake(self):
        return int(time_since_unix_epoch()) * 10000000 + randint(0, 9999999)

    def _hash_password(self, password, salt):
        return pwd_hash_function(
            password, salt, time_cost=75, parallelism=4, hash_len=64, encoding="raw"
        )

    def _token_generator(self, user_id):
        return jwt.encode(
            {
                "user_id": user_id,
                "exp": int(time_since_unix_epoch()) + (60 * 60 * 24 * 10),
            },
            config["token_secret"],
        )

    def _validate_token(self, token):
        return jwt.decode(token,config["token_secret"],["HS256"])

    def create_user(self, data):
        """
        Method for adding a new user to the database
        For Internal use Only
        """
        username = data["username"]
        password = data["password"]
        if len(password) < 8:
            return {"reason":"Password should be 8 letters or more"},400

        salt = self._create_salt()
        password_hash = self._hash_password(password,salt)
      
        user_id = self._create_user_snowflake()
        sql = """
            INSERT INTO users(user_id, username, email,salt,password_hash)
            VALUES (?,?,?, ?, ?)
        """

        self.cursor.execute(
            sql,
            (
                user_id,
                username,
                data["email"],
                salt,
                password_hash,
            
            ),
        )
        self.conn.commit()
        token = self._token_generator(user_id)
        return {"user_id": user_id,"token":token,"username":username,"email":data["email"]},201

    def auth_user(self, data):
        """
        Method for authenticating existing user to the application
        For Internal use Only
        """
        email = data["email"]
        password = data["password"] 
        try:
            sql = """SELECT user_id,username,salt,password_hash FROM users WHERE email=?"""
            self.cursor.execute(sql, (email,))
            user_id,username,salt, password_hash =self.cursor.fetchone()
            if self._hash_password(password, salt) == password_hash:
                token = self._token_generator(user_id)
                return {"jwt":token,"user_id":user_id,"username":username,"email":email},200
            else:
                return {"reason": "Invalid Credentials"},401
        except:
            return {"reason": "Email doesnt Exist"},401
        

    # TODO:Add methods

    def update_user_email(self):
        """
        Method for changing user email
        For Internal Use Only
        """

    def update_user_password(self):
        """
        Method for changing user credentials
        For Internal Use Only
        """

    def delete_user(self):
        """
        Method for changing user credentials
        For Internal Use Only
        """

    def create_prompt(self, token, prompt, response):
        """
        Method for adding a new message/prompt to the database
        For Internal use Only
        """
        try:
            user_id = self._validate_token(token)["user_id"]
        except jwt.exceptions.DecodeError:
            return {"reason":"Invalid Token"},401
        created = time_since_unix_epoch()
        message_id = self._create_message_snowflake()
        sql = (
            """INSERT INTO prompts (message_id,user_id,prompt,response,created) VALUES (?,?,?,?,?)"""
        )
        self.cursor.execute(sql, (message_id,user_id, prompt, response, created))
        self.conn.commit()
        return {"message_id":message_id,"user_id":user_id,"response":response,"created":created},200


    def list_prompts(self, token):
        """
        Method for listing messages/prompts from the database
        For Internal use Only
        """
        try:
            user_id = self._validate_token(token)["user_id"]
        except jwt.exceptions.DecodeError:
            return {"reason":"Invalid Token"},401
        sql = """SELECT * FROM prompts WHERE user_id=?"""
        self.cursor.execute(sql, (user_id,))
        #Usable format
        prompts = []
        for message_id,_,prompt,response,created in self.cursor.fetchall():
            prompts.append({"message_id":message_id,"user_id":user_id,"prompt":prompt,"response":response,"created":created})
        if len(prompts) == 20:
            self._delete_earliest_prompt(token)
        return {"user_id":user_id,"prompts":prompts},200


    def _delete_earliest_prompt(self, token):
        prompt_ids = [prompt["message_id"] for prompt in self.list_prompts(token)["prompts"]]
        sorted_prompts =sorted(prompt_ids)
        sql = """DELETE FROM prompts WHERE prompt_id=?"""
        self.cursor.execute(sql, (sorted_prompts[0],))
        self.conn.commit()

    def delete_all_prompts(self):
        """
        Method for changing user credentials
        For Internal Use Only
        """