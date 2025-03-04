Solana Wallet Balance Checker and Transfer Script
Welcome to the Solana Wallet Balance Checker and Transfer Script! This Python script helps you check the balance of SOL (Solana's native cryptocurrency) and JUP tokens in multiple Solana wallets and transfer them to a target wallet if certain conditions are met. It uses the Solana blockchain and the solders library to interact with the network. This version can process all keypair_*.json files in the same folder!
Note: This script is for educational purposes. Be careful with private keys and real money—do not share your private keys with anyone!
What Does This Script Do?
Loads private keys from all keypair_*.json files in the folder (e.g., keypair_0.json, keypair_1.json).

Checks the SOL and JUP token balances for each wallet.

Transfers JUP tokens or SOL to a predefined target wallet if the balance is sufficient and there’s enough SOL to cover transaction fees and rent exemption.

Handles errors like missing files or network issues (e.g., "429 Too Many Requests").

Ensures enough SOL is left in the wallet for rent exemption (a Solana requirement).

Requirements
Before running this script, you need to set up your computer. Don’t worry—we’ll guide you step by step!
What You Need
A computer running macOS or Linux.

An internet connection.

Solana wallet private keys saved in JSON files (e.g., keypair_0.json, keypair_1.json).

Step-by-Step Setup Instructions
1. Install a Terminal
The terminal is like a command-line tool to talk to your computer. Follow these steps:
On macOS:
Open the "Applications" folder.

Find "Terminal" (it looks like a black screen icon) and double-click it.

On Linux:
Click the "Activities" menu (top-left corner) or press the Super key (Windows key).

Type "Terminal" and click the Terminal app when it appears.

2. Update Your System
Your computer needs to be up to date to install the right tools.
On macOS:
In Terminal, type:  

softwareupdate -i -a

Press "Enter" and wait. It might ask for your password—type it and press "Enter" again.

On Linux:
In Terminal, type:  

sudo apt update && sudo apt upgrade -y

Press "Enter." When it asks for a password, type it and press "Enter" again. Wait until it finishes.

3. Install Python
This script needs Python 3. Let’s install it.
On macOS:
Python might already be installed. Check by typing:  

python3 --version

If you see a version number (e.g., "Python 3.11.4"), you’re good! If not, install it:
Go to python.org in your web browser.

Download the latest Python 3 version for macOS and follow the installer instructions.

On Linux:
Install Python by typing:  

sudo apt install python3 python3-pip -y

Press "Enter" and wait. Then check the version:  

python3 --version

You should see a version number.

4. Install Git
Git helps you download the script from GitHub.
On macOS:
Install Git by typing:  

xcode-select --install

Press "Enter," then click "Install" in the pop-up window.

On Linux:
Install Git by typing:  

sudo apt install git -y

Press "Enter" and wait.

5. Download the Script
Let’s get the script from GitHub.
In Terminal, type:  

git clone https://github.com/yourusername/solana-wallet-script.git

Replace yourusername with the GitHub username and solana-wallet-script with the repository name (ask the script owner for the correct link if it’s different).

Press "Enter." This creates a folder called solana-wallet-script.

Type:  

cd solana-wallet-script

Press "Enter" to go into the folder.

6. Install Required Libraries
The script needs some extra tools (libraries). Install them with pip.
In Terminal, type:  

python3 -m pip install solders solana

Press "Enter" and wait. This downloads the solders and solana libraries.

7. Create Keypair JSON Files
The script needs your wallet’s private keys in files named keypair_*.json (e.g., keypair_0.json, keypair_1.json).
Get your Solana wallet’s private key (e.g., from a wallet like Phantom). It should be a 64-byte base64-encoded string.

For each wallet, create a file:
In Terminal, type:  

nano keypair_0.json

Press "Enter."

Type this inside (replace YOUR_BASE64_PRIVATE_KEY with your actual private key):  

{
  "private_key": "YOUR_BASE64_PRIVATE_KEY"
}

Press Ctrl + O, then "Enter" to save, then Ctrl + X to exit.

Repeat for other wallets (e.g., keypair_1.json, keypair_2.json) with different private keys.

Make sure all files are in the solana-wallet-script folder.

8. Make the Script Executable
This step lets you run the script directly.
In Terminal, type:  

chmod +x solana-wallet-script.py

Press "Enter."

9. Run the Script
Now you’re ready to use the script!
In Terminal, type:  

./solana-wallet-script.py

Press "Enter." The script will:
Find all keypair_*.json files.

Check SOL and JUP balances for each wallet.

Transfer tokens to the target wallet if conditions are met.

Watch the Terminal for messages (e.g., balances or errors).

Troubleshooting
Error: "ModuleNotFoundError":
Run the pip command again:  

python3 -m pip install solders solana

Error: "Keypair file not found":
Check that your keypair_*.json files are in the folder and have the correct format.

Error: "429 Too Many Requests":
The script will wait and retry. Be patient!

Error: "Insufficient SOL balance to send while maintaining rent exemption":
Ensure each wallet has at least 0.00099088 SOL (990880 lamports) to cover rent and fees.

Important Notes
Security: Keep your keypair_*.json files safe and never share them. Anyone with them can access your wallets!

Target Wallet: The script sends tokens to a hardcoded address. Change TARGET_WALLET_STR and TARGET_TOKEN_ACCOUNT_STR in the code if needed.

Costs: Sending transactions requires a small amount of SOL for fees. Each wallet must retain at least 0.00089088 SOL (890880 lamports) for rent exemption.

Contributing
Feel free to improve this script! Fork the repository, make changes, and submit a pull request.

