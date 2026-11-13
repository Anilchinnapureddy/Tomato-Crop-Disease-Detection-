"""
Dataset Setup & Quick Verification Helper
Generates organized class directories and realistic synthetic sample images
for all 10 tomato leaf classes so the project can be trained and tested immediately.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFilter

CLASSES = [
    "Tomato___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites_Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus"
]

DATASET_ROOT = os.path.join(os.path.dirname(__file__), "dataset")


def draw_leaf_base(draw, width, height, base_color):
    """Draws a natural serrated leaf shape on a neutral background."""
    # Leaf main body (ellipse / polygon)
    center_x = width // 2
    center_y = height // 2
    draw.polygon(
        [
            (center_x, 20),
            (center_x + 75, center_y - 40),
            (center_x + 85, center_y + 20),
            (center_x + 55, center_y + 80),
            (center_x, height - 25),
            (center_x - 55, center_y + 80),
            (center_x - 85, center_y + 20),
            (center_x - 75, center_y - 40),
        ],
        fill=base_color,
        outline=(20, 60, 20)
    )
    # Leaf stem
    draw.line([(center_x, 25), (center_x, height - 20)], fill=(30, 80, 25), width=3)
    # Leaf veins
    for dy in range(40, height - 40, 25):
        draw.line([(center_x, dy), (center_x + 45, dy - 15)], fill=(35, 95, 30), width=1)
        draw.line([(center_x, dy), (center_x - 45, dy - 15)], fill=(35, 95, 30), width=1)


def generate_sample_leaf(class_name: str, width: int = 224, height: int = 224) -> Image.Image:
    """Generates a synthetic leaf image with class-specific visual symptoms."""
    img = Image.new("RGB", (width, height), color=(240, 238, 230))
    draw = ImageDraw.Draw(img)

    # Base leaf color
    if "healthy" in class_name.lower():
        draw_leaf_base(draw, width, height, (46, 125, 50))
    elif "yellow" in class_name.lower():
        draw_leaf_base(draw, width, height, (180, 195, 45))
        # Yellow curled edges
        for _ in range(30):
            x = random.randint(30, 190)
            y = random.randint(30, 190)
            r = random.randint(6, 14)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=(235, 215, 50, 180))
    elif "mosaic" in class_name.lower():
        draw_leaf_base(draw, width, height, (80, 150, 60))
        # Mosaic mottled patches
        for _ in range(40):
            x = random.randint(40, 180)
            y = random.randint(40, 180)
            draw.rectangle([x, y, x + 15, y + 10], fill=random.choice([(210, 220, 80), (35, 90, 30)]))
    elif "bacterial" in class_name.lower():
        draw_leaf_base(draw, width, height, (55, 115, 50))
        # Small black spots with yellowish halos
        for _ in range(25):
            x = random.randint(50, 170)
            y = random.randint(40, 180)
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(210, 200, 70))
            draw.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(30, 20, 15))
    elif "early_blight" in class_name.lower():
        draw_leaf_base(draw, width, height, (60, 110, 45))
        # Concentric dark rings
        for _ in range(5):
            cx = random.randint(60, 160)
            cy = random.randint(50, 170)
            for rad in [18, 14, 10, 6, 2]:
                col = (60, 35, 20) if rad % 8 == 0 else (120, 80, 40)
                draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=col, width=2)
    elif "late_blight" in class_name.lower():
        draw_leaf_base(draw, width, height, (50, 95, 45))
        # Large irregular water-soaked dark lesions
        for _ in range(6):
            cx = random.randint(60, 160)
            cy = random.randint(50, 170)
            draw.ellipse([cx - 25, cy - 20, cx + 25, cy + 20], fill=(50, 40, 30))
            draw.ellipse([cx - 20, cy - 15, cx + 20, cy + 15], fill=(35, 25, 20))
    elif "mold" in class_name.lower():
        draw_leaf_base(draw, width, height, (75, 120, 55))
        # Velvety olive/brown patches
        for _ in range(15):
            cx = random.randint(55, 165)
            cy = random.randint(45, 175)
            draw.ellipse([cx - 12, cy - 10, cx + 12, cy + 10], fill=(130, 110, 50))
    elif "septoria" in class_name.lower():
        draw_leaf_base(draw, width, height, (55, 115, 50))
        # Gray spots with dark border
        for _ in range(30):
            cx = random.randint(50, 170)
            cy = random.randint(40, 180)
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(40, 25, 20), fill=(200, 200, 195))
    elif "spider" in class_name.lower():
        draw_leaf_base(draw, width, height, (80, 115, 60))
        # Fine stippling dots & webbing effect
        for _ in range(120):
            cx = random.randint(45, 175)
            cy = random.randint(35, 185)
            draw.point((cx, cy), fill=(240, 235, 180))
    elif "target" in class_name.lower():
        draw_leaf_base(draw, width, height, (60, 115, 50))
        for _ in range(8):
            cx = random.randint(55, 165)
            cy = random.randint(45, 175)
            draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(190, 170, 90))
            draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=(70, 45, 25), fill=(95, 65, 35))
    else:
        draw_leaf_base(draw, width, height, (50, 120, 50))

    # Apply slight smoothing filter
    img = img.filter(ImageFilter.SMOOTH_MORE)
    return img


def create_sample_dataset(samples_per_train_class: int = 15, samples_per_val_class: int = 5, samples_per_test_class: int = 4):
    """Generates synthetic dataset structure for all 10 classes."""
    splits = {
        "train": samples_per_train_class,
        "validation": samples_per_val_class,
        "test": samples_per_test_class,
    }

    print("Generating starter sample leaf images across all 10 classes...")
    total_created = 0

    for split_name, count in splits.items():
        split_dir = os.path.join(DATASET_ROOT, split_name)
        for cls in CLASSES:
            cls_dir = os.path.join(split_dir, cls)
            os.makedirs(cls_dir, exist_ok=True)
            for i in range(1, count + 1):
                img = generate_sample_leaf(cls)
                filename = f"{cls.lower()}_{split_name}_{i:03d}.jpg"
                filepath = os.path.join(cls_dir, filename)
                img.save(filepath, "JPEG", quality=90)
                total_created += 1

    print(f"[SUCCESS] Created {total_created} sample images across train, validation, and test splits!")
    print(f"Dataset root: {os.path.abspath(DATASET_ROOT)}")


if __name__ == "__main__":
    create_sample_dataset()
