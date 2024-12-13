import csv

products = [
    {
        "id": 1,
        "name": "Accuracy",
        "type": "Power",
        "desc": "Shivs deal 4 more damage",
        "energy": 1,
        "classtype": "The Silent" 
    },
    {
        "id": 2,
        "name": "Blade Dance",
        "type": "Skill",
        "desc": "Add 3 Shivs into your hand",
        "energy": 1,
        "classtype": "The Silent" 
    },
    {
        "id": 3,
        "name": "Catalyst",
        "type": "Skill",
        "desc": "Double the enemyäs poison, exhaust",
        "energy": 1,
        "classtype": "The Silent" 
    },
    {
        "id": 4,
        "name": "Corpse Explosion",
        "type": "Skill",
        "desc": "Apply 6 poison. When the enemy dies, deal damage equal to it's max HP to ALL enemies.",
        "energy": 2,
        "classtype": "The Silent" 
    },
    {
        "id": 5,
        "name": "After Image",
        "type": "Power",
        "desc": "Whenever you play a card, gain 1 Block",
        "energy": 1,
        "classtype": "The Silent" 
    },
    {
        "id": 6,
        "name": "Carnage",
        "type": "Attack",
        "desc": "Deal 20 damage, Exhaust",
        "energy": 2,
        "classtype": "The Ironclad" 
    },
    {
        "id": 7,
        "name": "Bash",
        "type": "Attack",
        "desc": "Deal 8 damage, apply 2 Vulnerability",
        "energy": 2,
        "classtype": "The Ironclad" 
    },
    {
        "id": 8,
        "name": "Limit Break",
        "type": "Skill",
        "desc": "Double your strength, Exhaust",
        "energy": 1,
        "classtype": "The Ironclad" 
    },
    {
        "id": 9,
        "name": "Corruption",
        "type": "Power",
        "desc": "Skills cost 0. Whenever you play a skill, Exhaust it",
        "energy": 1,
        "classtype": "The Ironclad" 
    },
    {
        "id": 10,
        "name": "Spot Weakness",
        "type": "Skill",
        "desc": "If the enemy intends to attack, gain 2 Strength",
        "energy": 1,
        "classtype": "The Ironclad" 
    },
    {
        "id": 11,
        "name": "Glacier",
        "type": "Skill",
        "desc": "Gain 7 block, Channel 2 Frost.",
        "energy": 2,
        "classtype": "The Defect" 
    },
    {
        "id": 12,
        "name": "Coolheaded",
        "type": "Skill",
        "desc": "Channel 1 Frost. Draw 1 card",
        "energy": 1,
        "classtype": "The Defect" 
    },
    {
        "id": 13,
        "name": "Echo Form",
        "type": "Power",
        "desc": "The first card you play at the start of your turn is played twice",
        "energy": 3,
        "classtype": "The Defect" 
    },
    {
        "id": 14,
        "name": "Biased Cognition",
        "type": "Power",
        "desc": "Gain 4 Focus. At the start of your turn, lose 1 Focus",
        "energy": 1,
        "classtype": "The Defect" 
    },
    {
        "id": 15,
        "name": "Equilibrium",
        "type": "Skill",
        "desc": "Gain 13 Block, retain your hand this turn",
        "energy": 2,
        "classtype": "The Defect" 
    },
     {
        "id": 16,
        "name": "Worship",
        "type": "Skill",
        "desc": "Gain 5 Mantra",
        "energy": 2,
        "classtype": "The Watcher" 
    },
      {
        "id": 17,
        "name": "Devotion",
        "type": "Power",
        "desc": "At the start of your turn, Gain 2 Mantra",
        "energy": 1,
        "classtype": "The Watcher" 
    },
       {
        "id": 18,
        "name": "Blasphemy",
        "type": "Skill",
        "desc": "Enter Divinity, Die next turn",
        "energy": 1,
        "classtype": "The Watcher" 
    },
        {
        "id": 19,
        "name": "Deva Form",
        "type": "Power",
        "desc": "Ethereal. At the start of your turn, gain Energy and increase this gain by 1",
        "energy": 2,
        "classtype": "The Watcher" 
    },
         {
        "id": 20,
        "name": "Talk to the Hand",
        "type": "Attack",
        "desc": "Deal 5 damage. Whenever you attack this enemy, gain 2 Block",
        "energy": 2,
        "classtype": "The Watcher" 
    },
    ]     


# Define the CSV file path
csv_file_path = "cards.csv"

# Write the products data to a CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "type", "energy", "classtype"])
    writer.writeheader()  # Write the header row
    writer.writerows(products)  # Write the product data

print(f"Data successfully saved to {csv_file_path}")