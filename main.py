import json
import os 
from solcx import compile_standard, install_solc, compile_source
from dotenv import load_dotenv

from app.deploy import \
(connect_web3, 
read_contract, 
compile_contract,
write_contract, 
compile_contract_source,
get_abi, 
get_bytecode, 
create_contract,
submit_transaction,
interactive_contract)

load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
address = os.getenv("ADDRESS")

contract = read_contract(contract_file = "TodoList.sol")
compile_sol = compile_contract_source(contract)
contract_id, contract_interface = compile_sol.popitem()
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]

# contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
# success = write_contract(contract = contract_dict)
# abi = get_abi(contract_dict)
# bytecode = get_bytecode(contract_dict)

web3 = connect_web3(os.getenv("URL"))
print(web3.eth.block_number)
created_contract = create_contract(abi = abi, bytecode = bytecode)
tx_hash = submit_transaction(private_key = private_key, address = address, contract = created_contract)
w_contract = interactive_contract(tx_hash = tx_hash, abi = abi)

