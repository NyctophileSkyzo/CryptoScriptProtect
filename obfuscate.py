#https://github.com/NyctophileSkyzo/CryptoScriptProtect?tab=readme-ov-file#license
import random
import base64
import zlib
import sys
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import marshal

# Meningkatkan batas rekursi
sys.setrecursionlimit(1000000000)

# Fungsi untuk membersihkan layar
def clear():
    os = __import__("os")
    platform = __import__("sys").platform
    os.system("clear" if "linux" in platform.lower() else "cls")

# Fungsi enkripsi AES sederhana
def aes_encrypt(data, key):
    key = hashlib.sha256(key.encode("utf-8")).digest()
    iv = random.getrandbits(128).to_bytes(16, "big")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
    return base64.b64encode(iv + encrypted).decode("utf-8")

# Fungsi dekripsi AES sederhana
def aes_decrypt(encrypted, key):
    key = hashlib.sha256(key.encode("utf-8")).digest()
    encrypted = base64.b64decode(encrypted.encode("utf-8"))
    iv = encrypted[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted[16:]), AES.block_size)
    return decrypted.decode("utf-8")

# Membersihkan layar sebelum memulai
clear()

# Membaca skrip asli dari file input
input_file = input("[-] Input file : ")
with open(input_file, "r", encoding="utf-8") as file:
    original_script = file.read()

# Fungsi untuk melakukan obfuscation berulang
def obfuscate_script(script, iterations):
    for _ in range(iterations):
        # Generate random key
        secret_key = "".join(random.choices("0123456789ABCDEF", k=16))
        # Konversi secret_key ke dalam format string Python yang dapat dibaca
        secret_key_repr = repr(secret_key)
        encrypted_script = aes_encrypt(script, secret_key)
        # Konversi encrypted_script ke dalam format string Python yang dapat dibaca
        encrypted_script_repr = repr(encrypted_script)

        # Setup kode obfuscasi
        obfuscated_code = f"""
import base64
import zlib
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def aes_decrypt(encrypted, key):
    key = hashlib.sha256(key.encode()).digest()
    encrypted = base64.b64decode(encrypted)
    iv = encrypted[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted[16:]), AES.block_size)
    return decrypted.decode()

key = {secret_key_repr}
encrypted_script = {encrypted_script_repr}
exec(aes_decrypt(encrypted_script, key))
"""

        # Kompresi dan encoding kode obfuscasi
        compressed_code = zlib.compress(obfuscated_code.encode())
        encoded_code = base64.b64encode(compressed_code).decode()

        # Kompilasi menggunakan marshal
        compiled_code = marshal.dumps(
            compile(
                f"""
import base64
import zlib
exec(zlib.decompress(base64.b64decode("{encoded_code}")).decode())
""",
                "<string>",
                "exec",
            )
        )

        # Final obfuscated script
        obfuscated = f"""
import marshal
exec(marshal.loads({repr(compiled_code)}))
"""
        
        # Kompilasi menggunakan marshal lagi
        compiled_ = marshal.dumps(compile(obfuscated, '<string>', 'exec'))
        script = f"""
import marshal
exec(marshal.loads({repr(compiled_)}))
"""
    return script

# Meminta input jumlah lapisan obfuscation
loop = int(input("[-] Count : "))
if loop > 350:
    print("Batasnya hanya 350")
    sys.exit()

# Obfuscate script
final_script = obfuscate_script(original_script, loop)

# Menyimpan final_script ke file output
output_file = input("[-] Output file : ")
with open(output_file, "w", encoding="utf-8") as file:
    file.write(final_script)
print(f"Final obfuscated script has been saved to {output_file}")
