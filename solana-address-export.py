import pexpect
import getpass
import json
import os
import subprocess

def get_wallet_keypair(seed_phrase, index):
    # Temporary file to store the keypair
    temp_file = f'keypair_temp_{index}.json'
    
    # Command to generate keypair with solana-keygen
    cmd = f'solana-keygen recover "prompt:?key={index}/0" --outfile {temp_file}'
    
    # Spawn the child process
    child = pexpect.spawn(cmd, encoding='utf-8')
    
    # Wait for the seed-phrase prompt
    child.expect_exact('[recover] seed phrase:')
    child.sendline(seed_phrase)
    
    # Wait for bip39 passphrase prompt (if none, just press enter)
    child.expect(r'If this seed phrase has an associated passphrase.*continue:')
    child.sendline('')
    
    # Wait for confirmation prompt and respond with 'y'
    child.expect_exact('Continue? (y/n):')
    child.sendline('y')
    
    # Wait for the command to fully finish
    child.expect(pexpect.EOF)
    
    # Read the temporary keypair file
    try:
        with open(temp_file, 'r') as f:
            keypair_data = json.load(f)
        
        # The solana-keygen output is an array of 64 bytes (32 bytes private key + 32 bytes public key)
        if len(keypair_data) != 64:
            raise ValueError(f"Invalid keypair length: {len(keypair_data)} bytes, expected 64")
        
        # Get the public key string using solana-keygen
        pub_cmd = f'solana-keygen pubkey {temp_file}'
        pub_child = pexpect.spawn(pub_cmd, encoding='utf-8')
        pub_child.expect(pexpect.EOF)
        public_key = pub_child.before.strip()
        
        # Use the full 64-byte keypair as the private key for compatibility
        full_keypair = bytes(keypair_data)
        
        # Clean up temporary file
        os.remove(temp_file)
        
        return {
            'public_key': public_key,
            'private_key': [int(b) for b in full_keypair]  # Store full 64-byte keypair as list of integers
        }
    except Exception as e:
        print(f"Error reading keypair file {temp_file}: {str(e)}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return None

def main():
    # Quietly get the seed phrase (like a password)
    seed_phrase = getpass.getpass('Enter your phantom seed phrase: ')
    
    # How many keypairs to generate
    num_addresses = int(input('Enter the number of keypairs to derive: '))
    print("\n")
    
    # Store keypairs in separate files
    with open('addresses.txt', 'w') as public_file:
        for i in range(num_addresses):
            try:
                keypair = get_wallet_keypair(seed_phrase, i)
                
                if keypair is None:
                    print(f"Failed to generate keypair for index {i}")
                    continue
                
                # Write public key to addresses.txt
                public_file.write(f'{keypair["public_key"]}\n')
                
                # Write full keypair to individual files in a structured JSON format
                with open(f'keypair_{i}.json', 'w') as keypair_file:
                    json.dump({
                        'public_key': keypair['public_key'],
                        'private_key': keypair['private_key']  # Full 64-byte keypair
                    }, keypair_file, indent=2)
                
                print(f'Public key: {keypair["public_key"]}')
                print(f'Full keypair saved to keypair_{i}.json')
            except Exception as e:
                print(f"Error processing keypair {i}: {str(e)}")
            
            print("-" * 50)
    
    print('\nAll public keys have been saved to addresses.txt')
    print(f'All keypairs have been saved to individual JSON files (keypair_0.json through keypair_{num_addresses-1}.json)')

if __name__ == '__main__':
    main()