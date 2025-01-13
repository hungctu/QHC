from database import Database
from datetime import datetime, timedelta

class IpCodeModel:
    def __init__(self):
        self.db = Database()
        
    def lastDategetCode(self,IP):
        try:
            query = """
                SELECT MAX(get_code_at) AS last_code_time 
                FROM ip_code ic 
                JOIN userip u ON ic.ip_id = u.id
                WHERE u.IP = %s
            """
            result = self.db.fetch_one(query, (IP,))

            return {
                'status':True,
                'last_code_time':result['last_code_time']
            }
        except Exception as e:
            print(f"Error when get last date get code: {e}")
            return{
                'status':False,
                'error': str(e)
            }

    def createIpCode(self,code_id,code_type,ip_id):
        try:
            query="""INSERT INTO `ip_code`(`code_id`, `code_type`, `ip_id`) VALUES (%s,%s,%s)"""
            self.db.execute(query,(code_id,code_type,ip_id,))
            return True
        except Exception as e:
            print(f'Error when add IpCode data to DB: {e}')
            return False