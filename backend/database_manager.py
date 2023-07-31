"""
Database Manager for VoxFlow
"""
import json
import sqlite3
from random import choice, randint
from string import printable
from time import time as time_since_unix_epoch
from typing import Union

import jwt
from pyargon2 import hash as pwd_hash_function
from aiohttp.web import json_response



class DatabaseManager:
    """
    for easy db management
    """

    def __init__(self) -> None:
        self.conn = sqlite3.connect("./database/data.db")
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
        with open("./database/config/config.json", encoding="utf-8") as f:
            config = json.load(f)
        return jwt.encode(
            {
                "user_id": user_id,
                "exp": int(time_since_unix_epoch()) + (60 * 60 * 24 * 30),
            },
            config["token_secret"],
        )

    def _validate_token(self, token) -> dict:
        sql = """SELECT user_id FROM tokens WHERE token=?"""
        self.cursor.execute(sql, (token))
        user_id = self.cursor.fetchone()
        if not user_id:
            return {"reason": "You are not authorized to access this resource"}
            
        return {"user_id":user_id}

    def create_user(self, data):
        """
        Method for adding a new user to the database
        For Internal use Only
        """
        username = data["username"]

        salt = self._create_salt()
        password_hash = self._hash_password(username, data["password"])
        user_id = self._create_user_snowflake()
        sql = """
            INSERT INTO users (user_id, username, email,salt, password_hash, system_prompt)
            VALUES (?,?,?, ?, ?, ?, ?)
        """

        self.cursor.execute(
            sql,
            (
                user_id,
                username,
                data["email"],
                salt,
                password_hash,
                data["bot_name"],
                data["system_prompt"],
            ),
        )
        self.conn.commit()
        return {"user_id": user_id,"username":username,"email":data["email"],"bot_name":data["bot_name"],"system_prompt":data["system_prompt"]}

    def auth_user(self, email, password):
        """
        Method for authenticating existing user to the application
        For Internal use Only
        """
        sql = """SELECT user_id,salt,password_hash FROM users WHERE email=?"""
        self.cursor.execute(sql, (email,))
        user: tuple = self.cursor.fetchone()
        user_id, salt, password_hash = user[0], user[1], user[2]
        if self._hash_password(password, salt) == password_hash:
            token = self._token_generator(user_id)
            sql = """INSERT INTO tokens (user_id,token) VALUES (?,?)"""
            self.cursor.execute(sql, (user_id, token))
            self.conn.commit()
            return {"token": token, "user_id": user_id}

        return {"reason": "You are unauthorised to access this service"}
        

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
        user_id = self._validate_token(token)["user_id"] if self._validate_token(token)["user_id"] else None
        created = time_since_unix_epoch()
        message_id = self._create_message_snowflake()
        sql = (
            """INSERT INTO prompts (message_id,user_id,prompt,response,created) VALUES (?,?,?,?)"""
        )
        self.cursor.execute(sql, (message_id,user_id, prompt, response, created))
        self.conn.commit()
        return {"message_id":message_id,"user_id":user_id,"created":created}


    def list_prompts(self, token):
        """
        Method for listing messages/prompts from the database
        For Internal use Only
        """
        user_id = self._validate_token(token)["user_id"] if self._validate_token(token)["user_id"] else None
        sql = """SELECT * FROM prompts WHERE user_id=?"""
        self.cursor.execute(sql, (user_id,))
        #Usable format
        prompts = []
        for message_id,_,prompt,response,created in self.cursor.fetchall():
            prompts.append({"message_id":message_id,"user_id":user_id,"prompt":prompt,"response":response,"created":created})
        return {"user_id":user_id,"prompts":prompts}


    def _delete_earliest_prompt(self, token):
        prompt_ids = [self.list_prompts(token)["prompts"]["message_id"]]
        sorted_prompts =sorted(prompt_ids)
        sql = """DELETE FROM prompts WHERE prompt_id=?"""
        self.cursor.execute(sql, (sorted_prompts[0],))
        self.conn.commit()

    def delete_all_prompts(self):
        """
        Method for changing user credentials
        For Internal Use Only
        """