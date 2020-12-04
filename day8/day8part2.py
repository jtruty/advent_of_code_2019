from typing import Dict, List

PIXEL_WIDTH = 25
PIXEL_HEIGHT = 6

digit_str = ""
with open("input.txt") as f:
    for line in f:
        digit_str += line.strip()

layer_data: Dict[int, List[str]] = {}
idx = 0
layer = 1


while idx < len(digit_str):
    for i in range(PIXEL_HEIGHT):
        if layer not in layer_data:
            layer_data[layer] = []
        layer_data[layer].append(digit_str[idx : idx + PIXEL_WIDTH])
        idx += PIXEL_WIDTH
    layer += 1


layer_count = len(layer_data)
final_layer_data = ["" * PIXEL_WIDTH for i in range(PIXEL_HEIGHT)]

for height_idx in range(PIXEL_HEIGHT):
    for width_idx in range(PIXEL_WIDTH):
        for layer_idx in range(1, layer_count + 1):
            value = layer_data[layer_idx][height_idx][width_idx]
            if value != "2":
                existing_value = final_layer_data[height_idx]
                final_layer_data[height_idx] = (
                    existing_value[:width_idx] + value + existing_value[width_idx + 1 :]
                )
                break

for height in final_layer_data:
    print(height.replace("1", "#").replace("0", "."))
