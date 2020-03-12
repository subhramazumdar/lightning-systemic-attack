#!/usr/bin/env bash
SCRIPT_NAME=$(basename -s ".sh" $0)
DATA_DIR="$LN/simulations/$SCRIPT_NAME"
OUTPUT_FILE="$LN/simulations/$SCRIPT_NAME.out"
TOPOLOGY="$LN/topologies/topology-5-lnd-victims.json"
SIMULATION=3
COMMANDS_FILE=$LN/generated_commands_$SIMULATION
cd $LN/py
python3 -m commands_generator.commands_generator \
    --topology "$TOPOLOGY" \
    --establish-channels \
    --make-payments 1 3 5000 11000000 \
    --steal-attack 1 3 200 \
    --dump-data "$DATA_DIR" \
    --block-time 150 \
    --bitcoin-blockmaxweight 100000 \
    --simulation-number $SIMULATION \
    --outfile $COMMANDS_FILE

rm -rf /tmp/lightning-simulations/$SIMULATION
bash $COMMANDS_FILE 2>&1 | tee "$OUTPUT_FILE"
