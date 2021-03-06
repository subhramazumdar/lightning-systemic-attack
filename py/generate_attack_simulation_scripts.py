import json
import os

from commands_generator.commands_generator import generate_attack_file
from paths import LN

num_sending_nodes = 10
num_receiving_nodes = num_sending_nodes
num_victims = 10
blockmaxweight = 4_000_000
simulation_num = 1
payments_per_channel = int(483 * 2)  # increase number of payments a little bit because some payments randomly fail

num_channels = num_sending_nodes * num_victims
script_name = f"steal-attack-{num_channels}-channels-blockmaxweight={blockmaxweight}"

# first we generate topology. sending-node ids start with 1, receiving-node ids
# start with 3, victim ids start with 4 (only a convention we use here, not required)
sending_node_ids = [f"1{i}" for i in range(1, num_sending_nodes + 1)]
receiving_node_ids = [f"3{i}" for i in range(1, num_receiving_nodes + 1)]
victim_node_ids = [f"4{i}" for i in range(1, num_victims + 1)]

topology = {}
for sending_node_id in sending_node_ids:
    topology[sending_node_id] = {
        "client": "c-lightning",
        "evil": True,
        "peers": victim_node_ids,
        "type": "attacker-sending",
    }

for receiving_node_id in receiving_node_ids:
    topology[receiving_node_id] = {
        "client": "c-lightning",
        "evil": True,
        "peers": [],
        "type": "attacker-receiving",
    }

for victim_node_id in victim_node_ids:
    topology[victim_node_id] = {
        "client": "lnd",
        "peers": receiving_node_ids,
        "type": "victim",
    }

topology_filename = f"topology-{num_sending_nodes}-{num_victims}-{num_receiving_nodes}.json"
topology_fullpath = os.path.join(LN, "topologies", topology_filename)
with open(topology_fullpath, mode="w") as f:
    json.dump(topology, f, sort_keys=True, indent=4)

outfile = os.path.join(LN, "simulations", f"{script_name}.sh")
datadir = os.path.join(LN, "simulations", f"{script_name}")
generate_attack_file(
    topology_file=topology_fullpath,
    simulation_number=simulation_num,
    bitcoin_blockmaxweight=blockmaxweight,
    payments_per_channel=payments_per_channel,
    amount_msat=11000000,
    datadir=datadir,
    block_time_sec=300,  # 5 minutes
    outfile=outfile,
)
