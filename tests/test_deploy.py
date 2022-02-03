import unittest
import json
import os 
from dotenv import load_dotenv

from app.deploy import\
(connect_web3, 
read_contract, 
compile_contract_source,
compile_contract,
write_contract, 
get_abi, 
get_bytecode, 
create_contract,
submit_transaction,
interactive_contract)

load_dotenv()


class TestDeploy(unittest.TestCase):
    def test_read_contract_file(self):
        """This test asserts if a contract file is read successfuly"""
        contract = read_contract("TodoList.sol")
        self.assertIsNotNone(contract)

    def test_compile_contract_source(self):
        """This test asserts if the contract source is compiled successfuly"""
        contract = read_contract("TodoList.sol")
        sompiled_sol = compile_contract_source(source = contract)

    def test_compile_contract_with_solcx(self):
        """This test asserts if a contract is compiled successfuly"""
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        self.assertIsInstance(contract_dict, dict)

    def test_write_contract_to_json(self):
        """This test asserts if a contract is written into a json file"""
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        success = write_contract(contract = contract_dict)
        self.assertTrue(success)

    def test_get_bytecode_and_abi(self):
        """This test asserts if an abi is retrieved"""
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        success = write_contract(contract = contract_dict)
        abi = get_abi(contract_dict)
        self.assertNotEqual(abi, -1)
        
    def test_get_bytecodes(self):
        """This test asserts if bytecode is retrieved"""
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        success = write_contract(contract = contract_dict)
        bytecode = get_bytecode(contract_dict)
        self.assertNotEqual(bytecode, -1)

    def test_connect_web3(self):
        """This test assert if the app connects to the web3"""
        is_connected = connect_web3(os.getenv("URL"))

    def test_create_contract(self):
        """This test assert if the contract is created"""
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        success = write_contract(contract = contract_dict)
        abi = get_abi(contract_dict)
        bytecode = get_bytecode(contract_dict)
        web3 = connect_web3(os.getenv("URL"))
        created_contract = create_contract(abi = abi, bytecode = bytecode)

    def test_submit_transaction(self):
        """This test assert if the transaction is created"""
        private_key = os.getenv("PRIVATE_KEY")
        address = os.getenv("ADDRESS")
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        success = write_contract(contract = contract_dict)
        abi = get_abi(contract_dict)
        bytecode = get_bytecode(contract_dict)
        created_contract = create_contract(abi = abi, bytecode = bytecode)
        tx_hash = submit_transaction(private_key = private_key, address = address, contract = created_contract)
        
    def test_interact_contract(self):
        """This test assert if a contract is isinteractive"""
        private_key = os.getenv("PRIVATE_KEY")
        address = os.getenv("ADDRESS")
        contract = read_contract(contract_file = "TodoList.sol")
        contract_dict = compile_contract(contract = contract, contract_file_name = "TodoList.sol")
        success = write_contract(contract = contract_dict)
        abi = get_abi(contract_dict)
        bytecode = get_bytecode(contract_dict)
        created_contract = create_contract(abi = abi, bytecode = bytecode)
        tx_hash = submit_transaction(private_key = private_key, address = address, contract = created_contract)
        transaction = interactive_contract(tx_hash, abi)