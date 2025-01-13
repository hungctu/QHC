from datetime import datetime

from database import Database
from polygonClient import polygonClient

class walletsModel:
    def __init__(self):
        self.db = Database()

    def checkAddress(self, address):
        try:
            query = """SELECT COUNT(*) AS nums FROM wallets WHERE wallet_address=%s"""
            result = self.db.fetch_one(query, (address,))
            print(f"result:{result}")
            print(f"add: {address}")
            if result['nums'] == 0:
                return {'status': True, 'exists': False}  # Truy vấn thành công, địa chỉ không tồn tại
            return {'status': True, 'exists': True}  # Truy vấn thành công, địa chỉ tồn tại
        except Exception as e:
            print(f"Error when checking address: {e}")
            return {'status': False, 'error': str(e)}  # Truy vấn thất bại

    def createWallet(self,address,POL,QHC):
        try:
            print(f'address:{address}')
            print(f'POL:{POL}')
            print(f'QHC:{QHC}')
            query= """INSERT INTO `wallets`(`wallet_address`, `POL`, `QHC`) VALUES (%s,%s,%s)"""
            self.db.execute(query,(address,POL,QHC,))
            return {
                'status': True,
                'message': 'wallet added successfully'
            }
        except Exception as e:
            print(f"Error when create wallet: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def updateBalanceWallet(self,address,POL,QHC):
        try:
            print(f"add1:{address}")
            query= """UPDATE `wallets` SET `POL`=%s,`QHC`=%s,`last_updated`=%s
             WHERE wallet_address=%s"""
            current_time = datetime.now()
            self.db.execute(query,(POL,QHC,current_time,address))
            return {
                'status': True,
                'message': 'wallet updated successfully'
            }
        except Exception as e:
            print(f"Error when update wallet: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def addOrUpdateBalanceWallet(self, address):
        try:
            pol = polygonClient()

            balance = pol.from_wei_c(pol.userWalletBalance(pol.checksum(address)),18)
            QHC = pol.from_wei_c(pol.userQHCBalance(pol.checksum(address)),3)

            check_result = self.checkAddress(address)
            if not check_result['status']:
                # Lỗi khi kiểm tra địa chỉ
                return {
                    'status': False,
                    'error': check_result.get('error', 'Unknown error occurred when checking the address')
                }

            if check_result['exists'] == True:
                result = self.updateBalanceWallet(address,balance,QHC)
            else:
                result = self.createWallet(address, balance, QHC)
            print(f"result: {result}")
            if result['status']==False:
                return {
                    'status': False,
                    'address': address,
                    'balance': balance,
                    'QHC': QHC,
                    'message': result['error']
                }

            print(result['message'])
            print(type(address))
            print(type(balance))
            print(type(QHC))
            return {
                'status': True,
                'address': address,
                'balance': balance,
                'QHC': QHC,
                'message': result['message']
            }

        except Exception as e:
            print(f"Error when adding wallet to DB: {e}")
            return {
                'status': False,
                'error': str(e)
            }

    def getWalletId(self,address):
        query = """SELECT id FROM wallets WHERE wallet_address=%s"""
        return self.db.fetch_one(query, (address,))