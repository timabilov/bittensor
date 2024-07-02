import pytest

from bittensor.v2.commands.root import RootRegisterCommand
from bittensor.v2.commands.delegates import NominateCommand
from bittensor.v2.commands.network import RegisterSubnetworkCommand
from bittensor.v2.commands.register import RegisterCommand
from ..utils import setup_wallet


# Automated testing for take related tests described in
# https://discord.com/channels/799672011265015819/1176889736636407808/1236057424134144152
@pytest.mark.asyncio
async def test_takes(local_chain):
    # Register root as Alice
    keypair, exec_command, wallet = await setup_wallet("//Alice")
    await exec_command(RootRegisterCommand, ["root", "register"])

    # Create subnet 1 and verify created successfully
    assert not (local_chain.query("SubtensorModule", "NetworksAdded", [1]).serialize())

    await exec_command(RegisterSubnetworkCommand, ["s", "create"])
    assert local_chain.query("SubtensorModule", "NetworksAdded", [1])

    assert local_chain.query("SubtensorModule", "NetworksAdded", [1]).serialize()

    # Register and nominate Bob
    keypair, exec_command, wallet = await setup_wallet("//Bob")
    assert (
        local_chain.query(
            "SubtensorModule", "LastTxBlock", [keypair.ss58_address]
        ).serialize()
        == 0
    )

    assert (
        local_chain.query(
            "SubtensorModule", "LastTxBlockDelegateTake", [keypair.ss58_address]
        ).serialize()
        == 0
    )
    await exec_command(RegisterCommand, ["s", "register", "--netuid", "1"])
    await exec_command(NominateCommand, ["root", "nominate"])
    assert (
        local_chain.query(
            "SubtensorModule", "LastTxBlock", [keypair.ss58_address]
        ).serialize()
        > 0
    )
    assert (
        local_chain.query(
            "SubtensorModule", "LastTxBlockDelegateTake", [keypair.ss58_address]
        ).serialize()
        > 0
    )
