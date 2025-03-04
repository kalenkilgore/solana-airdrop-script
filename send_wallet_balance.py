#!/usr/bin/env python3
import sys
import time
import json
import os
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.transaction import Transaction, AccountMeta
from solders.instruction import Instruction
from solders.system_program import transfer, TransferParams
from solders.keypair import Keypair as SoldersKeypair
from solders.pubkey import Pubkey
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address, transfer_checked, TransferCheckedParams
import random
from solders.hash import Hash
from solders.keypair import Keypair
from solders.presigner import Presigner
from solders.signature import Signature
from solders.transaction import Transaction as SoldersTransaction
from solders.message import Message
from solders.compute_budget import set_compute_unit_price, set_compute_unit_limit

# Constants
JUP_MINT_STR = "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
TARGET_WALLET_STR = "9RzSFFeM8xdTqDN2WvhseNyZsTuEbV9ZSY9EdADQpFhw"
TARGET_TOKEN_ACCOUNT_STR = "6Sdv4eDLQFBG4pv4QLL5w8xeXHueJHGC4hwZKmjbQMAE"
TOKEN_PROGRAM_ID_STR = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"

def load_keypair(index: int) -> SoldersKeypair:
    try:
        filename = f"keypair_{index}.json"
        if not os.path.exists(filename):
            print(f"Keypair file {filename} not found")
            return None
        
        with open(filename, 'r') as f:
            keypair_data = json.load(f)
        
        private_key = bytes(keypair_data['private_key'])
        if len(private_key) != 64:
            raise ValueError(f"Invalid private key length: {len(private_key)} bytes, expected 64")
        
        return SoldersKeypair.from_bytes(private_key)
    
    except Exception as e:
        print(f"Error loading keypair for index {index}: {e}")
        return None

def get_latest_blockhash_with_retry(client, max_retries=5, base_delay=5):
    """Fetch latest blockhash with retry on 429 errors."""
    for attempt in range(max_retries):
        try:
            resp = client.get_latest_blockhash()
            return resp.value.blockhash
        except Exception as e:
            if "429 Too Many Requests" in str(e):
                delay = base_delay * (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
                print(f"429 Too Many Requests detected. Retrying in {delay:.2f} seconds (attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
            else:
                raise e
    raise Exception("Failed to fetch blockhash after max retries due to 429 errors")

def main():
    client = Client("https://api.mainnet-beta.solana.com")

    # Find all keypair files in the current directory
    keypair_files = [f for f in os.listdir('.') if f.startswith('keypair_') and f.endswith('.json')]
    
    # Sort the keypair files by index
    keypair_files.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))
    
    print(f"Found {len(keypair_files)} keypair files to process")
    
    # Process each keypair file
    for keypair_file in keypair_files:
        # Extract the index from the filename
        i = int(keypair_file.split('_')[1].split('.')[0])
        print(f"\nProcessing keypair index {i}...")
        
        try:
            keypair = load_keypair(i)
            if keypair is None:
                print(f"Skipping keypair {i} due to loading error")
                continue
            
            # Fix: Use the correct method to get secret key from SoldersKeypair
            # The keypair object is already a solders.keypair.Keypair
            from solana.keypair import Keypair
            solana_keypair = Keypair.from_secret_key(bytes(keypair))
            
            pubkey = keypair.pubkey()
            pubkey_str = str(pubkey)
            # Create PublicKey object from the string
            solana_pubkey = PublicKey(pubkey_str)
            
            print(f"Loaded public key: {pubkey_str}")
            print(f"Public key length (base58): {len(pubkey_str)}")
            print("Public key is valid")

            # Get SOL balance
            try:
                print(f"Fetching SOL balance for: {pubkey_str}")
                sol_balance_resp = client.get_balance(pubkey)
                print(f"Raw response: {sol_balance_resp}")
                sol_balance = sol_balance_resp.value
                print(f"SOL balance: {sol_balance} lamports")
            except Exception as e:
                print(f"Error fetching SOL balance: {e}")
                continue

            # Get JUP balance
            jup_mint = PublicKey(JUP_MINT_STR)
            jup_token_account = get_associated_token_address(solana_pubkey, jup_mint)
            jup_token_account_str = str(jup_token_account)
            try:
                print(f"Fetching JUP balance for: {jup_token_account_str}")
                jup_balance_resp = client.get_token_account_balance(jup_token_account)
                print(f"JUP balance response: {jup_balance_resp}")
                if hasattr(jup_balance_resp, 'value') and jup_balance_resp.value is not None:
                    jup_amount = int(jup_balance_resp.value.amount)
                    jup_decimals = int(jup_balance_resp.value.decimals)
                    print(f"JUP balance: {jup_amount / (10 ** jup_decimals)} JUP (raw: {jup_amount}, decimals: {jup_decimals})")
                else:
                    jup_amount = 0
                    jup_decimals = 6
                    print("No JUP token account found or zero balance")
            except Exception as e:
                print(f"Error checking JUP balance: {e}")
                jup_amount = 0
                jup_decimals = 6
                print("Error checking JUP balance, assuming zero")

            # Send JUP tokens if balance exists and sufficient SOL
            MIN_SOL_FOR_FEE = 10000
            if jup_amount > 0 and sol_balance >= MIN_SOL_FOR_FEE:
                print("Sending JUP tokens...")
                blockhash = get_latest_blockhash_with_retry(client)
                print(f"Using blockhash: {blockhash}")

                # Fix: Convert PublicKey to Pubkey
                from solders.pubkey import Pubkey
                
                # Convert all PublicKey objects to Pubkey objects
                solders_pubkey = Pubkey.from_string(str(solana_pubkey))
                jup_token_account_pubkey = Pubkey.from_string(str(jup_token_account))
                target_token_account_pubkey = Pubkey.from_string(str(PublicKey(TARGET_TOKEN_ACCOUNT_STR)))
                jup_mint_pubkey = Pubkey.from_string(str(PublicKey(JUP_MINT_STR)))
                token_program_pubkey = Pubkey.from_string(str(TOKEN_PROGRAM_ID))
                
                # Create transaction using the converted Pubkey objects
                txn = Transaction(fee_payer=solders_pubkey, recent_blockhash=blockhash)
                
                # Add the transfer instruction
                transfer_ix = transfer_checked(
                    TransferCheckedParams(
                        program_id=token_program_pubkey,
                        source=jup_token_account_pubkey,
                        mint=jup_mint_pubkey,
                        dest=target_token_account_pubkey,
                        owner=solders_pubkey,
                        amount=jup_amount,
                        decimals=jup_decimals
                    )
                )
                
                # Add the transfer instruction to the transaction
                txn.add(transfer_ix)
                
                # Add priority fees
                txn.add(set_compute_unit_price(400000))
                txn.add(set_compute_unit_limit(200000))
                
                try:
                    # Send the transaction
                    send_resp = client.send_transaction(txn, keypair)
                    print(f"JUP transfer tx: {send_resp.value}")
                except Exception as e:
                    print(f"Error sending JUP: {e}")
                    print(f"Transaction details: {txn}")
                time.sleep(5)

            if jup_amount > 0 and sol_balance < MIN_SOL_FOR_FEE:
                print(f"Insufficient SOL ({sol_balance} lamports) for JUP transfer fee. Minimum required: {MIN_SOL_FOR_FEE} lamports.")

            # Send SOL if balance sufficient
            FEE_ESTIMATE = 5000
            if sol_balance > FEE_ESTIMATE:
                # Fix: Leave more SOL for rent-exemption
                # The error shows we need to leave more SOL for rent
                # Solana accounts need a minimum balance to stay alive
                RENT_EXEMPT_MINIMUM = 890880  # Minimum SOL needed for rent exemption (0.00089088 SOL)
                ADJUSTED_FEE_ESTIMATE = 100000  # For transaction fees
                
                # Leave enough for both rent and fees
                TOTAL_RESERVED = RENT_EXEMPT_MINIMUM + ADJUSTED_FEE_ESTIMATE
                
                if sol_balance <= TOTAL_RESERVED:
                    print(f"Insufficient SOL balance ({sol_balance} lamports) to send while maintaining rent exemption. Minimum required: {TOTAL_RESERVED} lamports.")
                    continue
                
                send_amount = sol_balance - TOTAL_RESERVED
                print(f"Sending {send_amount} lamports of SOL...")
                blockhash = get_latest_blockhash_with_retry(client)
                print(f"Using blockhash: {blockhash}")

                # Fix: Import Pubkey at the beginning of this section
                from solders.pubkey import Pubkey
                
                # Convert PublicKey objects to Pubkey objects
                solders_pubkey = Pubkey.from_string(str(solana_pubkey))
                target_wallet_pubkey = Pubkey.from_string(str(PublicKey(TARGET_WALLET_STR)))
                
                # Create the SOL transfer instruction with Pubkey objects
                sol_transfer_ix = transfer(
                    TransferParams(
                        from_pubkey=solders_pubkey,
                        to_pubkey=target_wallet_pubkey,
                        lamports=send_amount
                    )
                )
                
                # Create transaction
                tx = Transaction()
                tx.recent_blockhash = Hash.from_string(str(blockhash))
                tx.fee_payer = solders_pubkey
                
                tx.add(sol_transfer_ix)
                
                # Add priority fees
                tx.add(set_compute_unit_price(400000))
                tx.add(set_compute_unit_limit(200000))
                
                try:
                    send_resp = client.send_transaction(tx, keypair)
                    print(f"SOL transfer tx: {send_resp.value}")
                except Exception as e:
                    print(f"Error sending SOL: {e}")
                    print(f"Transaction details: {tx}")
                time.sleep(5)
            else:
                print(f"Insufficient SOL balance ({sol_balance} lamports) to cover fee for SOL transfer. Minimum required: {FEE_ESTIMATE}")

        except Exception as e:
            import traceback
            print(f"Error processing keypair index {i}: {e}")
            print(traceback.format_exc())

if __name__ == "__main__":
    main()