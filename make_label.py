import os
from glob import glob

import cv2
from ultralytics import YOLO

# -----------------------------
# 설정 부분
# -----------------------------
IMAGE_DIR = "./datasets/images/temp"       # 라벨링할 이미지 폴더
LABEL_DIR = "./datasets/labels/temp"       # YOLO txt 라벨이 저장될 폴더
MODEL_PATH = "./runs/train/custom_yolov8n_augmented/weights/best.pt"  # 사용할 모델 (사전학습 가중치 또는 내 모델)
CONF_THRES = 0.1          # confidence threshold (0~1)
IOU_THRES = 0.4            # NMS IoU threshold

# -----------------------------
# 폴더 준비
# -----------------------------
os.makedirs(LABEL_DIR, exist_ok=True)

# -----------------------------
# 모델 로드
# -----------------------------
print(f"[INFO] Loading model: {MODEL_PATH}")
model = YOLO(MODEL_PATH)

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
# 헬퍼 함수: bbox를 YOLO 형식으로 변환
# -----------------------------
def xyxy_to_yolo(x1, y1, x2, y2, img_w, img_h):
    # 중심 좌표
    x_c = (x1 + x2) / 2.0
    y_c = (y1 + y2) / 2.0
    w = (x2 - x1)
    h = (y2 - y1)

    # 0~1 정규화
    return (
        x_c / img_w,
        y_c / img_h,
        w / img_w,
        h / img_h,
    )

# -----------------------------
# 메인 루프: 자동 라벨링
# -----------------------------
for img_path in image_paths:
    img_name = os.path.basename(img_path)
    label_name = os.path.splitext(img_name)[0] + ".txt"
    label_path = os.path.join(LABEL_DIR, label_name)

    print(f"[INFO] Processing {img_name}")

    # 이미지 읽기 (사이즈 얻기 위함)
    img = cv2.imread(img_path)
    if img is None:
        print(f"[WARN] Cannot read image: {img_path}")
        continue
    img_h, img_w = img.shape[:2]

    # YOLO 모델로 추론
    results = model.predict(
        source=img_path,
        conf=CONF_THRES,
        iou=IOU_THRES,
        verbose=False  # 로그 줄이기
    )

    # 한 이미지에 대해 결과는 보통 하나의 result
    if len(results) == 0:
        print(f"[INFO] No detections for {img_name}")
        # 감지된 게 전혀 없으면 빈 파일 또는 파일 생략
        open(label_path, "w").close()  # 그냥 빈 txt 만들고 싶으면 주석 해제 유지
        continue

    r = results[0]
    boxes = r.boxes  # bbox, cls, conf가 여기 들어 있음

    # 라벨 파일 쓰기
    with open(label_path, "w") as f:
        for box in boxes:
            cls_id = int(box.cls.item())         # 클래스 인덱스
            conf = float(box.conf.item())        # confidence
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # x1,y1,x2,y2

            # YOLO 형식으로 변환
            x_c, y_c, w, h = xyxy_to_yolo(x1, y1, x2, y2, img_w, img_h)

            # "class x_center y_center width height"
            line = f"{cls_id} {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}\n"
            f.write(line)

    print(f"[INFO] Saved labels to {label_path}")

print("[DONE] Auto labeling finished!")
