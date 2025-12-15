import os

def rename_images_in_directory(root_dir, start_number=1):
    """
    root_dir 안의 이미지 파일만(하위 폴더 제외)
    지정된 start_number부터 순서대로 이름 변경 (예: 10.jpg, 11.jpg, ...)
    
    :param root_dir: 이미지 파일이 있는 디렉토리 경로
    :param start_number: 파일 이름에 사용할 시작 숫자 (기본값: 1)
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
    # 시작 숫자를 반영하여 임시 이름의 인덱스를 조정합니다.
    temp_paths = []
    # enumerate의 start 값을 start_number로 설정합니다.
    for idx, old_path in enumerate(image_paths, start=start_number):
        ext = os.path.splitext(old_path)[1].lower()
        temp_name = f"__tmp_image_{idx}{ext}"
        temp_path = os.path.join(root_dir, temp_name)
        os.rename(old_path, temp_path)
        temp_paths.append(temp_path)

    # 최종 이름 변경
    # enumerate의 start 값을 start_number로 설정합니다.
    for idx, temp_path in enumerate(temp_paths, start=start_number):
        ext = os.path.splitext(temp_path)[1].lower()
        new_name = f"{idx}{ext}"
        new_path = os.path.join(root_dir, new_name)
        os.rename(temp_path, new_path)
        print(f"**{temp_path}** -> **{new_path}**")

    print("[완료] 이미지 정렬 끝.")


# 실행 예시
if __name__ == "__main__":
    rename_images_in_directory("./datasets/images/temp", start_number=157)