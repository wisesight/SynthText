import os

from glob import glob
from argparse import ArgumentParser

def run_generate_synth_text(all_fonts_path, font_familiy_path):
    # edit fontlists.txt
    with open(os.path.join(all_fonts_path, "fontlist.txt"), "w") as font_list_file:
        _font_files_paths = glob(os.path.join(font_familiy_path, "*"))
        font_files_paths = [font_family_path.replace(all_fonts_path, "") for font_family_path in _font_files_paths]
        
        font_list_file.write("\n".join(font_files_paths))
    
    invert_font_size_run_status = os.system("python prep_scripts/invert_font_size.py")
    if invert_font_size_run_status != 0:
        print(f"Unsucessfully invert_font_size on :{font_familiy_path}")
        exit(1)

    generate_run_status_code = -9999

    # Handle pygame unsucessful run
    while generate_run_status_code != 0:
        generate_run_status_code = os.system(f"python _gen.py --out_dir {os.path.join('results', os.path.basename(font_familiy_path))}")

def main():
    parser = ArgumentParser()
    parser.add_argument("--fonts_dir", type = str, default="data/fonts/")

    args = parser.parse_args()


    font_families_path = sorted(glob(os.path.join(args.fonts_dir, "*[!.txt]")))
    for font_family_path in font_families_path:
        run_generate_synth_text(args.fonts_dir, font_family_path)

if __name__ == "__main__":
    main()