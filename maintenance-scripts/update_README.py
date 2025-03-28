import json
import os

# Load JSON data
with open('me.json', 'r') as json_file:
    data = json.load(json_file)

# Extract physical properties
age = data.get('age', 'N/A')
height = data.get('height', 'N/A')
weight = data.get('weight', 'N/A')
name = data.get('first_name', '') + " " + data.get('middle_name', '') + " " + data.get('last_name', '')

# Generate the "Physical Properties" section
readme_content = f"""
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
      <img src="{image_path}" alt="{alt_text}" width="150" height="150"><br>idth="150" height="150"><br>
      <b>{alt_text}</b>      <b>{alt_text}</b>
    </td>\n"""
    avatars_section += "  </tr>\n</table>\n"
else:
    avatars_section += "No avatars available.\n"

# Combine sections
readme_content += "\n" + avatars_section
readme_content += "\n" + avatars_section






with open('README.md', 'w') as readme_file:  # Update README.md
    readme_file.write(readme_content)

print("README.md updated successfully!")
with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)

print("README.md updated successfully!")