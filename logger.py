import logging
import sys

# Set up basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("eth_deposit_tracker.log")  # Log to file for persistent records
    ]
)

logger = logging.getLogger('DepositTracker')
