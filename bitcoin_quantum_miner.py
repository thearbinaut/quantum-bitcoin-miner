import subprocess
import json
import time
import sys
import logging

from quantum_inspired_miner import quantum_inspired_mining

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def rpc_command(method, params=[]):
    command = f"bitcoin-cli {method} {' '.join(map(str, params))}"
    logging.debug(f"Executing command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stderr:
        logging.error(f"Command error: {result.stderr}")
    try:
        return json.loads(result.stdout) if result.stdout else None
    except json.JSONDecodeError:
        logging.error(f"Failed to parse JSON: {result.stdout}")
        return None

def main():
    logging.info("Starting Bitcoin Quantum Miner")
    while True:
        try:
            info = rpc_command('getblockchaininfo')
            if not info:
                logging.warning("Failed to get blockchain info. Is bitcoind running?")
                time.sleep(10)
                continue

            if info['initialblockdownload']:
                logging.info(f"Node is still syncing. Current progress: {info['verificationprogress']*100:.2f}%")
                time.sleep(60)
                continue

            block_template = rpc_command('getblocktemplate', ['{"rules": ["segwit"]}'])
            if not block_template:
                logging.warning("Failed to get block template. Retrying...")
                time.sleep(10)
                continue

            logging.info("Starting quantum-inspired mining...")
            result = quantum_inspired_mining(8, block_template)  # Using 8 "quantum positions"
            if result:
                position, nonce, block_hash = result
                logging.info(f"Potential block found by position {position}")
                logging.info(f"Nonce: {nonce}")
                logging.info(f"Block hash: {block_hash}")

                submit_result = rpc_command('submitblock', [block_hash])
                logging.info(f"Block submission result: {submit_result}")
            else:
                logging.info("No valid block found in this iteration.")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(10)  # Wait 10 seconds before next attempt

if __name__ == "__main__":
    main()
