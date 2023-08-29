import json
import toml

def generate_item_config(item: str, effect: str, amplifier: int = 0, duration: float = 5.0) -> str:
    if amplifier < 0 or amplifier > 255:
        raise ValueError("amplifier must be between 0 and 255")

    if duration < 0 or duration > 1000000:
        raise ValueError("duration must be between 0 and 1000000")

    config = {
        "effects": [
            {
                "duration": duration,
                "item": item,
                "amplifier": amplifier,
                "effect": effect
            }
        ]
    }

    return toml.dumps(config)

def generate_item_config_group(item_tag: str, effect: str, amplifier: int = 0, duration: float = 5.0) -> list[str]:
    with open(f"./input/{item_tag}.json", "r") as json_file:
        data = json.load(json_file)

    values: str = data["values"]

    configs: list[str] = []

    for value in values:
        if value.startswith("#"):
            continue

        configs.append(generate_item_config(value, effect, amplifier, duration))

    return configs

def generate_config_file(item_tags: list[list], eat_cookies_berries_fast: bool = True):
    configs = [
        toml.dumps({
            'General': {
                'eat_cookies_berries_fast': eat_cookies_berries_fast
            }
        })+"\n"
    ]

    for item_tag in item_tags:
        configs += generate_item_config_group(*item_tag)

    with open("./output/foodeffects-common.toml", "w") as file:
        for config in configs:
            file.write(config)

if __name__ == "__main__":
    generate_config_file([
        ["alcohols", "drinkbeer:drunk", 0, 120]
    ])
