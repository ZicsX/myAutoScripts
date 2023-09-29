import os
import zipfile
from shutil import rmtree

def divide_files(files):
    avg = len(files) // 5
    return [files[n:n+avg] for n in range(0, len(files), avg)]

def shard_zip(input_folder, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for item in os.listdir(input_folder):
        zip_path = os.path.join(input_folder, item)
        if zipfile.is_zipfile(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                temp_dir = os.path.join(output_dir, item.replace('.zip', ''))
                zip_ref.extractall(temp_dir)

                txt_files = [f for f in os.listdir(os.path.join(temp_dir, os.listdir(temp_dir)[0])) if f.endswith('.txt')]
                file_groups = divide_files(txt_files)

                for idx, file_group in enumerate(file_groups, 1):
                    shard_zip_name = f"{item.replace('.zip', '')}_{chr(96 + idx)}"
                    shard_zip_path = os.path.join(output_dir, f"{shard_zip_name}.zip")
                    with zipfile.ZipFile(shard_zip_path, 'w') as shard_zip:
                        for txt_file in file_group:
                            shard_zip.write(
                                os.path.join(temp_dir, os.listdir(temp_dir)[0], txt_file),
                                arcname=txt_file
                            )

                rmtree(temp_dir)

input_folder = 'input'
output_dir = 'output'
shard_zip(input_folder, output_dir)
