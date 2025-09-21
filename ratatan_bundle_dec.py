import sys
from pathlib import Path

KEY_STRING = "譬ｪ蠑丈ｼ夂､ｾTVT縺ｯ蜆ｪ遘?縺ｪ繧ｽ繝輔ヨ繧ｦ繧ｧ繧｢繝励Ο繧ｰ繝ｩ繝槭?繧貞供髮?＠縺ｦ縺?∪縺吮飭"
ENGINE_VER = "2022.3.61f1"

def xor_with_key(data: bytes, key: bytes) -> bytes:
    klen = len(key)
    return bytes(b ^ key[i % klen] for i, b in enumerate(data))

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(2)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])

    if not in_path.is_file():
        print("Input file not found.")
        sys.exit(1)

    key = KEY_STRING.encode("utf-8")
    data = in_path.read_bytes()
    result = xor_with_key(data, key)
    out_path.write_bytes(result)

if __name__ == "__main__":
    main()
