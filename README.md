# Solana Airdrop Script

This Python script helps you check the balance of SOL and JUP tokens in multiple Solana wallets, and transfer them to a target wallet if certain conditions are met. It uses the Solana blockchain and the `solders` library to interact with the network. This version can process all `keypair_*.json` files in the current working directory.

**Note:** Be careful with private keys and real money—do not share your private keys with anyone.

## What Does This Script Do?
- Loads private keys from all `keypair_*.json` files in the folder (e.g., `keypair_60.json`, `keypair_61.json`).
- Checks the SOL and JUP token balances for each wallet.
- Transfers JUP tokens or SOL to a predefined target wallet if the balance is sufficient and there’s enough SOL to cover transaction fees and rent exemption.
- Handles errors like missing files or network issues (e.g., "429 Too Many Requests").
- Ensures enough SOL remains in the wallet for rent exemption (a Solana requirement).

## Requirements

- macOS or Linux
- Python + modules
- Solana wallet seed phrase

### 1. Open a Terminal

#### On macOS:
- Open the "Applications" folder.
- Find "Terminal" and double-click it.

#### On Linux:
- Click the "Activities" menu (top-left corner) or press the **Super** key (Windows key).
- Type "Terminal" and click the Terminal app when it appears.

### 2. Update Your System

#### On macOS:
```bash
softwareupdate -i -a
```

#### On Linux:
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install Python

#### On macOS:
Check if Python 3 is installed:
```bash
python3 --version
```
If not installed, download it from [python.org](https://www.python.org/).

#### On Linux:
```bash
sudo apt install python3 python3-pip -y
python3 --version
```

### 4. Install Git

#### On macOS:
```bash
xcode-select --install
```

#### On Linux:
```bash
sudo apt install git -y
```

### 5. Download the Script
```bash
git clone https://github.com/kalenkilgore/solana-airdrop-script.git
cd solana-airdrop-script
```

### 6. Install Required Libraries
```bash
python3 -m pip install solders solana
```

### 7. Create Keypair JSON Files
The script needs your wallet’s private keys in files named `keypair_*.json` (e.g., `keypair_60.json`, `keypair_61.json`).

To generate the keypair files run the script in this [repo](https://github.com/kalenkilgore/solana-wallet-address-export)


### 8. Make the Script Executable
```bash
chmod +x solana-address-export.py
```

### 9. Run the Script
```bash
./solana-address-export.py
```

The script will:
- Find all `keypair_*.json` files.
- Check SOL and JUP balances for each wallet.
- Transfer tokens to the target wallet if conditions are met.
- Display messages (e.g., balances or errors).

## Troubleshooting

### Error: "ModuleNotFoundError"
Run the pip command again:
```bash
python3 -m pip install solders solana
```

### Error: "Keypair file not found"
Ensure that your `keypair_*.json` files are in the correct folder.

### Error: "429 Too Many Requests"
The script will automatically retry after waiting.

### Error: "Insufficient SOL balance to send while maintaining rent exemption"
Ensure each wallet has at least **0.00099088 SOL** (990880 lamports) to cover rent and fees.

## Important Notes
- **Security:** Keep your `keypair_*.json` files safe and never share them.
- **Target Wallet:** The script sends tokens to a hardcoded address. Change `TARGET_WALLET_STR` and `TARGET_TOKEN_ACCOUNT_STR` in the script if needed.
- **Costs:** Sending transactions requires a small amount of SOL for fees. Each wallet must retain at least **0.00089088 SOL** (890880 lamports) for rent exemption.

## Contributing
Feel free to improve this script! Fork the repository, make changes, and submit a pull request.

That’s the entire process. Have fun!

