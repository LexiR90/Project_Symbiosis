# auth_cli.py (partial update)
def authenticate_and_sync():
    password = getpass.getpass("Enter your GPG password: ")
    
    # Decrypt key to temporary file
    with tempfile.NamedTemporaryFile() as temp_key:
        subprocess.run(
            ["gpg", "--decrypt", "--batch", "--passphrase", password,
             "/home/lexirath90/Documents/secrets/project-symbiosis-448023-4fc6b154493c.json.gpg"],
            stdout=temp_key, check=True
        )
        
        # Set environment variable for bash script
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_key.name
        
        # Run sync script
        subprocess.run(
            ["/bin/bash", "/home/lexirath90/Project_Symbiosis/sync_framework.sh", "--drive"],
            check=True
        )
    
    # Environment variable auto-cleared when Python exits
