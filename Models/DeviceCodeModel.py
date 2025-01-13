from database import Database
from datetime import datetime, timedelta


class DeviceCodeModel:
    def __init__(self):
        self.db = Database()

    def lastDategetCode(self, device_name):
        try:
            query = """
                SELECT MAX(get_code_at) AS last_code_time 
                FROM device_code dc
                JOIN device d ON dc.device_id = d.id
                WHERE d.device_name = %s
            """
            result = self.db.fetch_one(query, (device_name,))
            print(result['last_code_time'])
            return {
                'status': True,
                'last_code_time': result['last_code_time']
            }
        except Exception as e:
            print(f"Error when get last date get code: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def createDeviceCode(self, code_id, code_type, device_id):
        try:
            query = """INSERT INTO `device_code`(`code_id`, `code_type`, `device_id`) VALUES (%s,%s,%s)"""
            self.db.execute(query, (code_id, code_type, device_id,))
            return True
        except Exception as e:
            print(f'Error when add IpCode data to DB: {e}')
            return False