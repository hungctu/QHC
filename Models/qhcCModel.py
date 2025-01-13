from Models.DeviceCodeModel import DeviceCodeModel
from Models.IpCodeModel import IpCodeModel
from Models.tranfersModel import transferModel
from Models.walletsModel import walletsModel
from database import Database
from polygonClient import polygonClient
from datetime import datetime
import random
import string

class qhcCModel:
    def __init__(self):
        self.db = Database()
        self.pol = polygonClient()

    # Add Nums Code
    # Begin
    def createCode(self, code):
        try:
            query = """INSERT INTO `qhc_c` (`code`) VALUES (%s)"""
            self.db.execute(query, (code,))
            return True  # Chèn thành công
        except Exception as e:
            # Lỗi nếu mã đã tồn tại (trùng UNIQUE constraint)
            if "Duplicate entry" in str(e):
                return False
            raise e  # Các lỗi khác không mong muốn

    def addCodes(self, nums):
        codes = []
        try:
            i = 1
            for _ in range(nums):
                while True:  # Lặp để đảm bảo mã không bị trùng
                    # Ký tự đầu tiên cố định là 'A'
                    first_char = 'C'
                    # Tạo 5 ký tự ngẫu nhiên còn lại (chữ cái in hoa và chữ số)
                    remaining_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    # Ghép lại thành mã hoàn chỉnh
                    code = first_char + remaining_chars

                    # Thử chèn mã vào cơ sở dữ liệu
                    if self.createCode(code):
                        codes.append({
                            "index": i,
                            "code": code
                        })
                        i += 1
                        break  # Thoát vòng lặp khi mã đã được tạo thành công

            return {
                'status': True,
                'message': f"Created {nums} codes",
                'codes': codes
            }
        except Exception as e:
            return {
                'status': False,
                'error': str(e)
            }
    # End

    #LAY CODE KHI QUET QR
    #BEGIN
    def getCode(self):
        try:
            query = """select id,code,unit from qhc_c where status=1 LIMIT 1"""
            result = self.db.fetch_one(query, ())
            return {
                'status': True,
                'result': result
            }
        except Exception as e:
            print(f"Error when get code: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def checkCountCode(self):
        try:
            query = """select count(id) as nums from qhc_c where status=1 LIMIT 1"""
            result = self.db.fetch_one(query, ())
            if result['nums'] == 0:
                return False
            return True
        except Exception as e:
            print(f"Error when check Code form qhc_c: {e}")
            return False

    def updateCodeStatus(self, id):
        try:
            query = """UPDATE `qhc_c` SET `status`=0, `get_code_at`=%s WHERE id=%s"""
            # Lấy thời gian hiện tại
            current_time = datetime.now()
            result = self.db.execute(query, (current_time, id))
            return {
                'status': True,
                'result': result
            }
        except Exception as e:
            print(f"Error when updating code: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def getNearestCode(self,last_code_time,device_name):
        try:
            query="""SELECT code,unit from qhc_c c join device_code dc on c.id=dc.code_id join device d on dc.device_id=d.id 
            WHERE dc.get_code_at=%s and d.device_name=%s LIMIT 1"""
            result = self.db.fetch_one(query,(last_code_time,device_name,))
            return {
                'status':True,
                'result':result
            }
        except Exception as e:
            print(f"Error when get nearest code: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def getCodeForUser(self,device_id):
        try:
            if self.checkCountCode()==False:
                add = self.addCodes(10)
                if add['status']==False:
                    return {
                        'status': False,
                        'error': add['error']
                    }
                
            result = self.getCode()
            if result['status']==False:
                return {
                    'status': False,
                    'error': result['error']
                }
            getcode = result['result']
            id = getcode['id']
            code = getcode['code']
            unit = getcode['unit']
            status = self.updateCodeStatus(id)
            if status['status']==False:

                return {
                    'status': False,
                    'error': status['error']
                }

            # icm = IpCodeModel()
            # print(type(id))
            # print(type(ip_id))
            # cic = icm.createIpCode(id,'QHC_C',ip_id)
            icm = DeviceCodeModel()
            print(type(id))
            print(type(device_id))
            cic = icm.createDeviceCode(id, 'QHC_A', device_id)
            if cic == False:
                return {
                    'status': False,
                    'error': 'Got the code successfully but cant update the time to get the code'
                }

            return {
                'status': True,
                'code': code,
                'unit': unit
            }

        except Exception as e:
            print(f"Error when get Code for User: {e}")
            return {
                'status': False,
                'error': str(e)
            }
    #END

    # SU DUNG CODE:
    # BEGIN
    def checkCode(self, code):
        try:
            query = """select count(id) as nums from qhc_c where code = %s"""
            result = self.db.fetch_one(query, (code,))
            if result['nums'] == 0:
                return False
            return True
        except Exception as e:
            print(f"Error when check Code form qhc_c: {e}")
            return False

    def checkCodeIsUsed(self,code):
        try:
            query = """select is_used from qhc_c where code = %s"""
            result = self.db.fetch_one(query, (code,))
            if result['is_used'] == 1:
                return False
            return True
        except Exception as e:
            print(f"Error when check Code form qhc_c: {e}")
            return False


    def updateCodeIsUsed(self, code, is_used):
        try:
            query = """UPDATE `qhc_c` SET `is_used`=%s, `used_code_at`=%s WHERE code=%s"""
            # Lấy thời gian hiện tại
            current_time = datetime.now()
            result = self.db.execute(query, (is_used, current_time, code,))
            return {
                'status': True,
                'result': result
            }
        except Exception as e:
            print(f"Error when updating code: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def SendToken(self, address):
        try:
            hash = self.pol.send_transaction(address, 0.1)
            if not hash['status']:
                return {
                    'status': False,
                    'error': hash['error']
                }

            result = self.pol.wait_for_transaction(hash['hash'])
            if result:
                # Nếu giao dịch thành công, trả về trạng thái thành công kèm hash
                return {
                    'status': True,
                    'hash': hash['hash']
                }
            else:
                # Nếu chờ giao dịch nhưng không nhận được kết quả, trả về lỗi
                return {
                    'status': False,
                    'error': 'Transaction failed or timed out'
                }
        except Exception as e:
            print(f"Error when send token: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def addCW(self, code, id):
        try:
            query = """INSERT INTO `get_qhcc`(`code`, `wallet_id`) VALUES (%s,%s)"""
            self.db.execute(query, (code, id,))
            return True
        except Exception as e:
            print(f"Error when add getQHCA data to db: {e}")
            return False

    def transaction(self, code, address):
        # B1: kiem tra code co ton tai ko=>Co den B3
        # B2: goi SendToken de thuc hien giao dich
        # B3: Kiem tra hash => Thanh cong den B4
        # B4: Cap nhat code sang TT da su dung
        # B5: Kiem tra vi nguoi dung co trong db hay ko
        # B5.1: Tao vi neu ko co
        # B5.2: Cap nhat vi neu co
        # B6: Them du lieu vao bang transfers
        # B7: Them du lieu vao bang get_qhca
        # B8: Tra ve Hash
        try:
            if not self.checkCode(code):
                return {
                    'status': False,
                    'error': f'{code} does not exist'
                }

            if not self.checkCodeIsUsed(code):
                return {
                    'status': False,
                    'error': f'{code} is used'
                }

            hash = self.SendToken(address)

            if hash['status'] == False:
                return {
                    'status': False,
                    'error': hash['error']
                }

            uc = self.updateCodeIsUsed(code, 1)
            if uc['status'] == False:
                return {
                    'status': False,
                    'error': uc['error']
                }

            wallets = walletsModel()
            wallet = wallets.addOrUpdateBalanceWallet(address)
            if wallet['status'] == False:
                return {
                    'status': False,
                    'error': wallet['error']
                }
            QHC = wallet['QHC']
            walletId = wallets.getWalletId(address)['id']

            transfer = transferModel()
            at = transfer.addTransfer(walletId, code, 0.1, hash['hash'])
            if at == False:
                uc = self.updateCodeIsUsed(code, 0)
                if uc['status'] == False:
                    return {
                        'status': False,
                        'error': uc['error']
                    }
                return {
                    'status': False,
                    'error': 'Cant add Transfer Data for this transaction'
                }

            cw = self.addCW(code, walletId)
            if cw == False:
                uc = self.updateCodeIsUsed(code, 0)
                if uc['status'] == False:
                    return {
                        'status': False,
                        'error': uc['error']
                    }
                return {
                    'status': False,
                    'error': 'Cant add Transfer Data for this transaction'
                }

            return {
                'status': True,
                'QHC': QHC,
                'txhash': hash
            }

        except Exception as e:
            print(f"ERROR: {e}")
            return {
                'status': False,
                'error': str(e)
            }
    # END

    def getCodeInfo(self,code):
        query = """select id,unit from qhc_c where code = %s"""
        result = self.db.fetch_one(query,(code,))
        return result

    def useCodeOnWP(self,code):
        try:
            # 1: Kiểm tra code đúng ko
            # 2: Kiểm tra code đã sử dụng chưa
            # 3: Lấy thong tin code
            # 4: Luu thong tin giao dich vao bang wp
            # 5: Trả về xác nhận
            if not self.checkCode(code):
                return {
                    'status': False,
                    'error': f'{code} does not exist'
                }

            if not self.checkCodeIsUsed(code):
                return {
                    'status': False,
                    'error': f'{code} is used'
                }

            info = self.getCodeInfo(code)
            id = info['id']
            unit = info['unit']
            amount = self.pol.get_qhc_vnd_price(unit)
            return {
                'status': True,
                'id': id,
                'code': code,
                'amount': amount
            }

        except Exception as e:
            print(f"ERROR: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def getCodeUnit(self, code):
        try:
            query = """select unit from qhc_c where code = %s"""
            result = self.db.fetch_one(query, (code,))

            # Kiểm tra nếu result là None
            if result is None or 'unit' not in result:
                return {
                    'status': False,
                    'error': f'Cant get {code} quantity'
                }

            # In thông tin nếu có
            print(f"unit: {result['unit']}, type: {type(result['unit'])}")
            return {
                'status': True,
                'unit': result['unit']
            }
        except Exception as e:
            print(f"Error when check Code form qhc_a: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def buyCode(self,tx_hash,customer):
        try:
            result = self.pol.wait_for_transaction(tx_hash)
            if result:
                result = self.getCode()
                if result['status'] == False:
                    return {
                        'status': False,
                        'error': result['error']
                    }
                getcode = result['result']
                id = getcode['id']
                code = getcode['code']
                unit = getcode['unit']
                status = self.updateCodeStatus(id)
                if status['status'] == False:
                    return {
                        'status': False,
                        'error': status['error']
                    }
                wallets = walletsModel()
                wallet = wallets.addOrUpdateBalanceWallet(customer)
                # if wallet['status'] == False:
                #     return {
                #         'status': False,
                #         'code': code,
                #         'error': wallet['error']
                #     }
                return {
                    'status': True,
                    'code': code,
                }
            else:
                # Nếu chờ giao dịch nhưng không nhận được kết quả, trả về lỗi
                return {
                    'status': False,
                    'error': 'Transaction failed or timed out'
                }
        except Exception as e:
            print(f"ERROR: {e}")
            return {
                'status': False,
                'error': str(e)
            }