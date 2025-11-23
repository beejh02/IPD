from ultralytics import YOLO

# 1. COCO pretrained yolov8n 로드 (데이터 50장에 가장 적합)
model = YOLO("yolov8n.pt")

# 2. 학습
model.train(
    data="data.yml",       # 데이터 yaml
    imgsz=480,             # 원본 비율 맞출 필요 없으면 480~640 적절
    epochs=50,             # 50~100 권장, early stopping 활성화
    batch=8,               # 50장 데이터에서 batch는 너무 크지 않게
    lr0=0.003,             # 기본보다 약간 안정적인 초기 LR
    optimizer="AdamW",     # 작은 데이터일수록 AdamW 안정적
    pretrained=True,       # pretrained 반드시 사용
    device="cpu",          # GPU 있으면 "0"으로 변경
    patience=20,           # 검증 성능 정체 시 자동 early stopping
    workers=2,             # 데이터로더 워커 수
    project="runs/train",
    name="custom_yolov8n",

    # 백본 일부 freeze → 작은 데이터에서 과적합 방지 효과 큼
    freeze=10,             # 앞단 10개 레이어 고정 (필요 시 조절)
)
