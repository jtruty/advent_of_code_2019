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
        layer_data[layer].append(digit_str[idx : idx + 25])
        idx += 25
    layer += 1

print(layer_data)

fewest_zeroes = None
fewest_layer = 0
for layer, data in layer_data.items():
    zero_count = sum([d.count("0") for d in data])
    if not fewest_zeroes or zero_count < fewest_zeroes:
        fewest_zeroes = zero_count
        fewest_layer = layer

print(f"Fewest layer: {fewest_layer}")

result = sum(d.count("1") for d in layer_data[fewest_layer]) * sum(
    d.count("2") for d in layer_data[fewest_layer]
)

print(f"Result: {result}")
