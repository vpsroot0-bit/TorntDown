import argparse
import zipfile
import os

def split_file_to_zips(input_path, output_dir, chunk_mb):
    chunk_size = chunk_mb * 1024 * 1024  # تبدیل مگابایت به بایت
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    part_num = 1

    with open(input_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            zip_name = f"{base_name}.part{part_num:03d}.zip"
            zip_path = os.path.join(output_dir, zip_name)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                # داخل zip یک فایل با محتوای بخش قرار می‌دهیم
                zf.writestr(f"{base_name}.chunk{part_num:03d}", chunk)

            print(f"ایجاد شد: {zip_path} ({len(chunk)} bytes)")
            part_num += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="فایل اصلی")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--size-mb", type=int, default=90)
    args = parser.parse_args()
    split_file_to_zips(args.input, args.output_dir, args.size_mb)
