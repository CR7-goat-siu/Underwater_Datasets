import os
import shutil
import cv2
import numpy as np
from tqdm import tqdm
import random

# ================= ⚙️ 配置区域 =================
ROOT_DIR = '.'
TARGET_KEYWORD = "_FR_"
TEST_RATIO = 0.2
ELITE_RATIO = 0.2
IMG_EXTS = ('.jpg', '.png', '.jpeg', '.bmp', '.tif')


# ===============================================

def calculate_image_quality_score(image_path):
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None: return 0
        sharpness = cv2.Laplacian(img, cv2.CV_64F).var()
        contrast = img.std()
        return sharpness + (contrast * 2)
    except Exception:
        return 0


def split_dataset_smart(dataset_name):
    print(f"\n✂️  正在重置并划分: {dataset_name} (精英共享策略)")

    base_path = os.path.join(ROOT_DIR, dataset_name)
    raw_source = os.path.join(base_path, 'raw')
    ref_source = os.path.join(base_path, 'ref')

    train_dir = os.path.join(base_path, 'train')
    test_dir = os.path.join(base_path, 'test')

    # === 🛑 关键步骤: 自动清理旧的 train/test 文件夹 ===
    # 这样可以防止旧数据和新数据混合，避免数据泄露
    if os.path.exists(train_dir):
        print("   [清理] 检测到旧的 train 文件夹，正在删除...", end="")
        shutil.rmtree(train_dir)
        print(" 完成")

    if os.path.exists(test_dir):
        print("   [清理] 检测到旧的 test 文件夹，正在删除...", end="")
        shutil.rmtree(test_dir)
        print(" 完成")
    # =================================================

    # 重新创建目录结构
    train_raw_dir = os.path.join(train_dir, 'raw')
    train_ref_dir = os.path.join(train_dir, 'ref')
    test_raw_dir = os.path.join(test_dir, 'raw')
    test_ref_dir = os.path.join(test_dir, 'ref')

    for d in [train_raw_dir, train_ref_dir, test_raw_dir, test_ref_dir]:
        os.makedirs(d, exist_ok=True)

    # 检查源文件
    if not os.path.exists(ref_source):
        print("   [跳过] 源 ref 文件夹不存在 (可能已经被移动了?)")
        return

    files = sorted([f for f in os.listdir(ref_source) if f.lower().endswith(IMG_EXTS)])
    total_count = len(files)
    if total_count == 0:
        print("   [跳过] 源文件夹为空")
        return

    print(f"   共 {total_count} 张。正在计算质量分数...")

    # 1. 计算分数
    scored_files = []
    for f in tqdm(files, desc="   Scoring"):
        score = calculate_image_quality_score(os.path.join(ref_source, f))
        scored_files.append((f, score))

    # 2. 排序 (High -> Low)
    scored_files.sort(key=lambda x: x[1], reverse=True)

    # 3. 分池
    n_elite = int(total_count * ELITE_RATIO)
    if n_elite < 1: n_elite = 1

    elite_pool = scored_files[:n_elite]
    normal_pool = scored_files[n_elite:]

    # 4. 分配策略
    n_test_total = int(total_count * TEST_RATIO)
    if n_test_total < 1: n_test_total = 1

    # 精英分一半给 Test
    n_test_from_elite = int(n_elite * 0.5)

    n_test_from_normal = n_test_total - n_test_from_elite
    if n_test_from_normal < 0: n_test_from_normal = 0

    random.shuffle(elite_pool)
    random.shuffle(normal_pool)

    test_set = []
    train_set = []

    test_set.extend(elite_pool[:n_test_from_elite])
    train_set.extend(elite_pool[n_test_from_elite:])

    test_set.extend(normal_pool[:n_test_from_normal])
    train_set.extend(normal_pool[n_test_from_normal:])

    random.shuffle(train_set)
    random.shuffle(test_set)

    print(f"   -> 最终划分: Train={len(train_set)} | Test={len(test_set)}")

    # 5. 执行复制
    def copy_files(file_list, dest_type):
        dst_raw_base = train_raw_dir if dest_type == 'train' else test_raw_dir
        dst_ref_base = train_ref_dir if dest_type == 'train' else test_ref_dir

        for fname, _ in tqdm(file_list, desc=f"   Copying to {dest_type.upper()}"):
            src_raw = os.path.join(raw_source, fname)
            src_ref = os.path.join(ref_source, fname)
            dst_raw = os.path.join(dst_raw_base, fname)
            dst_ref = os.path.join(dst_ref_base, fname)

            # 使用 copy2 覆盖写入
            if os.path.exists(src_raw): shutil.copy2(src_raw, dst_raw)
            if os.path.exists(src_ref): shutil.copy2(src_ref, dst_ref)

    copy_files(test_set, 'test')
    copy_files(train_set, 'train')
    print("   ✅ 完成。")


def main():
    print("=" * 60)
    print("   智能数据集划分 (含自动清理旧数据)")
    print("=" * 60)

    datasets = [d for d in os.listdir(ROOT_DIR) if os.path.isdir(d) and TARGET_KEYWORD in d]

    if not datasets:
        print("未找到数据集。")
        return

    for ds in datasets:
        split_dataset_smart(ds)

    print("\n" + "=" * 60)
    print("🎉 重置并划分结束！")
    print("旧的 train/test 已被清除，现在的划分是纯净且包含高质量测试集的。")
    print("=" * 60)


if __name__ == '__main__':
    main()