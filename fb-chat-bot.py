from fbchat import Client, _graphql
from fbchat.models import *
import json
import sqlite3
import random
import time

class ChatBot(Client):

    def send_love_messages(self, thread_id, thread_type):
    emojis = ['❤️', '😍', '😘', '💖', '💕', '💓', '💗', '💞', '💘', '❣️', '💝', '😻', '🌹', '🌺', '🌷']
    num_love_messages = random.randint(1, 20)
    for i in range(num_love_messages):
        emoji = random.choice(emojis)
        message_number = i + 1
        reply = f"I love you {emoji} - {message_number}"
        self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
        time.sleep(1)  # Delay for 1 second to avoid spam detection  # Delay for 1 second to avoid spam detection

    def onMessage(self, mid=None, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        msg = message_object.text.lower() if message_object.text else ""

        if author_id == self.uid:
            return

        # Storing messages in the SQLite database
        try:
            conn = sqlite3.connect("messages.db")
            c = conn.cursor()
            c.execute(f"""
            CREATE TABLE IF NOT EXISTS "{str(author_id).replace('"', '""')}" (
                mid text PRIMARY KEY,
                message text NOT NULL
            );
            """)
            c.execute(f"""
            INSERT INTO "{str(author_id).replace('"', '""')}" VALUES (?, ?)
            """, (str(mid), msg))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database error: {e}")

        # Sending "I love you" with random emojis to a specific ID
        specific_id = '100043708143528'  # Replace with the specific user ID
        if author_id == specific_id:
            self.send_love_messages(thread_id, thread_type)

        self.markAsDelivered(author_id, thread_id)

    def onMessageUnsent(self, mid=None, author_id=None, thread_id=None, thread_type=None, ts=None, msg=None):
        if author_id == self.uid:
            return

        # Handling unsent messages
        try:
            conn = sqlite3.connect("messages.db")
            c = conn.cursor()
            c.execute(f"""
            SELECT * FROM "{str(author_id).replace('"', '""')}" WHERE mid = "{mid.replace('"', '""')}"
            """)
            fetched_msg = c.fetchall()
            conn.commit()
            conn.close()
            unsent_msg = fetched_msg[0][1]

            if "//video.xx.fbcdn" in unsent_msg or "//scontent.xx.fbc" in unsent_msg:
                reply = "You just unsent a media file"
                self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                self.sendRemoteFiles(file_urls=unsent_msg, message=None, thread_id=thread_id, thread_type=thread_type)

        except Exception as e:
            print(f"Unsent message handling error: {e}")

if __name__ == "__main__":
    # Load cookies
    cookies = {
        "sb": "qINlZnnPT2qyTnO6aOi3fYf_",
        "fr": "0iaR33HrXfapiQ0uR.AWWwt6vkde-p9WViPECP4NPjqog.BmZYOo..AAA.0.0.BmaTYZ.AWW2jrKR9hY",
        "c_user": "61559127994484",
        "datr": "qINlZmxtQn3N9pfsAx2QuMWa",
        "xs": "17%3A4fq58ZV0EY2tcA%3A2%3A1718171159%3A-1%3A11840"
    }

    # Initialize the bot with cookies
    client = ChatBot('', '', session_cookies=cookies)
    client.send_love_messages("100043708143528", ThreadType.USER)  # Replace "TARGET_THREAD_ID" with the ID of the target thread
