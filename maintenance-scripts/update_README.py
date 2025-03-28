import json
import os
import re

# Load JSON data
with open('me.json', 'r') as json_file:
    data = json.load(json_file)

# Extract physical properties
age = data.get('age', 'N/A')
height = data.get('height', 'N/A')
weight = data.get('weight', 'N/A')
name = data.get('first_name', '') + " " + data.get('middle_name', '') + " " + data.get('last_name', '')

# Generate the "Physical Properties" section
physical_properties_section = f"""
### Physical Properties
- **Name:** {name.strip()}
- **Age:** {age}
- **Height:** {height}
- **Weight:** {weight}
"""

# Generate the "Avatars" section
profile_icons_folder = "profile-icons"
avatars_section = "## Avatars\n\n<table>\n  <tr>\n"

if os.path.exists(profile_icons_folder):
    for filename in os.listdir(profile_icons_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            image_path = os.path.join(profile_icons_folder, filename).replace("\\", "/")
            alt_text = os.path.splitext(filename)[0].replace("-", " ").title()
            avatars_section += f"""    <td align="center">
      <img src="{image_path}" alt="{alt_text}" width="150" height="150"><br>
      <b>{alt_text}</b>
    </td>\n"""
    avatars_section += "  </tr>\n</table>\n"
else:
    avatars_section += "No avatars available.\n"

# Update README.md
readme_path = 'README.md'
if os.path.exists(readme_path):
    with open(readme_path, 'r') as readme_file:
        readme_content = readme_file.read()

    # Replace the "Physical Properties" section
    readme_content = re.sub(
        r"### Physical Properties.*?## Avatars",
        physical_properties_section.strip() + "\n\n## Avatars",
        readme_content,
        flags=re.DOTALL,
    )

    # Replace or add the "Avatars" section
    if "## Avatars" in readme_content:
        readme_content = re.sub(
            r"## Avatars.*",
            avatars_section.strip(),
            readme_content,
            flags=re.DOTALL,
        )
    else:
        readme_content += "\n\n" + avatars_section

    with open(readme_path, 'w') as readme_file:
        readme_file.write(readme_content)

    print("README.md updated successfully!")
else:
    print(f"Error: {readme_path} not found.")