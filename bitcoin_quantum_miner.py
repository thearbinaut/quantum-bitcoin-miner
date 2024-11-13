import subprocess
import json
import time
import sys

print("Script started")

try:
    from quantum_inspired_miner import quantum_inspired_mining
    print("quantum_inspired_miner imported successfully")
except ImportError as e:
    print(f"Failed to import quantum_inspired_miner: {e}")
    sys.exit(1)

def rpc_command(method, params=[]):
    command = f"bitcoin-cli {method} {' '.join(map(str, params))}"
    print(f"Executing command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(f"Command output: {result.stdout}")
    print(f"Command error: {result.stderr}")
    try:
        return json.loads(result.stdout) if result.stdout else None
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {result.stdout}")
        return None

def main():
    print("Entering main function")
    while True:
        try:
            print("Checking node status...")
            info = rpc_command('getblockchaininfo')
            if not info:
                print("Failed to get blockchain info. Is bitcoind running?")
                time.sleep(10)
                continue

            print(f"Blockchain info: {info}")
            print("Script is running. Press Ctrl+C to stop.")
            time.sleep(10)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()

