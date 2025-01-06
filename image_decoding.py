import bz2

# Constants from the C code
PAYLOAD_IMG_BYTE_ID = 0xE0
PAYLOAD_IMG_HEAD_BYTE = 0xE2
PAYLOAD_IMG_TAIL_BYTE = 0xED
IMG_MARKER_LENGTH = 3

HEAD_MARKER = bytes([0x02, PAYLOAD_IMG_HEAD_BYTE] * IMG_MARKER_LENGTH)
TAIL_MARKER = bytes([0x02, PAYLOAD_IMG_TAIL_BYTE] * IMG_MARKER_LENGTH)

def decode_bz2_to_image(encoded_binary_path, output_image_path):
    # Read the encoded binary file
    with open(encoded_binary_path, 'rb') as bin_file:
        encoded_bytes = bin_file.read()

    # Remove head and tail markers
    start = len(HEAD_MARKER)
    end = len(encoded_bytes) - len(TAIL_MARKER)
    encoded_data = encoded_bytes[start:end]

    # Swap bytes pairwise
    swapped_bytes = bytearray()
    for i in range(0, len(encoded_data), 2):
        if i + 1 < len(encoded_data):
            # Swap pairs
            swapped_bytes.append(encoded_data[i + 1])
            swapped_bytes.append(encoded_data[i])
        else:
            swapped_bytes.append(encoded_data[i])  # If odd, just append the last byte

    # Decode the data
    decoded_bytes = bytearray()
    for i in range(0, len(swapped_bytes), 2):
        lsb = (swapped_bytes[i] >> 3) & 0b00011111
        msb = (swapped_bytes[i + 1] & 0b00011111) << 4
        decoded_bytes.append(lsb | msb)

    # Decompress bz2
    decompressed_bytes = bz2.decompress(decoded_bytes)

    # Save the original image
    with open(output_image_path, 'wb') as img_file:
        img_file.write(decompressed_bytes)

    print(f"Decoded image saved to {output_image_path}")


# Example usage
image_path = 'map.jpg'   # Replace with your image path
output_bz2_path = 'output_image.bz2'
binary_output_path = 'encoded_image.bin'
decoded_image_path = 'decoded_map.jpg'

decode_bz2_to_image(binary_output_path, decoded_image_path)
