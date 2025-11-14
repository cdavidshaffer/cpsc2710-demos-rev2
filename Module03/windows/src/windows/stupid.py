from pathlib import Path

print(f"__file__: {__file__}")
parent = Path(__file__).parent
print(f"parent: {parent}")

icons_dir = parent / "icons"
print(f"icons_dir: {icons_dir}")
print(f"type(icons_dir): {type(icons_dir)}")
