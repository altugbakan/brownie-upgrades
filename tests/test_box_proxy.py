from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract

from scripts.helpful_scripts import get_account, encode_function_data


def test_proxy_delegate_calls():
    # Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        encode_function_data(),
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    # Act/Assert
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
