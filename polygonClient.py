import requests
from dotenv import load_dotenv
from web3 import Web3
import os
load_dotenv()

class polygonClient:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("POLYGON_RPC_URL")))

        self.mainWallet = self.w3.to_checksum_address(os.getenv('MAIN_WALLET_ADDRESS'))
        self.mainPK =  os.getenv('MAIN_WALLET_PRIVATE_KEY')

        self.token = self.w3.to_checksum_address(os.getenv('TOKEN_CONTRACT_ADDRESS'))
        self.tokenABI = os.getenv('TOKEN_ABI')

    def userWalletBalance(self,address):
        balance = self.w3.eth.get_balance(address)
        print(f'balance:{balance}')
        return balance

    def userQHCBalance(self,address):
        tokenContact = self.w3.eth.contract(address=self.token,abi=self.tokenABI)
        balance = tokenContact.functions.balanceOf(address).call()
        return balance

    def checksum(self,address):
        return self.w3.to_checksum_address(address)

    # def send_transaction(self, receiver_address, amount):
    #     try:
    #         gas_price = self.w3.eth.gas_price
    #         gas_limit = 100000
    #         gas_fee = gas_price * gas_limit
    #
    #         amount = self.w3.to_wei(amount, 'ether')
    #         if amount <= gas_fee:
    #             raise ValueError("Insufficient balance to cover gas fee.")
    #
    #         amount_to_send = amount - gas_fee - 100000
    #
    #         print(amount_to_send)
    #
    #         tx = {
    #             'nonce': self.w3.eth.get_transaction_count(self.mainWallet, 'pending'),
    #             'to': receiver_address,
    #             'value': amount_to_send,
    #             'gas': gas_limit,
    #             'gasPrice': gas_price,
    #             'chainId': 137,
    #         }
    #         print("tr3")
    #         signed_tx = self.w3.eth.account.sign_transaction(tx, self.mainPK)
    #         tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    #         return {
    #             'status': True,
    #             'hash': tx_hash.hex()
    #         }
    #     except Exception as e:
    #         print(f"Error while transfers: {str(e)}")
    #         return{
    #             'status': False,
    #             'error': str(e)
    #         }

    def to_wei_c(self, value, decimal):
        return int(value * (10 ** decimal))

    def from_wei_c(self, value, decimal):
        return value / (10 ** decimal)

    def send_transaction(self, receiver_address, amount):
        try:
            print(f"receiver_address: {receiver_address}")
            print(f"Value of amount: {amount}, Type of amount: {type(amount)}")

            # Tạo đối tượng contract cho token
            tokenContact = self.w3.eth.contract(address=self.token,abi=self.tokenABI)

            # Chuyển đổi amount theo decimals của token (QHC có decimals = 3)
            amount_in_units = self.to_wei_c(amount,3)
            print(f"amount_in_units:{amount_in_units}")

            # Xác định gas price và gas limit
            gas_price = self.w3.eth.gas_price
            gas_limit = 100000  # Có thể thay đổi tùy thuộc vào token

            # Tạo giao dịch
            tx = tokenContact.functions.transfer(receiver_address, amount_in_units).build_transaction({
                'chainId': 137,  # Chain ID của Polygon
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.mainWallet, 'pending')
            })

            # Ký giao dịch
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.mainPK)

            # Gửi giao dịch
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            print(f"txhash:{tx_hash.hex()}")
            return {
                'status': True,
                'hash': tx_hash.hex()
            }
        except Exception as e:
            print(f"Error while transferring tokens: {str(e)}")
            return {
                'status': False,
                'error': str(e)
            }

    def wait_for_transaction(self, tx_hash, timeout=600, poll_interval=5):
        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout, poll_latency=poll_interval)
            return receipt
        except Exception as e:
            print(f"Error waiting for transaction {tx_hash}: {str(e)}")
            return None

    def get_v3_price(self,token_in, token_out, amount_in, fee=100, sqrt_price_limit_x96=0):
        # Khởi tạo contract Quoter
        quoter_address = self.w3.to_checksum_address(os.getenv('QUOTER_ADDRESS'))
        quoter_abi = os.getenv('QUOTER_ABI')
        quoter = self.w3.eth.contract(address=quoter_address, abi=quoter_abi)

        # Truy vấn tỷ giá
        amount_out = quoter.functions.quoteExactInputSingle(token_in, token_out, fee, amount_in,
                                                            sqrt_price_limit_x96).call()
        return amount_out

    def get_pol_usd_price(self):
        url = os.getenv("POL_per_USD_API_URL")
        try:
            response = requests.get(url).json()
            # Kiểm tra nếu phản hồi có dữ liệu
            if "matic-network" in response:
                return response["matic-network"]["usd"]
            else:
                print("Không có dữ liệu cho MATIC.")
                return None
        except Exception as e:
            print(f"Đã xảy ra lỗi khi lấy dữ liệu: {e}")
            return None

    def get_usd_to_vnd_rate(self):
        url = os.getenv("VND_per_USD_API_URL")  # Hoặc một API khác bạn chọn
        response = requests.get(url).json()
        return response["rates"]["VND"]

    def get_qhc_vnd_price(self,amount):
        try:
            # Lấy giá WPOL/USD
            wpol_usd_price = self.get_pol_usd_price()
            print(f"Giá WPOL/USD: {wpol_usd_price}")

            # Giả sử 1 QHC là input
            qhc_decimals = 3  # Số decimals của token QHC
            amount_in = self.to_wei_c(1,3)  # Lấy 1 token QHC

            # Lấy giá QHC/WPOL từ Uniswap V3 (giả sử sử dụng pool 0.3% phí)
            qhc_wpol_price_v3 = self.get_v3_price(self.token, os.getenv("WETH_ADDRESS"), amount_in)

            qhc_wpol_price_v3 = self.from_wei_c(qhc_wpol_price_v3,18)  # Vì WPOL có 18 decimals

            print(f"Giá QHC/WPOL từ Uniswap V3: {qhc_wpol_price_v3}")

            # Quy đổi giá QHC/USD
            qhc_usd_price = qhc_wpol_price_v3 * wpol_usd_price
            print(f"Giá QHC/USD: {qhc_usd_price}")

            # Lấy tỷ giá USD/VND từ API
            usd_to_vnd = self.get_usd_to_vnd_rate()
            print(f"Tỷ giá USD/VND: {usd_to_vnd}")

            # Quy đổi sang VND
            qhc_vnd_price = amount*(qhc_usd_price * usd_to_vnd)
            print(f"Giá QHC/VND: {qhc_vnd_price}")
            return{
                    'status': True,
                    'amount': qhc_vnd_price
                }
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
            return {
                'status': False,
                'error': str(e)
            }
