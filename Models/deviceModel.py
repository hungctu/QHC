from Models.DeviceCodeModel import DeviceCodeModel
from Models.IpCodeModel import IpCodeModel
from database import Database
from datetime import datetime, timedelta

class deviceModel:
    def __init__(self):
        self.db = Database()

    def createDevice(self,device):
        try:
            query = """INSERT INTO `device`(`device_name`) VALUES (%s)"""
            self.db.execute(query, (device,))
            return True
        except Exception as e:
            return False

    def getDeviceId(self,device):
        query = """SELECT id FROM `device` WHERE device_name=%s"""
        return self.db.fetch_one(query, (device,))

    def checkDevice(self, device_name):
        try:
            # Kiểm tra xem IP có tồn tại trong cơ sở dữ liệu không
            query = """SELECT COUNT(id) AS nums FROM device WHERE device_name = %s"""
            result = self.db.fetch_one(query, (device_name,))
            print(result['nums'])
            if result['nums'] == 0:
                # Nếu IP chưa tồn tại, tạo mới
                ip = self.createDevice(device_name)
                if ip:
                    return {
                        'status': True,
                        'isCreate': True,
                        'hasCode':False,
                        'message': 'Add User Device successful'
                    }
                else:
                    return {
                        'status': False,
                        'isCreate': True,
                        'hasCode': False,
                        'error': 'Add User Device failed'
                    }
            else:
                ic = DeviceCodeModel()
                result = ic.lastDategetCode(device_name)
                if result['status']==False:
                    return {
                        'status': False,
                        'isCreate': False,
                        'hasCode': False,
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
                            'hasCode': True,
                            'last_code_time': last_code_time,
                            'device_name':device_name
                        }

                return {
                    'status': True,
                    'isCreate': False,
                    'hasCode': False,
                    'message': 'IP can receive a new code.'
                }

        except Exception as e:
            return {
                'status': False,
                'isCreate': False,
                'error': str(e)
            }
