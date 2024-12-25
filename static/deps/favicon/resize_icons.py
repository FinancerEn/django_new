from PIL import Image

# Путь к исходному изображению
input_image_path = "logotip.png"

# Список размеров
sizes = [
    (32, 32),
    (16, 16),
    (512, 512),
    (192, 192),
]

# Создание иконок
for size in sizes:
    img = Image.open(input_image_path)
    img_resized = img.resize(size, Image.Resampling.LANCZOS)  # Изменено на LANCZOS
    output_path = f"favicon-{size[0]}x{size[1]}.png"
    img_resized.save(output_path)
    print(f"Сохранено: {output_path}")
