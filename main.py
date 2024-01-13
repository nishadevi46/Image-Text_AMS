import os
import easyocr
import re

# Specify the folder path containing the images
folder_path = 'images/'

# Specify the file path where you want to store the filtered results
output_file_path = 'filtered_output.txt'

reader = easyocr.Reader(['en'])

# Create a set to store unique numerical results
numeric_results = set()

# Specify the words to ignore
ignore_words = {'unknown', 'unknc', 'Da', 'o.s'}

# Function to extract first 8 digits from a string
def extract_first_8_digits(text):
    match = re.search(r'\b\d{8}\b', text)
    return match.group(0) if match else None

# Check if the output file already exists
file_exists = os.path.exists(output_file_path)

# Open the file in append mode if it exists, otherwise create a new file
with open(output_file_path, 'a' if file_exists else 'w', encoding='utf-8') as output_file:
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            # Construct the full path to the image
            image_path = os.path.join(folder_path, filename)

            # Process the image using easyOCR
            result = reader.readtext(image_path)

            # Filter and add numeric results to the set
            for (bbox, text, prob) in result:
                # Extract the first 8 digits and check if it's a numeric value
                extracted_digits = extract_first_8_digits(text)
                if extracted_digits and extracted_digits not in ignore_words:
                    numeric_results.add(extracted_digits)

    # Write the filtered numeric results to the file
    for numeric_text in numeric_results:
        output_file.write(f'{numeric_text}\n')

print(f'Filtered first 8 digits results for all images written to {output_file_path}')
