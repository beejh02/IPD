import os
import time  # 잠시 대기하기 위해 time 모듈 추가

target_dir = './datasets/labels/train' 
count = 0

if not os.path.isdir(target_dir):
    print(f"오류: 지정된 디렉토리 '{target_dir}'를 찾을 수 없습니다.")
else:
    for filename in os.listdir(target_dir):
        full_path = os.path.join(target_dir, filename) 
        
        if filename.endswith(".txt") and os.path.isfile(full_path):
            
            # 파일을 읽는 부분
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    
                if first_line.startswith('2 '): 
                    print(f"삭제 예정 파일: {filename} (경로: {full_path})")
                    
                    # 파일을 삭제하는 부분 (WinError 32에 대한 처리 추가)
                    try:
                        os.remove(full_path) 
                        count += 1
                    except PermissionError as pe: # PermissionError (WinError 32 포함)
                        print(f"⚠️ [WinError 32] 삭제 실패: {filename} - 다른 프로세스가 파일을 사용 중입니다. (오류: {pe})")
                        
                        # 3초 대기 후 재시도 (선택 사항)
                        # time.sleep(3)
                        # try:
                        #     os.remove(full_path)
                        #     print(f"재시도 성공: {filename} 삭제 완료.")
                        #     count += 1
                        # except Exception:
                        #     print(f"재시도 실패: {filename} 삭제 불가능.")
                        
            except Exception as e:
                # 파일 인코딩 문제나 경로 문제가 있을 경우
                print(f"파일 내용 처리 중 오류 발생 {filename}: {e}")

    print(f"총 {count}개의 파일이 조건에 해당하여 삭제되었습니다.")