import base64

# Path to the updated Python script
input_file = "Code_2.py"
output_file = "update.bin"

# Read and encode the file
with open(input_file, "rb") as f:
    encoded_data = base64.b64encode(f.read())

# Save the encoded data to a .bin file
with open(output_file, "wb") as f:
    f.write(encoded_data)

print(f"Encoded {input_file} to {output_file}.")
