import streamlit as st
from PIL import Image
import numpy as np

# 이미지 병합 함수
def merge_images(images, direction="horizontal"):
    if len(images) < 2:
        raise ValueError("이미지를 두 개 이상 업로드하세요.")
    
    # 각 이미지를 같은 크기로 조정
    min_width = min(img.width for img in images)
    min_height = min(img.height for img in images)
    resized_images = [img.resize((min_width, min_height), Image.Resampling.LANCZOS) for img in images]
    
    # 가로 병합 또는 세로 병합
    if direction == "horizontal":
        total_width = sum(img.width for img in resized_images)
        merged_image = Image.new("RGB", (total_width, min_height))
        x_offset = 0
        for img in resized_images:
            merged_image.paste(img, (x_offset, 0))
            x_offset += img.width
    elif direction == "vertical":
        total_height = sum(img.height for img in resized_images)
        merged_image = Image.new("RGB", (min_width, total_height))
        y_offset = 0
        for img in resized_images:
            merged_image.paste(img, (0, y_offset))
            y_offset += img.height
    else:
        raise ValueError("Invalid direction. Choose 'horizontal' or 'vertical'.")
    
    return merged_image

# Streamlit 애플리케이션
def main():
    st.title("이미지 합치기 앱")
    st.write("두 개 이상의 이미지를 업로드하고 가로 또는 세로로 합칠 수 있습니다.")
    
    # 파일 업로드
    uploaded_files = st.file_uploader(
        "이미지를 업로드하세요 (두 개 이상):",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )
    
    if uploaded_files:
        try:
            # 이미지를 PIL 객체로 열기
            images = [Image.open(file) for file in uploaded_files]
            
            # 원본 이미지 출력
            st.subheader("업로드된 이미지")
            for img in images:
                st.image(img, use_column_width=True)
            
            # 병합 방향 선택
            direction = st.radio("이미지를 합치는 방향을 선택하세요:", ("horizontal", "vertical"))
            
            # 병합 버튼
            if st.button("이미지 합치기"):
                merged_image = merge_images(images, direction=direction)
                
                # 병합된 이미지 출력
                st.subheader("병합된 이미지")
                st.image(merged_image, caption="합쳐진 이미지", use_column_width=True)
                
                # 병합된 이미지 다운로드 버튼
                buffer = BytesIO()
                merged_image.save(buffer, format="PNG")
                buffer.seek(0)
                st.download_button(
                    label="합쳐진 이미지 다운로드",
                    data=buffer,
                    file_name="merged_image.png",
                    mime="image/png",
                )
        except Exception as e:
            st.error(f"이미지를 처리하는 동안 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
