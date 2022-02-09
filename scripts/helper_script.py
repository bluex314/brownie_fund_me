from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_BLOCKCHAINS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
DECIMAL = 8
STARTING_PRICE = 2 * 10**8


def get_account():
    print("Active network: ", network.show_active())
    if network.show_active() in (
        LOCAL_BLOCKCHAIN_ENVIRONMENT + FORKED_LOCAL_BLOCKCHAINS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallet"]["from_keys"])


def deploy_mocks():
    print("Deploying Mocks...")
    # If already deployed
    if len(MockV3Aggregator) <= 0:
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMAL, STARTING_PRICE, {"from": get_account()}
        )
    print("Mocks Deployed")
