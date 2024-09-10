from web3 import Web3
from prometheus_client import Counter
from config import BEACON_DEPOSIT_CONTRACT
from mongo_handler import MongoHandler
from telegram_notifier import TelegramNotifier
from logger import logger
from datetime import datetime, timezone
import asyncio

DEPOSIT_PROCESSED = Counter('deposit_processed', 'Number of deposits processed')

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
                asyncio.run(self.process_event(event))

    def format_deposit(self, deposit):
        deposit['blockTimestamp'] = datetime.fromtimestamp(int(deposit['blockTimestamp']), tz=timezone.utc).strftime('%H:%M:%S %Y-%m-%d')
        deposit['fee'] = deposit['fee'] / 1e18  # Convert Wei to ETH
        deposit['transactionLink'] = f"https://etherscan.io/tx/{deposit['hash']}"
        return deposit

    async def process_event(self, event):
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
                    'hash': '0x'+str(tx_hash),
                    'pubkey': '0x'+str(log.topics[1].hex())  # Adjust based on actual event structure
                }
                fromatted_deposit = self.format_deposit(deposit)
                logger.info(f"New deposit detected: {fromatted_deposit} \n\n")
                await self.notifier.send_notification(f"New deposit detected: Block Number: {fromatted_deposit['blockNumber']} at Timestamp: {fromatted_deposit['blockTimestamp']} the transaction fee is {fromatted_deposit['fee']} eth, Transaction can be viewed at {fromatted_deposit['transactionLink']}")
                logger.info("notification sent \n\n")
                DEPOSIT_PROCESSED.inc() 
