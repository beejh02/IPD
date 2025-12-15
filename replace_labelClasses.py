import os
from glob import glob

# -----------------------------
# 설정
# -----------------------------
LABEL_DIR = "./datasets/labels/temp/"   # 라벨 txt 폴더

# -----------------------------
# txt 파일 목록 가져오기
# -----------------------------
label_paths = sorted(glob(os.path.join(LABEL_DIR, "*.txt")))
print(f"[INFO] Found {len(label_paths)} label files")

# -----------------------------
# 클래스 ID를 모두 0으로 변환 (덮어쓰기 버전)
# -----------------------------
for label_path in label_paths:
    with open(label_path, "r") as f:
        lines = f.readlines()

    fixed_lines = []

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        parts = line.split()
        if len(parts) != 5:
            print(f"[WARN] Invalid label format in {label_path}: {line}")
            continue

        # 기존 class는 버리고 0으로 고정
        _, x, y, w, h = parts
        fixed_line = f"2 {x} {y} {w} {h}\n"
        fixed_lines.append(fixed_line)

    # 기존 파일을 덮어쓰기
    with open(label_path, "w") as f:
        f.writelines(fixed_lines)

    print(f"[INFO] Overwritten label file → {label_path}")
