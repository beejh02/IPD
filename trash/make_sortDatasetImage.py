import os

def rename_images_in_directory(root_dir):
    """
    root_dir 아래의 모든 하위 디렉토리를 포함해서
    이미지 파일들을 1.jpg, 2.jpg, ... 순서로 이름 변경
    """

    # 지원하는 확장자들
    IMG_EXT = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

    # 1. 모든 이미지 경로 모으기 (하위 폴더 포함)
    image_paths = []
    for cur_dir, _, files in os.walk(root_dir):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in IMG_EXT:
                full_path = os.path.join(cur_dir, f)
                image_paths.append(full_path)

    # 정렬 (경로 기준)
    image_paths.sort()

    print(f"[정보] 찾은 이미지 파일 개수: {len(image_paths)}")
    if not image_paths:
        print("[경고] 이미지 파일을 하나도 못 찾았습니다.")
        print(" - 경로가 맞는지 확인하세요.")
        print(" - 확장자가 .jpg/.png 같은 형식인지 확인하세요.")
        return

    # 2단계로 이름 변경 (이름 충돌 방지)
    # 2-1. 먼저 임시 이름으로 변경
    temp_paths = []
    for idx, old_path in enumerate(image_paths, start=1):
        dir_name = os.path.dirname(old_path)
        ext = os.path.splitext(old_path)[1].lower()
        temp_name = f"__tmp_image_{idx}{ext}"
        temp_path = os.path.join(dir_name, temp_name)
        os.rename(old_path, temp_path)
        temp_paths.append(temp_path)

    # 2-2. 이제 최종 이름 1.jpg, 2.jpg ... 로 변경
    counter = 1
    for temp_path in temp_paths:
        dir_name = os.path.dirname(temp_path)
        ext = os.path.splitext(temp_path)[1].lower()
        new_name = f"{counter}{ext}"
        new_path = os.path.join(dir_name, new_name)
        os.rename(temp_path, new_path)
        print(f"{temp_path}  ->  {new_path}")
        counter += 1

    print("[완료] 모든 이미지 파일 이름이 순서대로 변경되었습니다.")


# ==============================
# 사용 예시
# ==============================
if __name__ == "__main__":
    # 👉 여기 경로만 네 폴더 경로로 바꿔서 실행하면 돼
    # 윈도우 예시:
    #   r"C:\Users\USER\Desktop\images"
    # 리눅스/맥 예시:
    #   "/home/user/images"
    target_dir = "./"  # 여기를 수정!

    rename_images_in_directory(target_dir)
