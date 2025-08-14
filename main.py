from PIL import Image

def encode_message(image_path, message, output_path):
    """
    Encodes a secret message into an image using LSB steganography.
    
    Args:
        image_path (str): Path to the original image.
        message (str): The secret message to hide.
        output_path (str): Path to save the encoded image.
    """
    img = Image.open(image_path)
    binary_msg = ''.join(format(ord(c), '08b') for c in message)
    binary_msg += '1111111111111110'  # Delimiter to mark end of message

    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = img.getdata()
    new_pixels = []
    msg_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if msg_index < len(binary_msg):
            r = (r & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        if msg_index < len(binary_msg):
            g = (g & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        if msg_index < len(binary_msg):
            b = (b & ~1) | int(binary_msg[msg_index])
            msg_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path)
    print(f"[✅] Message encoded successfully into {output_path}")




def decode_message(image_path):
    """
    Decodes a hidden message from an image.
    
    Args:
        image_path (str): Path to the encoded image.
        
    Returns:
        str: The hidden message.
    """
    img = Image.open(image_path)
    binary_data = ""
    for pixel in img.getdata():
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ""
    for byte in all_bytes:
        message += chr(int(byte, 2))
        if message[-2:] == 'þ':  # End delimiter
            break
    return message[:-1]


if __name__ == "__main__":
    choice = input("Do you want to (E)ncode or (D)ecode?  : ").strip().lower()
    if choice == 'e':
        image_path = input("Enter the path of the image: ")
        message = input("Enter the secret message: ")
        output_path = input("Enter the output image path: ")
        encode_message(image_path, message, output_path)
    elif choice == 'd':
        image_path = input("Enter the path of the encoded image: ")
        hidden_message = decode_message(image_path)
        print(f"[📩] Hidden message: {hidden_message}")
    else:
        print("[❌] Invalid choice.")