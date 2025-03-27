import json

# Load JSON data
with open('me.json', 'r') as json_file:
    data = json.load(json_file)

# Extract physical properties
age = data.get('age', 'N/A')
height = data.get('height', 'N/A')
weight = data.get('weight', 'N/A')
name = data.get('first_name', '') + " " + data.get('middle_name', '') + " " + data.get('last_name', '')

# Update README.md
readme_content = f"""
### Physical Properties
- **Name:** {name}
- **Age:** {age}
- **Height:** {height}
- **Weight:** {weight}
"""

with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)