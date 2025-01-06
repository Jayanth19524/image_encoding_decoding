import bz2

# Constants from the C code
PAYLOAD_IMG_BYTE_ID = 0xE0
PAYLOAD_IMG_HEAD_BYTE = 0xE2
PAYLOAD_IMG_TAIL_BYTE = 0xED
IMG_MARKER_LENGTH = 3

HEAD_MARKER = bytes([0x02, PAYLOAD_IMG_HEAD_BYTE] * IMG_MARKER_LENGTH)
TAIL_MARKER = bytes([0x02, PAYLOAD_IMG_TAIL_BYTE] * IMG_MARKER_LENGTH)

def encode_image_to_bz2(image_path, output_path, binary_output_path, txt_output_path):
    # Read image as bytes
    with open(image_path, 'rb') as img_file:
        img_bytes = img_file.read()

    # Compress to bz2
    compressed_bytes = bz2.compress(img_bytes)

    # Save as .bz2
    with open(output_path, 'wb') as bz2_file:
        bz2_file.write(compressed_bytes)

    # Generate encoded byte stream
    encoded_stream = bytearray()

    # Add HEAD marker
    encoded_stream.extend(HEAD_MARKER)

    # Encode data bytes
    for byte in compressed_bytes:
        lsb = (byte & 0b00011111) << 3
        msb = (byte & 0b11100000) >> 4 | PAYLOAD_IMG_BYTE_ID
        encoded_stream.append(lsb)
        encoded_stream.append(msb)

    # Add TAIL marker
    encoded_stream.extend(TAIL_MARKER)

    # Swap bytes pairwise
    swapped_stream = bytearray()
    for i in range(0, len(encoded_stream), 2):
        if i + 1 < len(encoded_stream):
            # Swap pairs
            swapped_stream.append(encoded_stream[i + 1])
            swapped_stream.append(encoded_stream[i])
        else:
            swapped_stream.append(encoded_stream[i])  # If odd, just append the last byte

    # Save byte stream with swapped pairs to binary file
    with open(binary_output_path, 'wb') as bin_file:
        bin_file.write(swapped_stream)

    # Save hex values to a text file
    with open(txt_output_path, 'w') as txt_file:
        for byte in swapped_stream:
            txt_file.write(f"{byte:02X} ")  # Write hex value with two digits, space separated

    return swapped_stream

# Example usage
image_path = 'before.jpeg'   # Replace with your image path
output_bz2_path = 'output_image.bz2'
binary_output_path = 'encoded_image.bin'
txt_output_path = 'encoded_image.txt'  # File to save hex stream
decoded_image_path = 'decoded_map.jpg'

encoded_byte_stream = encode_image_to_bz2(image_path, output_bz2_path, binary_output_path, txt_output_path)
print(f"Binary byte stream saved to {binary_output_path}")
