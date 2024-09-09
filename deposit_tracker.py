from web3 import Web3
from config import BEACON_DEPOSIT_CONTRACT
from mongo_handler import MongoHandler
from telegram_notifier import TelegramNotifier
from logger import logger

class DepositTracker:
    def __init__(self, web3):
        self.web3 = web3
        self.contract_address = Web3.to_checksum_address(BEACON_DEPOSIT_CONTRACT)
        self.mongo_handler = MongoHandler()
        self.notifier = TelegramNotifier()

    def track_deposits(self):
        # Create a filter for tracking deposits to the Beacon Deposit Contract
        deposit_filter = self.web3.eth.filter({
            'address': self.contract_address,
            'fromBlock': 'latest'
        })

        # Polling the filter for new deposits
        while True:
            for event in deposit_filter.get_new_entries():
                self.process_event(event)

    def process_event(self, event):
        tx_hash = event['transactionHash'].hex()
        tx = self.web3.eth.get_transaction(tx_hash)
        block = self.web3.eth.get_block(tx['blockNumber'])
        
        # Process multiple deposits in a single transaction if applicable
        for log in self.web3.eth.get_transaction_receipt(tx_hash).logs:
            if log.address == self.contract_address:
                deposit = {
                    'blockNumber': tx['blockNumber'],
                    'blockTimestamp': block['timestamp'],
                    'fee': tx['gasPrice'] * tx['gas'],
                    'hash': tx_hash,
                    'pubkey': log.topics[1].hex()  # Adjust based on actual event structure
                }
                logger.info(f"New deposit detected: {deposit}")
                self.mongo_handler.insert_deposit(deposit)
                self.notifier.send_notification(f"New deposit detected: {deposit}")
