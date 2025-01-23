import hashlib

# Path to the binary file
file_path = "update.bin"
expected_hash = "1734ef2ff774b6786aa4467951c8504254483376d18b1b400dc2e26bb04a91e4"  # Replace with your generated hash

# Calculate the hash
sha256 = hashlib.sha256()
with open(file_path, "rb") as f:
    while chunk := f.read(1024):
        sha256.update(chunk)

calculated_hash = sha256.hexdigest()

# Check if the hash matches
if calculated_hash == expected_hash:
    print("Hash matches!")
else:
    print("Hash mismatch!")
    print(f"Expected: {expected_hash}")
    print(f"Calculated: {calculated_hash}")
