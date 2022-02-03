import os 
import json
import logging
from dotenv import load_dotenv
from solcx import compile_standard, install_solc, compile_source
from web3 import Web3

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
SOLC_VERSION = os.getenv("SOLC_VERSION")
LOG_FILE = os.path.join(BASE_DIR, "test.log")

logging.basicConfig(filename = LOG_FILE, level = logging.DEBUG, 
                     format="%(asctime)s:%(levelname)s:%(message)s")

install_solc(SOLC_VERSION)
print(SOLC_VERSION)

def read_contract(contract_file:str) -> str:
    file_dir = os.path.join(BASE_DIR, f"contracts/{contract_file}")
    with open(file_dir, mode = "r") as file:
        return file.read()

def compile_contract(contract:str, contract_file_name:str) -> dict:
    contract_dict = compile_standard(
        input_data = {
            "language": "Solidity",
            "sources": {contract_file_name: {"content": contract}},
            "settings": {
                "outputSelection": {
                    "*" : {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version = SOLC_VERSION,
    )
    return contract_dict

def compile_contract_source(source:str):
    compile_sol = compile_source(source = source,     
                                output_values = ["abi", "bin"], 
                                solc_version = SOLC_VERSION
    )   
    return compile_sol

## helper function
def create_json_file(file_name = None):
    filename, _ = os.path.splitext(file_name)
    json_file_name = f"{filename.strip()}.json"
    return json_file_name

def write_contract(contract:dict, file_name = None):
    if isinstance(contract, dict):
        contract_json = json.dumps(contract)
    try:
        json_file_name = list(contract["contracts"].keys())[0] if file_name is None else file_name
        json_file_name = create_json_file(json_file_name)
        file_dir = os.path.join(BASE_DIR, json_file_name)
        with open(file_dir, mode = "w") as file:
            file.write(contract_json)
        return True
    except Exception as e:
        logging.error("write_contract failed") 
        return False

def get_abi(contract: dict) -> str:
    if not isinstance(contract, dict):
        raise TypeError("contract must be type dict")
    try:
        abi = json.dumps(contract["contracts"]["TodoList.sol"]["TodoList"]["abi"])
        return abi
    except Exception as e:
        logging.error("abi not found")
        return -1

def get_bytecode(contract:dict) -> str:
    if not isinstance(contract, dict):
        raise TypeError("contract must be type dict")
    try:
        bytecode = contract["contracts"]["TodoList.sol"]["TodoList"]["evm"]["bytecode"]["object"]
        return bytecode
    except Exception as e:
        logging.error("bytecode not found")
        return -1

def connect_web3(url:str):
    global web3
    web3 = Web3(Web3.HTTPProvider(os.getenv("URL")))
    if web3.isConnected():
        return web3
    else:
        logging.error("Connecting to web3 failed")
        raise ConnectionError("Connecting to web3 failed")


def create_contract(abi:str, bytecode:str):
    try:
        contract = web3.eth.contract(abi = abi, bytecode = bytecode)
        return contract
    except Exception as e:
        logging.debug("Creating a contract failed")

    
def submit_transaction(private_key:str, address:str, contract):
    nonce = web3.eth.get_transaction_count(address)
    transaction = contract.constructor().buildTransaction({
        "chainId": int(os.getenv("CHAIN_ID")),
        "gasPrice": web3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    })
    signed_tx = web3.eth.account.sign_transaction(transaction, private_key = private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash

def interactive_contract(tx_hash:str, abi:str):
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    contract = web3.eth.contract(address = tx_receipt.contractAddress, abi = abi)
    return contract