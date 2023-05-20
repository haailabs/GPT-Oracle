import os
import time
import openai
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from solcx import compile_files

openai.api_key = os.getenv("OPENAI_API_KEY")

def fulfill_request(event, contract, account):
    prompt = event['args']['prompt']
    request_id = event['args']['requestId']
    
    response = openai.Completion.create(engine="gpt-3.5-turbo", prompt=prompt, max_tokens=60)
    generated_text = response.choices[0].text.strip()
    request_id_openai = response['id']

    contract.functions.fulfillRequest(request_id, generated_text, request_id_openai).transact({'from': account.address})

def listen_for_requests(contract, account):
    event_filter = contract.events.RequestCreated.createFilter(fromBlock='latest')
    while True:
        for event in event_filter.get_new_entries():
            fulfill_request(event, contract, account)
        time.sleep(10)

def deploy_contract(private_key, contract_file):
    with open(contract_file, 'r') as file:
        contract_source_code = file.read()

    compiled_sol = compile_files([contract_file]) 
    contract_interface = compiled_sol[contract_file + ':RequestContract']

    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)  

    account = web3.eth.account.from_key(private_key)

    contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = contract.constructor().transact({'from': account.address})
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    contract = web3.eth.contract(
        address=tx_receipt['contractAddress'],
        abi=contract_interface['abi']
    )

    return contract, account

contract, account = deploy_contract(os.getenv('PRIVATE_KEY'), 'contract.sol')
listen_for_requests(contract, account)
