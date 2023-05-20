# GPT-Oracle

GPT Oracle is an AI-powered service helping decentralized autonomous organizations (DAOs) generate new proposal ideas. The struggle of deciding what to decide on is real and we're here to assist.

## Overview

DAOs are effective at collective decision-making. However, they can sometimes struggle with generating new proposals. That's where the GPT Oracle comes in - it proposes new ideas and topics for discussion, which DAOs can then put to a vote.

The GPT Oracle consists of two main components - an Ethereum smart contract (GPT.sol) and a Python server script (server.py). These work together to provide a decentralized way to generate proposals with GPT-3.5-turbo and store them securely on the Ethereum blockchain.

### GPT.sol

The GPT Oracle smart contract is responsible for handling requests for new proposals. Each request stores a prompt, which is used to generate a proposal, and a unique ID from the OpenAI API. The contract also stores the result of the proposal generation.

Requests can only be fulfilled by the contract owner, adding a layer of security to the process.

### server.py

The server script acts as a bridge between the smart contract and the OpenAI API. When a new request event is emitted by the smart contract, the server script picks it up, sends a corresponding request to the OpenAI API, and fulfills the request by storing the generated proposal and the OpenAI request ID on the smart contract.

## Setup

To use the GPT Oracle, you will need to have the following installed:

- [Python](https://www.python.org/downloads/)
- [web3.py](https://web3py.readthedocs.io/)
- [solc](https://solidity.readthedocs.io/en/latest/installing-solidity.html)

You will also need an Ethereum client running locally.

1. Clone this repository.
2. Set the environment variables `OPENAI_API_KEY` and `PRIVATE_KEY`.
3. Run `python server.py`.

## Contributing

Contributions are welcome. Please feel free to submit a pull request or open an issue.

## License

The GPT Oracle is licensed under the MIT License.

