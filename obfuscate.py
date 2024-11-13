import csv
import random
import string

def obfuscate_name(name):
    return ''.join(random.choice(string.ascii_letters) for _ in range(len(name)))

def obfuscate_topic(topic, obfuscation_map):
    parts = topic.split('/')
    obfuscated_parts = [obfuscation_map.get(part, part) for part in parts]
    return '/'.join(obfuscated_parts)

input_file = 'topics.csv'
output_file = 'topics2.csv'

# Read all unique names
unique_names = set()
with open(input_file, 'r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        for topic in row:
            parts = topic.split('/')
            unique_names.update(parts)

# Obfuscate names except "Enterprise"
obfuscation_map = {name: obfuscate_name(name) for name in unique_names if name != "Enterprise"}

# Read, obfuscate, and write the topics
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    for row in reader:
        obfuscated_row = [obfuscate_topic(topic, obfuscation_map) for topic in row]
        writer.writerow(obfuscated_row)