from PIL import Image

DELIMITER = "1111111111111110"

def encode_message(image_path, message, output_path):
    img = Image.open(image_path)
    binary_msg = ''.join(format(ord(c), '08b') for c in message) + DELIMITER

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
    img = Image.open(image_path)
    binary_data = ""
    for pixel in img.getdata():
        r, g, b = pixel
        binary_data += str(r & 1) + str(g & 1) + str(b & 1)

    message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if byte == DELIMITER[:8]:  # check start of delimiter
            if binary_data[i:i+16] == DELIMITER:
                break
        message += chr(int(byte, 2))
    return message


if __name__ == "__main__":
    choice = input("Do you want to (E)ncode or (D)ecode?  : ").strip().lower()
    if choice == 'e':
        image_path = input("Enter the path of the image (without quotes): ").strip()
        message = input("Enter the secret message: ")
        output_path = input("Enter the output image path: ").strip()
        encode_message(image_path, message, output_path)
    elif choice == 'd':
        image_path = input("Enter the path of the encoded image (without quotes): ").strip()
        hidden_message = decode_message(image_path)
        print(f"[📩] Hidden message: {hidden_message}")
    else:
        print("[❌] Invalid choice.")
