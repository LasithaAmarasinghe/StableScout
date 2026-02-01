import os
from web3 import Web3
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def get_stablecoin_yield(asset: str) -> str:
    """
    Fetches real-time supply APY for stablecoins on Ethereum Mainnet from Aave V3.
    Supported assets: 'USDC'.
    """
    # Load from .env in production
    RPC_URL = os.getenv("ALCHEMY_RPC_URL")
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        return "Error: Could not connect to the Ethereum network."

    pool_addr = w3.to_checksum_address("0x87870Bca3f3fD6335C3f4ce8392D69350B4fA4E2")
    asset_addr = w3.to_checksum_address("0xA0b86991c6218b36c1d19D4a2e9Eb0ce3606eb48")

    # Minimal Aave V3 ABI
    POOL_ABI = [{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveData","outputs":[{"components":[{"internalType":"uint256","name":"unimportant1","type":"uint256"},{"internalType":"uint128","name":"unimportant2","type":"uint128"},{"internalType":"uint128","name":"currentLiquidityRate","type":"uint128"},{"internalType":"uint128","name":"variableBorrowIndex","type":"uint128"},{"internalType":"uint128","name":"currentVariableBorrowRate","type":"uint128"},{"internalType":"uint128","name":"currentStableBorrowRate","type":"uint128"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"uint16","name":"id","type":"uint16"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"},{"internalType":"uint128","name":"accruedToTreasury","type":"uint128"},{"internalType":"uint128","name":"unbackedMintCap","type":"uint128"},{"internalType":"uint128","name":"isolationModeTotalDebt","type":"uint128"}],"internalType":"struct DataTypes.ReserveData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]

    try:
        pool_contract = w3.eth.contract(address=pool_addr, abi=POOL_ABI)
        data = pool_contract.functions.getReserveData(asset_addr).call()
        supply_apy = (data[2] / 10**27) * 100
        return f"The current live supply APY for {asset} on Aave V3 is {supply_apy:.2f}%."
    except Exception as e:
        return f"Error fetching data: {str(e)}"