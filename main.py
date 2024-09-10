from web3 import Web3
from config import RPC_ENDPOINT
from deposit_tracker import DepositTracker
from logger import logger
from prometheus_client import start_http_server, Counter, Summary

def start_prometheus_server(port=8000):
    start_http_server(port)
    logger.info(f"Prometheus metrics available at http://localhost:{port}")

def main():
    web3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
    
    if web3.is_connected():
        logger.info("Connected to Ethereum node")
        tracker = DepositTracker(web3)
        start_prometheus_server()
        tracker.track_deposits()
    else:
        logger.error("Failed to connect to Ethereum node")

if __name__ == "__main__":
    main()
