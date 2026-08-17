import os
import json
import time
import sys
import logging

# Ensure python finds src folder relative to this script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agents.ingestion import SEED_LIST, filter_companies
from src.agents.margin import get_resilient_session
import yfinance as yf # type: ignore

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Initializing financials downloader...")
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Filter targets using ingestion seed list filter
    targets = filter_companies(SEED_LIST)
    logger.info(f"Found {len(targets)} target tickers to download operating margins for.")
    
    financials_path = os.path.join("data", "financials.json")
    
    # Load existing financials if any
    financials = {}
    if os.path.exists(financials_path):
        try:
            with open(financials_path, "r") as f:
                financials = json.load(f)
            logger.info(f"Loaded {len(financials)} existing ticker margins from cache.")
        except Exception as e:
            logger.warning(f"Failed to load existing cache: {e}. Starting fresh.")
            
    session = get_resilient_session()
    
    # Loop over all target tickers and fetch live margins
    for i, company in enumerate(targets):
        ticker = company.ticker
        logger.info(f"[{i+1}/{len(targets)}] Fetching operating margin for {ticker} ({company.company_name})...")
        
        try:
            stock = yf.Ticker(ticker, session=session)
            # Fetch info dict
            info = stock.info
            margin_decimal = info.get("operatingMargins")
            
            if margin_decimal is not None:
                margin_percent = margin_decimal * 100.0
                financials[ticker] = round(margin_percent, 4)
                logger.info(f"Successfully fetched {ticker}: {margin_percent:.2f}%")
            else:
                logger.warning(f"No operating margin data found for {ticker}")
                if ticker not in financials:
                    financials[ticker] = None
        except Exception as e:
            logger.error(f"Error fetching operating margin for {ticker}: {type(e).__name__} - {e}")
            if ticker not in financials:
                financials[ticker] = None
                
        # Sleep to avoid rate limits
        if i < len(targets) - 1:
            logger.info("Waiting 2 seconds before the next request...")
            time.sleep(2)
            
    # Write back to financials.json
    try:
        with open(financials_path, "w") as f:
            json.dump(financials, f, indent=4)
        logger.info(f"Successfully wrote financials cache to {financials_path}")
    except Exception as e:
        logger.error(f"Failed to save financials cache to {financials_path}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
