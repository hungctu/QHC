from Models.IpCodeModel import IpCodeModel
from database import Database
from datetime import datetime, timedelta

class userIpModel:
    def __init__(self):
        self.db = Database()

    def createIP(self,IP):
        try:
            query = """INSERT INTO `userip`(`IP`) VALUES (%s)"""
            self.db.execute(query, (IP,))
            return True
        except Exception as e:
            return False

    def getIpId(self,IP):
        query = """SELECT id FROM `userip` WHERE IP=%s"""
        return self.db.fetch_one(query, (IP,))

    def checkIP(self, IP):
        try:
            # Kiểm tra xem IP có tồn tại trong cơ sở dữ liệu không
            query = """SELECT COUNT(id) AS nums FROM userip WHERE IP = %s"""
            result = self.db.fetch_one(query, (IP,))

            if result['nums'] == 0:
                # Nếu IP chưa tồn tại, tạo mới
                ip = self.createIP(IP)
                if ip:
                    return {
                        'status': True,
                        'isCreate': True,
                        'message': 'Create IP successful'
                    }
                else:
                    return {
                        'status': False,
                        'isCreate': True,
                        'error': 'Create IP failed'
                    }
            else:
                ic = IpCodeModel()
                result = ic.lastDategetCode(IP)
                if result['status']==False:
                    return {
                        'status': False,
                        'isCreate': False,
                        'error': result['error']
                    }
                last_code_time = result['last_code_time']

                if last_code_time:
                    # Kiểm tra xem thời gian có quá 1 giờ không
                    one_hour_ago = datetime.now() - timedelta(hours=1)
                    if last_code_time > one_hour_ago:
                        return {
                            'status': False,
                            'isCreate': False,
                            'error': 'IP cannot receive a new code yet. Wait for 1 hour.'
                        }

                return {
                    'status': True,
                    'isCreate': False,
                    'message': 'IP can receive a new code.'
                }

        except Exception as e:
            return {
                'status': False,
                'isCreate': False,
                'error': str(e)
            }
