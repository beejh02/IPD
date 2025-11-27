from ultralytics import YOLO
import cv2
import numpy as np

# OpenCV 라운드 박스 그리기 함수
def draw_round_rect(img, x1, y1, x2, y2, color, thickness=2, radius=10):
    # 네모의 점들
    points = [(x1+radius, y1),
              (x2-radius, y1),
              (x2, y1+radius),
              (x2, y2-radius),
              (x2-radius, y2),
              (x1+radius, y2),
              (x1, y2-radius),
              (x1, y1+radius)]

    # 직선 부분 그리기
    cv2.line(img, points[0], points[1], color, thickness)
    cv2.line(img, points[2], points[3], color, thickness)
    cv2.line(img, points[4], points[5], color, thickness)
    cv2.line(img, points[6], points[7], color, thickness)

    # 네 모서리에 원호 넣어서 라운딩
    cv2.ellipse(img, (x1+radius, y1+radius), (radius, radius), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2-radius, y1+radius), (radius, radius), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x2-radius, y2-radius), (radius, radius), 0, 0, 90, color, thickness)
    cv2.ellipse(img, (x1+radius, y2-radius), (radius, radius), 90, 0, 90, color, thickness)


# -----------------------------
# YOLO 원본 코드 + 수정 사항
# -----------------------------

# 1. 학습된 모델 불러오기
model = YOLO("./runs/train/custom_yolov8n_augmented/weights/best.pt")

img_path = "reshape_image.png"

# 2. 이미지 예측
results = model.predict(
    source=img_path,
    conf=0.3,
    save=False, 
    show=False
)

# 3. 원본 이미지 읽기
orig_img = cv2.imread(img_path)

# 4. 결과 출력 + 라운드박스 그리기
for r in results:
    boxes = r.boxes

    print(f"\n이미지: {img_path}")
    print(f"탐지된 객체 수: {len(boxes)}")

    if len(boxes) == 0:
        print("→ 탐지된 객체가 없습니다.")
    else:
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

            print(f"class: {cls_id}, conf: {conf:.2f}, box: {[x1, y1, x2, y2]}")

            # 라운드 박스 그리기
            draw_round_rect(orig_img, x1, y1, x2, y2, (0, 255, 0), thickness=2, radius=12)

            # 라벨 텍스트
            label = f"{cls_id} {conf:.2f}"
            cv2.putText(orig_img, label, (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 5. 저장
save_path = "result_round_box.jpg"
cv2.imwrite(save_path, orig_img)
print(f"\n라운드 박스 이미지 저장 완료: {save_path}")
