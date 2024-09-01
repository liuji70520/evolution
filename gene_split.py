import os
import sys
# 设置路径和参数
gene_tree_dir = sys.argv[1]
merged_fna_dir = sys.argv[2] 
suffix = sys.argv[3]

# 获取所有 .fna 文件名（仅包含存在的.fna文件）
all_fna_files = set()
for species_dir in os.listdir(gene_tree_dir):
    species_dir_path = os.path.join(gene_tree_dir, species_dir)
    if os.path.isdir(species_dir_path):
        for file in os.listdir(species_dir_path):
            if file.endswith(suffix):
                all_fna_files.add(file)

# 创建合并后的文件夹
os.makedirs(merged_fna_dir, exist_ok=True)

# 合并文件
for fna_file in all_fna_files:
    merged_file_path = os.path.join(merged_fna_dir, fna_file)
    with open(merged_file_path, "w") as f_out:
        for species_dir in os.listdir(gene_tree_dir):
            species_dir_path = os.path.join(gene_tree_dir, species_dir)
            if os.path.isdir(species_dir_path):
                fna_file_path = os.path.join(species_dir_path, fna_file)
                if os.path.exists(fna_file_path):
                    # 读取fasta文件并将序列写入合并后的文件
                    with open(fna_file_path, "r") as f_in:
                        f_out.write(f_in.read())  # 直接写入文件内容