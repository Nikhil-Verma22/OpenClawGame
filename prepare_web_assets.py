import os
import json

CHUNK_SIZE = 20 * 1024 * 1024  # 20 MB per chunk (well below 25 MB limit)

def split_file(filepath, prefix):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return [], 0
    
    file_size = os.path.getsize(filepath)
    part_files = []
    
    with open(filepath, "rb") as f:
        part_num = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            part_name = f"{prefix}.part{part_num:02d}"
            part_path = os.path.join(os.path.dirname(filepath), part_name)
            with open(part_path, "wb") as pf:
                pf.write(chunk)
            part_files.append(part_name)
            print(f"Created {part_name} ({len(chunk)} bytes)")
            part_num += 1
            
    return part_files, file_size

def main():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Build_Release")
    
    wasm_path = os.path.join(base_dir, "openclaw.wasm")
    data_path = os.path.join(base_dir, "openclaw.data")
    
    print("Splitting openclaw.wasm...")
    wasm_parts, wasm_size = split_file(wasm_path, "openclaw.wasm")
    
    print("Splitting openclaw.data...")
    data_parts, data_size = split_file(data_path, "openclaw.data")
    
    manifest = {
        "wasmParts": wasm_parts,
        "wasmSize": wasm_size,
        "dataParts": data_parts,
        "dataSize": data_size
    }
    
    manifest_path = os.path.join(base_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote manifest.json to {manifest_path}")

if __name__ == "__main__":
    main()
