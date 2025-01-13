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