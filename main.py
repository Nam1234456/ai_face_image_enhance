import streamlit as st
from PIL import Image, UnidentifiedImageError
import os
import subprocess
import sys
import shutil
import time
import imghdr

st.set_page_config(page_title="Phục hồi ảnh cũ", layout="wide")
st.title("Phục hồi chất lượng ảnh cũ")

uploaded = st.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png"])

if uploaded:
    orig = Image.open(uploaded).convert("RGB")

    # 5 cột: ảnh gốc + 4 stage
    col0, col1, col2, col3, col4 = st.columns(5)
    with col0:
        st.subheader("Ảnh gốc")
        st.image(orig, use_container_width=True)

    if st.button("Chạy phục hồi (4 stage)"):
        tmp_input = os.path.abspath("./tmp_input_folder")
        tmp_output = os.path.abspath("./tmp_output_folder")

        # Xóa folder cũ nếu tồn tại
        for folder in [tmp_input, tmp_output]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
            os.makedirs(folder, exist_ok=True)

        # Lưu ảnh người dùng vào folder input
        input_path = os.path.join(tmp_input, "input.png")
        orig.save(input_path)

        run_py_path = os.path.abspath("./run.py")
        cmd = [sys.executable, run_py_path,
               "--input_folder", tmp_input,
               "--output_folder", tmp_output,
               "--GPU", "-1",
               "--with_scratch"]

        # Chạy run.py trong subprocess riêng
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Stage folders và placeholder
        stage_folders = [
            "stage_1_restore_output/restored_image",
            "stage_2_detection_output",
            "stage_3_face_output/each_img",
            "final_output"
        ]
        stage_names = ["1. Globale restore", "2. Face detection", "3. Face Enhance", "4. Final Output"]
        cols = [col1, col2, col3, col4]

        # Tạo 2 placeholder cho mỗi stage
        title_placeholders = [col.empty() for col in cols]
        image_placeholders = [col.empty() for col in cols]
        displayed = [False] * 4

        while True:
            all_done = True
            for i, (folder, title_ph, img_ph, name) in enumerate(zip(stage_folders, title_placeholders, image_placeholders, stage_names)):
                folder_path = os.path.join(tmp_output, folder)
                img_path = None
                if os.path.exists(folder_path):
                    files = sorted(os.listdir(folder_path))
                    for f in files:
                        full_path = os.path.join(folder_path, f)
                        if imghdr.what(full_path):
                            img_path = full_path
                            break

                title_ph.subheader(name)  # Luôn hiển thị stage name
                if img_path:
                    if not displayed[i]:
                        try:
                            img = Image.open(img_path)
                            img_ph.image(img, caption=name, use_container_width=True)
                            displayed[i] = True
                        except UnidentifiedImageError:
                            all_done = False
                            img_ph.write("Chưa hoàn tất…")
                else:
                    all_done = False
                    if not displayed[i]:
                        img_ph.write("Chưa hoàn tất…")

            if process.poll() is not None and all(displayed):
                break
            time.sleep(1)

        # Hiển thị thông báo hoàn tất
        st.success("Pipeline phục hồi hoàn tất!")