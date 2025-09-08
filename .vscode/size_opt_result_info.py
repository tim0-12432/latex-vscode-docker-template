import time
import os


# Get current time
end_time = time.time()

# Get the path to the script and the PDF file
script_path = os.path.dirname(os.path.realpath(__file__))
old_path = os.path.join(script_path, '..', 'thesis.pdf')
new_path = os.path.join(script_path, '..', 'thesis_opt.pdf')

# Retrieve file sizes
try:
    old_size = os.path.getsize(old_path)
    new_size = os.path.getsize(new_path)
except FileNotFoundError:
    print('File not found!\n')
    old_size = 0
    new_size = 0

print(f'{old_size/1024/1024:.2f} MB -> {new_size/1024/1024:.2f} MB')

# Check and read temp time file
temp_file_path = os.path.join(script_path, 'start.temp')
if os.path.exists(temp_file_path):
    with open(temp_file_path, 'r') as temp_file:
        start_time = float(temp_file.read())

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print(f'\nNeeded time for optimization: {elapsed_time/60:.2f} minutes')

    # Remove the temporary file
    os.remove(temp_file_path)
