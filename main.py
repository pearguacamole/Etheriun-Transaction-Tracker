from web3 import Web3
from config import RPC_ENDPOINT
from deposit_tracker import DepositTracker
from logger import logger

def main():
    web3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
    
    if web3.is_connected():
        logger.info("Connected to Ethereum node")
        tracker = DepositTracker(web3)
        tracker.track_deposits()
    else:
        logger.error("Failed to connect to Ethereum node")

if __name__ == "__main__":
    main()
