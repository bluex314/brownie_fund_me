from brownie import FundMe
from scripts.helper_script import get_account


def fund():
    account = get_account()
    # Get the latest fund me contract from deployed contracts
    fund_me = FundMe[-1]
    entrance_fee = fund_me.getEntranceFee()
    print(f"Entrance Fee: {entrance_fee}")
    print("Funding...")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    account = get_account()
    # Get the latest fund me contract from deployed contracts
    fund_me = FundMe[-1]
    print("Withdrawing...")
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()
