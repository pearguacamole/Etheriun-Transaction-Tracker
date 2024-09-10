from web3 import Web3
from config import RPC_ENDPOINT
from deposit_tracker import DepositTracker
from logger import logger
from prometheus_client import start_http_server, Counter, Summary
import time

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
DEPOSIT_COUNT = Counter('deposit_count', 'Number of deposits tracked')

def start_prometheus_server(port=8000):
    start_http_server(port)
    logger.info(f"Prometheus metrics available at http://localhost:{port}")

@REQUEST_TIME.time()
def main():
    web3 = Web3(Web3.HTTPProvider(RPC_ENDPOINT))
    
    if web3.is_connected():
        logger.info("Connected to Ethereum node")
        tracker = DepositTracker(web3)
        start_prometheus_server()
        while True:
            tracker.track_deposits()
            DEPOSIT_COUNT.inc()  # Increment deposit count when a new deposit is processed
            time.sleep(1)
    else:
        logger.error("Failed to connect to Ethereum node")

if __name__ == "__main__":
    main()
