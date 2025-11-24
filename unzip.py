import os
import zipfile
import tarfile
import shutil

# ================= 配置区域 =================
# 你的压缩包存放路径 (例如: r'D:\Datasets\Underwater')
# '.' 表示当前脚本所在的目录
SOURCE_DIR = r'.'

# 是否解压到单独文件夹？ (True: dataset.zip -> ./dataset/...)
# 强烈建议为 True，防止不同数据集里的同名文件(如 train.txt)互相覆盖
EXTRACT_TO_SUBFOLDER = True

# 是否自动删除 __MACOSX 垃圾文件夹？ (True: 删除)
REMOVE_MACOSX = True


# ===========================================

def extract_zip(file_path, extract_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"[成功-ZIP] {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"[失败-ZIP] {os.path.basename(file_path)}: {e}")
        return False


def extract_tar(file_path, extract_path):
    try:
        with tarfile.open(file_path, 'r:*') as tar_ref:
            tar_ref.extractall(extract_path)
        print(f"[成功-TAR] {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"[失败-TAR] {os.path.basename(file_path)}: {e}")
        return False


def clean_macosx(target_dir):
    """递归删除 __MACOSX 文件夹"""
    for root, dirs, files in os.walk(target_dir, topdown=False):
        for name in dirs:
            if name == "__MACOSX":
                full_path = os.path.join(root, name)
                try:
                    shutil.rmtree(full_path)
                    print(f"  -> 已清理垃圾: {full_path}")
                except Exception as e:
                    print(f"  -> 清理失败: {full_path}, 错误: {e}")


def main():
    # 获取目录下所有文件
    files = [f for f in os.listdir(SOURCE_DIR) if os.path.isfile(os.path.join(SOURCE_DIR, f))]

    print(f"发现 {len(files)} 个文件，开始扫描压缩包...")

    count = 0
    for file in files:
        file_path = os.path.join(SOURCE_DIR, file)
        filename = os.path.splitext(file)[0]  # 文件名不带后缀

        # 确定解压目标路径
        if EXTRACT_TO_SUBFOLDER:
            target_dir = os.path.join(SOURCE_DIR, filename)
        else:
            target_dir = SOURCE_DIR

        is_extracted = False

        # 判断类型并解压
        if file.lower().endswith('.zip'):
            is_extracted = extract_zip(file_path, target_dir)
        elif file.lower().endswith(('.tar', '.tar.gz', '.tgz')):
            is_extracted = extract_tar(file_path, target_dir)

        if is_extracted:
            count += 1
            # 解压完立刻清理垃圾
            if REMOVE_MACOSX:
                clean_macosx(target_dir)

    print(f"\n处理完成！共解压 {count} 个压缩包。")


if __name__ == '__main__':
    main()