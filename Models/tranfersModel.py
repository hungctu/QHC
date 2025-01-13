from database import Database
from dotenv import load_dotenv
import os

load_dotenv()

class transferModel:
    def __init__(self):
        self.db = Database()

    def addTransfer(self,wallet_id,code,QHC,hash):
        try:
            query = 'INSERT INTO transfers(`main_wallet_address`, `wallet_id`, `code`, `QHC`, `Tx_hash`) VALUES (%s,%s,%s,%s,%s)'
            self.db.execute(query,(os.getenv('MAIN_WALLET_ADDRESS'),wallet_id,code,QHC,hash,))
            return True
        except Exception as e:
            print(f"Error when add Transfer data to DB: {e}")
            return False

    def addWP(self,code,user_agent,order_id):
        try:
            query = 'INSERT INTO wordpress(`code`, `user_agent`, `order_id`) VALUES (%s,%s,%s)'
            self.db.execute(query,(code,user_agent,order_id,))
            return True
        except Exception as e:
            print(f"Error when add WP data to DB: {e}")
            return False