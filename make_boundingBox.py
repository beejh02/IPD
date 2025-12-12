import os
from glob import glob

import cv2

# -----------------------------
# 설정 부분 (네 환경에 맞게 바꿔도 됨)
# -----------------------------
IMAGE_DIR = "./datasets/images/train/"   # 원본 이미지 폴더
LABEL_DIR = "./datasets/labels/train/"   # YOLO txt5 라벨 폴더
OUTPUT_DIR = "./vis/"     # 박스가 그려진 결과 이미지 저장 폴더

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# 헬퍼 함수: YOLO -> xyxy 변환
# -----------------------------
def yolo_to_xyxy(x_c, y_c, w, h, img_w, img_h):
    """
    x_c, y_c, w, h : 0~1 정규화된 값 (YOLO 형식)
    img_w, img_h   : 이미지 크기 (픽셀)
    return         : x1, y1, x2, y2 (픽셀 좌표)
    """
    x_c *= img_w
    y_c *= img_h
    w   *= img_w
    h   *= img_h

    x1 = int(x_c - w / 2)
    y1 = int(y_c - h / 2)
    x2 = int(x_c + w / 2)
    y2 = int(y_c + h / 2)

    # 이미지 범위를 벗어나지 않도록 클램프
    x1 = max(0, min(x1, img_w - 1))
    y1 = max(0, min(y1, img_h - 1))
    x2 = max(0, min(x2, img_w - 1))
    y2 = max(0, min(y2, img_h - 1))

    return x1, y1, x2, y2

# -----------------------------
# 이미지 리스트 가져오기
# -----------------------------
extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
image_paths = []
for ext in extensions:
    image_paths.extend(glob(os.path.join(IMAGE_DIR, ext)))

image_paths = sorted(image_paths)

print(f"[INFO] Found {len(image_paths)} images in '{IMAGE_DIR}'")

# -----------------------------
# 메인 루프: 라벨 읽어서 박스 그리기
# -----------------------------
for img_path in image_paths:
    img_name = os.path.basename(img_path)
    label_name = os.path.splitext(img_name)[0] + ".txt"
    label_path = os.path.join(LABEL_DIR, label_name)

    print(f"[INFO] Processing {img_name}")

    # 이미지 읽기
    img = cv2.imread(img_path)
    if img is None:
        print(f"[WARN] Cannot read image: {img_path}")
        continue
    img_h, img_w = img.shape[:2]

    # 라벨 파일이 없으면 스킵
    if not os.path.exists(label_path):
        print(f"[INFO] Label file not found: {label_path}")
        continue

    # 라벨 파일 읽기
    with open(label_path, "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        print(f"[INFO] Empty label file (no boxes): {label_path}")
        # 빈 라벨이면 그냥 원본을 복사해서 저장하거나, 스킵해도 됨
        # 여기서는 그냥 원본 그대로 저장
        out_path = os.path.join(OUTPUT_DIR, img_name)
        cv2.imwrite(out_path, img)
        continue

    # 각 라인마다 박스 그리기
    for line in lines:
        line = line.strip()
        if line == "":
            continue

        # YOLO 포맷: class x_center y_center width height
        parts = line.split()
        if len(parts) != 5:
            print(f"[WARN] Invalid label format in {label_path}: {line}")
            continue

        cls_id = int(parts[0])
        x_c = float(parts[1])
        y_c = float(parts[2])
        w   = float(parts[3])
        h   = float(parts[4])

        # YOLO -> 픽셀 좌표 변환
        x1, y1, x2, y2 = yolo_to_xyxy(x_c, y_c, w, h, img_w, img_h)

        # 박스 그리기 (BGR 색상, 두께 2)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 클래스 id를 텍스트로 표시 (옵션)
        text = str(cls_id)
        cv2.putText(
            img,
            text,
            (x1, max(y1 - 5, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

    # 결과 이미지 저장
    out_path = os.path.join(OUTPUT_DIR, img_name)
    cv2.imwrite(out_path, img)
    print(f"[INFO] Saved visualized image to {out_path}")

print("[DONE] Visualization finished!")