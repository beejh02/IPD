from ultralytics import YOLO

# 1. COCO pretrained yolov8n 로드
model = YOLO("yolov8n.pt")

# 2. 학습 (증강 인자 추가)
model.train(
    data="data.yml", 
    imgsz=640, 
    epochs=75, 
    batch=8, 
    lr0=0.003, 
    optimizer="AdamW", 
    pretrained=True, 
    device="cpu", 
    patience=20, 
    workers=2, 
    project="runs/train",
    name="custom_yolov8n_augmented",
    freeze=10, 
    
    # 🌟 데이터 증강(Augmentation) 설정 추가 🌟
    # 증강 강도를 높여 작은 데이터셋의 과적합을 방지하고 일반화 성능 향상
    
    # 회전(Rotation) 계열: 0.0 (기본값)에서 10도 회전 적용
    degrees=10.0,
    # 평행 이동(Translation) 계열: 0.1 (기본값)보다 강하게 적용
    translate=0.15,
    # 스케일(Scale) 계열: 0.5 (기본값)보다 강하게 적용
    scale=0.7,
    # 전단(Shear) 계열: 0.0 (기본값)에서 1.0도 적용
    shear=1.0, 
    # 원근(Perspective) 계열: 0.0 (기본값)에서 0.0005 적용
    perspective=0.0005,
    
    # 색상 공간 계열 (작은 데이터셋에서 과적합 방지에 도움)
    # HSV 색조(Hue): 0.015 (기본값)보다 강하게
    hsv_h=0.05,
    # HSV 채도(Saturation): 0.7 (기본값)보다 강하게
    hsv_s=0.9,
    # HSV 명도(Value): 0.4 (기본값)보다 강하게
    hsv_v=0.6,
    
    # 플립 계열 (기본값 유지)
    # 좌우 플립(Horizontal Flip)
    fliplr=0.5, 
    # 상하 플립(Vertical Flip): 객체에 따라 적용 여부 판단 (ex. 하늘 vs 땅)
    flipud=0.0, # 0.0 (기본값): 상하 반전은 일반적으로 객체 인식에서는 비활성화
    
    # 믹스(Mixup) 및 복사-붙여넣기(Copy-paste)
    # 믹스업: 두 이미지를 섞어 학습 데이터로 사용 (과적합 방지 효과)
    mixup=0.1, # 0.0 (기본값)에서 0.1 적용
    # 복사-붙여넣기: 객체를 복사해서 다른 이미지에 붙여넣기 (객체 수 부족 시 유용)
    copy_paste=0.1 # 0.0 (기본값)에서 0.1 적용 (Segment/Detect task)
)