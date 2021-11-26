from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest

from scripts.helpful_scripts import get_account, encode_function_data, upgrade_proxy


def test_proxy_upgrades():
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

    # Act/Assert
    box_v2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    upgrade_proxy(proxy, box_v2, proxy_admin, account=account)
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
