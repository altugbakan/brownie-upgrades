from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork", "development", "ganache"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return b""
    else:
        return initializer.encode_input(*args)


def upgrade_proxy(
    proxy,
    new_implementation,
    proxy_admin=None,
    initializer=None,
    *args,
    account=get_account()
):
    if proxy_admin:
        if initializer:
            tx = proxy_admin.upgradeAndCall(
                proxy.address,
                new_implementation.address,
                encode_function_data(initializer, *args),
                {"from": account},
            )
        else:
            tx = proxy_admin.upgrade(
                proxy.address, new_implementation.address, {"from": account}
            )
    else:
        if initializer:
            tx = proxy.upgradeToAndCall(
                new_implementation.address, encode_function_data(initializer, *args)
            )
        else:
            tx = proxy.upgradeTo(new_implementation.address, {"from": account})
    tx.wait(1)
    return tx
