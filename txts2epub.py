import os
 
def merge_files(input_folder, output_file):
    # 确保输出文件不存在时创建，存在时清空
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # 遍历文件夹中的所有文件
        for filename in sorted(os.listdir(input_folder)):
            # 检查文件名是否以 "00-" 或 "20-" 开头，并且以 ".txt" 结尾
            if filename.endswith('.txt'):
                # 构建文件的完整路径
                file_path = os.path.join(input_folder, filename)
                
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as infile:
                    file_content = infile.read()
                
                # 写入合并后的文件
                outfile.write(f"# {filename}\n\n")
                outfile.write(file_content+"\n")
                outfile.write("\n")  # 添加换行符以分隔不同文件的内容
 
# 示例用法
input_folder = '../../Downloads/生活中的传播学'  # 替换为你的输入文件夹路径
output_file = './book2.txt'  # 替换为你的输出文件路径
 
merge_files(input_folder, output_file)