from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    network,
    config,
)

from scripts.helpful_scripts import get_account, encode_function_data, upgrade_proxy


def main():
    account = get_account()
    publish_source = config["networks"][network.show_active()].get("verify", False)

    # Deploy Box
    print("Deploying Box...")
    box = Box.deploy({"from": account}, publish_source=publish_source)
    print("Deployed.")

    # Deploy ProxyAdmin
    print("Deploying ProxyAdmin...")
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=publish_source)
    print("Deployed.")

    # Deploy TransparentUpgradeableProxy
    print("Deploying TransparentUpgradeableProxy...")
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encode_function_data(),
        {"from": account, "gas_limit": 1000000},
        publish_source=publish_source,
    )
    print("Deployed.")

    # Test proxy
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print("Storing 1 to proxy...")
    proxy_box.store(1, {"from": account})
    print("Stored.")
    print("Retrieving...")
    retrieved_value = proxy_box.retrieve()
    print(f"Retrieved {retrieved_value}.")

    # Deploy BoxV2
    print("Deploying BoxV2...")
    box_v2 = BoxV2.deploy({"from": account}, publish_source=publish_source)
    print("Deployed.")

    # Upgrade proxy.
    print("Upgrading Proxy...")
    upgrade_proxy(proxy, box_v2, proxy_admin, account=account)
    print("Upgraded.")

    # Test upgrade.
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print("Incrementing proxy...")
    proxy_box.increment({"from": account})
    print("Incremented.")
    print("Retrieving...")
    retrieved_value = proxy_box.retrieve()
    print(f"Retrieved {retrieved_value}.")
