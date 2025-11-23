from PIL import Image
import os

input_folder = "./datasets/images/val"      # 원본 이미지 폴더
target_size = (512, 512)           # 원하는 해상도

for file in os.listdir(input_folder):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        try:
            img_path = os.path.join(input_folder, file)
            img = Image.open(img_path).convert("RGB")   # PNG 문제 방지

            # 리사이즈
            img = img.resize(target_size, Image.LANCZOS)

            # 원본 위치에 그대로 덮어쓰기
            img.save(img_path, quality=90, optimize=True)

            print(f"{file} 리사이즈 및 대체 완료")

        except Exception as e:
            print(f"{file} 처리 중 오류 발생: {e}")

print("전체 이미지 덮어쓰기 리사이즈 완료!")
