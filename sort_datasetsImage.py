import os

def rename_images_in_directory(root_dir):
    """
    root_dir 안의 이미지 파일만(하위 폴더 제외)
    1.jpg, 2.jpg, ... 순서로 이름 변경
    """

    # 지원하는 확장자들
    IMG_EXT = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}

    # 1. root_dir 안의 파일만 검사
    files = os.listdir(root_dir)

    # 이미지 파일만 필터링
    image_paths = [
        os.path.join(root_dir, f) for f in files
        if os.path.splitext(f)[1].lower() in IMG_EXT
    ]

    # 정렬
    image_paths.sort()

    print(f"[정보] 찾은 이미지 파일 개수: {len(image_paths)}")
    if not image_paths:
        print("[경고] 이미지 파일을 하나도 못 찾았습니다.")
        return

    # 2단계 이름 변경 (충돌 방지)
    temp_paths = []
    for idx, old_path in enumerate(image_paths, start=1):
        ext = os.path.splitext(old_path)[1].lower()
        temp_name = f"__tmp_image_{idx}{ext}"
        temp_path = os.path.join(root_dir, temp_name)
        os.rename(old_path, temp_path)
        temp_paths.append(temp_path)

    # 최종 이름 변경
    for idx, temp_path in enumerate(temp_paths, start=1):
        ext = os.path.splitext(temp_path)[1].lower()
        new_name = f"{idx}{ext}"
        new_path = os.path.join(root_dir, new_name)
        os.rename(temp_path, new_path)
        print(f"{temp_path} -> {new_path}")

    print("[완료] 이미지 정렬 끝.")


# 실행 예시
if __name__ == "__main__":
    rename_images_in_directory("./datasets/images/temp")  # 원하는 경로로 변경