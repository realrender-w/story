import os
from face_swap import swap_face
from text_replace import replace_name_in_image

TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

def generate_story(child_name, child_image_path):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ✅ Step 1: Process cover page (if exists)
    cover_template = os.path.join(TEMPLATE_DIR, "cover.png")
    cover_output = os.path.join(OUTPUT_DIR, f"cover_{child_name.lower()}.png")
    if os.path.exists(cover_template):
        try:
            replace_name_in_image(cover_template, child_name, cover_output)
            print(f"[📘] Cover page generated: {cover_output}")
        except Exception as e:
            print(f"[⚠️] Failed to process cover page: {e}")

    # ✅ Step 2: Process all available pageX.png templates
    template_files = sorted([
        f for f in os.listdir(TEMPLATE_DIR)
        if f.startswith("page") and f.endswith(".png")
    ])

    for filename in template_files:
        page_number = filename.replace("page", "").replace(".png", "")
        template_path = os.path.join(TEMPLATE_DIR, filename)
        swapped_path = os.path.join(OUTPUT_DIR, f"{filename.replace('.png', '_swapped.png')}")
        final_output_path = os.path.join(OUTPUT_DIR, f"page{page_number}_{child_name.lower()}.png")

        print(f"[🖼️] Processing page {page_number}...")

        # Step 1: Face swap
        try:
            swap_face(template_path, child_image_path, swapped_path)
        except Exception as e:
            print(f"[❌] Face swap failed on page {page_number}: {e}")
            continue

        # Step 2: Text replacement
        try:
            if os.path.exists(swapped_path):
                replace_name_in_image(swapped_path, child_name, final_output_path)
            else:
                print(f"[⚠️] Skipped text replacement — swapped file not found for page {page_number}.")
        except Exception as e:
            print(f"[❌] Text replacement failed on page {page_number}: {e}")

