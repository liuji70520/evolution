#!/bin/bash
####注意路径的更改以及对应后缀的更改

# 通过传参获取文件后缀、父级文件夹路径和输出文件夹路径

parent_folder=$1
output_folder=$2
suffix=$3
# 确保输出文件夹存在，如果不存在则创建它
mkdir -p "$output_folder"

# 遍历每个物种文件夹
for folder in "$parent_folder"/*/; do
  # 获取文件夹名称作为物种名
  species_name=$(basename "$folder")

  # 创建对应的输出子文件夹
  output_subfolder="$output_folder/$species_name"
  mkdir -p "$output_subfolder"

  # 遍历所有基因文件
  for file in "$folder"/*.${suffix}; do
    # 获取文件名
    filename=$(basename "$file")

    # 修改后的文件输出到指定输出文件夹
    sed "s/^>/>${species_name}:/" "$file" > "$output_subfolder/$filename"
  done
done
