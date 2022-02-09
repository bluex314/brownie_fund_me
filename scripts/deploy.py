from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helper_script import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
)


def deploy_fund_me():
    __network = network.show_active()
    print(f"Deploying to network: {__network}")
    # Live chain
    # If we are in a network like rinkbey use the address from config.
    # otherwise use local network like ganche for mocking.
    if __network not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    # Development chain
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # Publish_source is for verification, for that add ETHERSCAN_TOKEN in .env.
    # Token can be available from etherscan.io -> apis.
    # It is important to verify for making sure that code is not error prone and have security.
    # Passing price_feed_address as argument to FundMe constructor.
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": get_account()},
        publish_source=config["networks"][__network]["verify"],
    )

    print(f"Contract deployed to address : {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
