import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
trimal_output_dir = sys.argv[1]
species_tree_dir = sys.argv[2]
suffix=sys.argv[3]


gene_files = [
    f for f in os.listdir(trimal_output_dir) if f.endswith("."+suffix)
]  # 获取所有基因文件名
gene_files.sort()  # 按文件名排序

# 初始化物种列表和基因长度字典
species_names = set()
gene_lengths = {}

# 统计信息
for gene_file in gene_files:
    gene_file_path = os.path.join(trimal_output_dir, gene_file)
    gene_name = "_".join(gene_file.split("_")[:-1])  #获取基因名

    with open(gene_file_path, "r") as f:
        for record in SeqIO.parse(f, "fasta"):
            species_name = record.id.split(":")[0] # 获取物种名
            species_names.add(species_name)  # 添加到物种列表中

    # 记录基因长度（使用第一个物种的序列长度即可）
    with open(gene_file_path, "r") as f:
        for record in SeqIO.parse(f, "fasta"):
            gene_lengths[gene_name] = len(str(record.seq))
            break

# 拼接序列
species_sequences = {}
for species_name in species_names:
    species_sequences[species_name] = ""
    for gene_file in gene_files:
        gene_name = "_".join(gene_file.split("_")[:-1])  # 获取基因名
        gene_file_path = os.path.join(trimal_output_dir, gene_file)

        # 读取基因序列
        with open(gene_file_path, "r") as f:
            for record in SeqIO.parse(f, "fasta"):
                if record.id.split(":")[0] == species_name:
                    species_sequences[species_name] += str(record.seq)
                    break
            else:
                # 如果该物种在该基因文件中不存在，则添加空位
                species_sequences[species_name] += "-" * gene_lengths.get(
                    gene_name, 100
                )

# 创建输出文件夹
os.makedirs(species_tree_dir, exist_ok=True)

# 保存拼接后的序列到文件
for species_name, sequence in species_sequences.items():
    record = SeqRecord(Seq(sequence), id=species_name, description="")
    output_file = os.path.join(species_tree_dir, f"{species_name}.{suffix}")
    with open(output_file, "w") as f:
        SeqIO.write(record, f, "fasta")