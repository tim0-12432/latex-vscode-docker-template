import subprocess
import time
import os


# Get the path to the script and the PDF file
script_path = os.path.dirname(os.path.realpath(__file__))
temp_file_path = os.path.join(script_path, 'start.temp')

# write compile tool information to a file
result = subprocess.run([os.path.join(script_path, 'run_docker.bat'), 'pdflatex', '--version'], stdout=subprocess.PIPE).stdout.decode('utf-8')
with open(os.path.join(script_path, '..', 'src', 'info.tex'), 'w') as f:
    sys_info = result.splitlines()[0]
    f.write(f'\\newcommand{{\\compileTools}}{{{sys_info} Docker}}\n')

# Get the current time
start_time = time.time()

# Write the start time to a temporary file
with open(temp_file_path, 'w') as temp_file:
    temp_file.write(str(start_time))
