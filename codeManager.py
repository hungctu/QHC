from Models.deviceModel import deviceModel
from Models.qhcAModel import qhcAModel
from Models.qhcBModel import qhcBModel
from Models.qhcCModel import qhcCModel
from Models.qhcDModel import qhcDModel
from Models.tranfersModel import transferModel
from Models.userIpModel import userIpModel


class codeManager:
    def __init__(self):
        pass

    def addNumsCode(self,nums, type):
        match type:
            case 'qhc_a':
                handler = qhcAModel()
            case 'qhc_b':
                handler = qhcBModel()
            case 'qhc_c':
                handler = qhcCModel()
            case 'qhc_d':
                handler = qhcDModel()
            case _:
                raise ValueError("Invalid code: Does not start with a valid character")

        return handler.addCodes(nums)


    def getCode(self,device):
        try:
            ud = deviceModel()
            check = ud.checkDevice(device)
            handler = qhcCModel()
            if check['status'] == False:
                if check['hasCode']==True:
                    nearestCode = handler.getNearestCode(check['last_code_time'],check['device_name'])
                    return {
                        'status': True,
                        'code': nearestCode['result']['code'],
                        'unit': nearestCode['result']['unit']
                }
                return {
                    'status': False,
                    'error': check['error']
                }
            id = ud.getDeviceId(device)['id']

            code = handler.getCodeForUser(id)

            return code
        except Exception as e:
            print(f"Error while finding code: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def buyCode(self,tx_hash,customer,amount):
        try:

            match amount:
                case 0.001:
                    handler = qhcAModel()
                case 0.01:
                    handler = qhcBModel()
                case 0.1:
                    handler = qhcCModel()
                case 1:
                    handler = qhcDModel()
                case _:
                    raise ValueError("Invalid code: Does not start with a valid character")

            return handler.buyCode(tx_hash, customer)
        except Exception as e:
            print(f"Error while finding code: {e}")
            return {
                    'status': False,
                    'error': str(e)
                }

    def UseCode(self, code,address):
        try:
            print(code)
            first_char = code[0].lower()  # Lấy ký tự đầu tiên và chuyển về chữ thường (nếu cần)

            match first_char:
                case 'a':
                    handler = qhcAModel()
                case 'b':
                    handler = qhcBModel()
                case 'c':
                    handler = qhcCModel()
                case 'd':
                    handler = qhcDModel()
                case _:
                    raise ValueError("Invalid code: Does not start with a valid character")

            return handler.transaction(code,address)
        except Exception as e:
            print(f"Error while finding code: {e}")
            return {
                    'status': False,
                    'error': str(e)
                }

    def useCodeOnWP(self, code):
        try:
            print(code)
            first_char = code[0].lower()  # Lấy ký tự đầu tiên và chuyển về chữ thường (nếu cần)

            match first_char:
                case 'a':
                    handler = qhcAModel()
                case 'b':
                    handler = qhcBModel()
                case 'c':
                    handler = qhcCModel()
                case 'd':
                    handler = qhcDModel()
                case _:
                    raise ValueError("Invalid code: Does not start with a valid character")

            return handler.useCodeOnWP(code)
        except Exception as e:
            print(f"Error while finding code: {e}")
            return {
                    'status': False,
                    'error': str(e)
                }

    def updateCodeUsedOnWP(self,code,user_agent,order_id):
        try:
            print(code)
            first_char = code[0].lower()  # Lấy ký tự đầu tiên và chuyển về chữ thường (nếu cần)

            match first_char:
                case 'a':
                    handler = qhcAModel()
                case 'b':
                    handler = qhcBModel()
                case 'c':
                    handler = qhcCModel()
                case 'd':
                    handler = qhcDModel()
                case _:
                    raise ValueError("Invalid code: Does not start with a valid character")

            updateCodeIsUsed = handler.updateCodeIsUsed(code,1)
            if updateCodeIsUsed['status']==False:
                return updateCodeIsUsed

            tm = transferModel()
            addWP = tm.addWP(code,user_agent,order_id)
            if addWP['status']:
                return addWP
            return {
                    'status': False,
                    'message': 'Updated code used successfully'
                }

        except Exception as e:
            print(f"Error while finding code: {e}")
            return {
                    'status': False,
                    'error': str(e)
                }

    def getUnit(self,code):
        try:
            first_char = code[0].lower()  # Lấy ký tự đầu tiên và chuyển về chữ thường (nếu cần)

            match first_char:
                case 'a':
                    handler = qhcAModel()
                case 'b':
                    handler = qhcBModel()
                case 'c':
                    handler = qhcCModel()
                case 'd':
                    handler = qhcDModel()
                case _:
                    raise ValueError("Invalid code: Does not start with a valid character")

            return handler.getCodeUnit(code)
        except Exception as e:
            print(f"Error while finding code quantity: {e}")
            return {
                'status': False,
                'error': str(e)
            }