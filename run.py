import os
import argparse
import shutil
import sys
from subprocess import call
import time

def run_cmd(command, cwd=None):
    try:
        call(command, shell=True, cwd=cwd)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder", type=str, default="./test_images/old")
    parser.add_argument("--output_folder", type=str, default="./output")
    parser.add_argument("--GPU", type=str, default="6,7")
    parser.add_argument("--checkpoint_name", type=str, default="Setting_9_epoch_100")
    parser.add_argument("--with_scratch", action="store_true")
    parser.add_argument("--HR", action='store_true')
    opts = parser.parse_args()

    opts.input_folder = os.path.abspath(opts.input_folder)
    opts.output_folder = os.path.abspath(opts.output_folder)
    ensure_folder(opts.output_folder)
    # ----------------- Stage 1 -----------------
    print("Running Stage 1: Overall restoration")
    stage_1_output_dir = os.path.join(opts.output_folder, "stage_1_restore_output")
    ensure_folder(stage_1_output_dir)

    if not opts.with_scratch:
        cmd1 = f"python3 test.py --test_mode Full --Quality_restore --test_input {opts.input_folder} --outputs_dir {stage_1_output_dir} --gpu_ids {opts.GPU}"
        run_cmd(cmd1, cwd="./Global")
    else:
        mask_dir = os.path.join(stage_1_output_dir, "masks")
        new_input = os.path.join(mask_dir, "input")
        new_mask = os.path.join(mask_dir, "mask")
        ensure_folder(mask_dir)
        cmd1a = f"python3 detection.py --test_path {opts.input_folder} --output_dir {mask_dir} --input_size full_size --GPU {opts.GPU}"
        HR_suffix = " --HR" if opts.HR else ""
        cmd1b = f"python3 test.py --Scratch_and_Quality_restore --test_input {new_input} --test_mask {new_mask} --outputs_dir {stage_1_output_dir} --gpu_ids {opts.GPU}{HR_suffix}"
        run_cmd(cmd1a, cwd="./Global")
        run_cmd(cmd1b, cwd="./Global")

    # ----------------- Stage 2 -----------------
    print("Running Stage 2: Face Detection")
    stage_2_output_dir = os.path.join(opts.output_folder, "stage_2_detection_output")
    ensure_folder(stage_2_output_dir)
    stage_2_input_dir = os.path.join(stage_1_output_dir, "restored_image")
    if opts.HR:
        cmd2 = f"python3 detect_all_dlib_HR.py --url {stage_2_input_dir} --save_url {stage_2_output_dir}"
    else:
        cmd2 = f"python3 detect_all_dlib.py --url {stage_2_input_dir} --save_url {stage_2_output_dir}"
    run_cmd(cmd2, cwd="./Face_Detection")
    # ----------------- Stage 3 -----------------
    print("Running Stage 3: Face Enhancement")
    stage_3_output_dir = os.path.join(opts.output_folder, "stage_3_face_output")
    ensure_folder(stage_3_output_dir)
    stage_3_input_face = stage_2_output_dir
    stage_3_input_mask = "./"
    if opts.HR:
        opts.checkpoint_name='FaceSR_512'
        cmd3 = f"python3 test_face.py --old_face_folder {stage_3_input_face} --old_face_label_folder {stage_3_input_mask} --tensorboard_log --name {opts.checkpoint_name} --gpu_ids {opts.GPU} --load_size 512 --label_nc 18 --no_instance --preprocess_mode resize --batchSize 1 --results_dir {stage_3_output_dir} --no_parsing_map"
    else:
        cmd3 = f"python3 test_face.py --old_face_folder {stage_3_input_face} --old_face_label_folder {stage_3_input_mask} --tensorboard_log --name {opts.checkpoint_name} --gpu_ids {opts.GPU} --load_size 256 --label_nc 18 --no_instance --preprocess_mode resize --batchSize 4 --results_dir {stage_3_output_dir} --no_parsing_map"
    run_cmd(cmd3, cwd="./Face_Enhancement")
    # ----------------- Stage 4 -----------------
    print("Running Stage 4: Blending")
    stage_4_output_dir = os.path.join(opts.output_folder, "final_output")
    ensure_folder(stage_4_output_dir)
    stage_4_input_image_dir = os.path.join(stage_1_output_dir, "restored_image")
    stage_4_input_face_dir = os.path.join(stage_3_output_dir, "each_img")

    # Chỉ blend nếu Stage 3 có output
    if os.path.exists(stage_3_output_dir) and os.listdir(stage_3_output_dir):
        if opts.HR:
            cmd4 = f"python3 align_warp_back_multiple_dlib_HR.py --origin_url {stage_4_input_image_dir} --replace_url {stage_4_input_face_dir} --save_url {stage_4_output_dir}"
        else:
            cmd4 = f"python3 align_warp_back_multiple_dlib.py --origin_url {stage_4_input_image_dir} --replace_url {stage_4_input_face_dir} --save_url {stage_4_output_dir}"
        run_cmd(cmd4, cwd="./Face_Detection")
    else:
        print("Stage 3 chưa hoàn tất, không blend final output!")

    print("All processing done. Please check results.")
