import json
import os
from datetime import datetime

# Function to calculate age
def calculate_age(birthdate_str):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

# Function to determine age range for kids
def get_age_range(age):
    if age < 2:
        return "Baby"
    elif 2 <= age <= 4:
        return "Preschool"
    elif 5 <= age <= 10:
        return "Elementary School"
    elif 11 <= age <= 13:
        return "Middle School"
    elif 14 <= age <= 18:
        return "High School"
    else:
        return "Adult" + "(" + str(age) + ")"

# Load the me.json file
json_file_path = "me.json"
try:
    with open(json_file_path, "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: {json_file_path} not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: {json_file_path} contains invalid JSON.")
    exit(1)

if not isinstance(data.get("kids", []), list):
    print("Error: 'kids' should be a list in the JSON file.")
    exit(1)

# Update your age if today is your birthday
my_birthdate = os.getenv("MY_BIRTHDATE")
if my_birthdate:
    my_birthdate_dt = datetime.strptime(my_birthdate, "%Y-%m-%d")
    today = datetime.today()
    if today.month == my_birthdate_dt.month and today.day == my_birthdate_dt.day:
        data["age"] = calculate_age(my_birthdate)
        print(f"Happy Birthday! Your age has been updated to {data['age']}.")

# Update kids' ages with descriptive strings
kids_birthdates = {
    "Gwen": os.getenv("GWEN_BIRTHDATE"),
    "Freddy": os.getenv("FREDDY_BIRTHDATE"),
    "Audrey": os.getenv("AUDREY_BIRTHDATE"),
}

for kid in data.get("kids", []):
    birthdate = kids_birthdates.get(kid["name"])
    if birthdate:
        age = calculate_age(birthdate)
        age_range = get_age_range(age)
        print(f"Updating {kid['name']}'s age to '{age_range}'.")
        kid["age"] = age_range

# Update pets' ages
pets_birthdates = {
    "Bruno": os.getenv("BRUNO_BIRTHDATE"),
    "Scout": os.getenv("SCOUT_BIRTHDATE"),
}

for pet_type in data.get("pets", {}).values():
    for pet in pet_type:
        birthdate = pets_birthdates.get(pet["name"])
        if birthdate:
            age = calculate_age(birthdate)
            print(f"Updating {pet['name']}'s age to {age}.")
            pet["age"] = age

# Save the updated JSON file
with open(json_file_path, "w") as file:
    json.dump(data, file, indent=4)

print("Ages updated successfully!")