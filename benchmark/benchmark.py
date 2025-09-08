import dotenv
import os
import shutil
from os import path
import time
import docker

dotenv.load_dotenv()

workdir = os.getenv("WORKDIR")
if workdir:
    print(f"Working directory is set to: {workdir}")
else:
    print("Working directory is not set.")
    exit(1)

modes = ['ORIGINAL', 'MAKEGLOSSARIES', 'DRAFTING', 'NOCONSOLE', 'PREAMBLE', 'COMBINED']
mode = os.getenv("MODE")
if mode not in modes:
    print(f"Invalid mode: {mode}.\nPlease use one of the following modes: {', '.join(modes)}")
    exit(1)
print(f"Mode is set to: {mode}")

template_dir = path.abspath(path.join(path.dirname(path.realpath(__file__)), '..', 'src'))

def wait_for_docker(max_retries=30, delay=1):
    for _ in range(max_retries):
        try:
            client = docker.from_env()
            client.ping()
            print("Docker daemon is ready.")
            return True
        except Exception as e:
            print(f"Docker not ready yet: {e}. Retrying...")
            time.sleep(delay)
    print("Docker daemon did not start in time.")
    exit(1)

def getDockerRunCommand(args):
    return f"docker run --rm -v \"{workdir}:/workdir\" -w /workdir texlive/texlive:latest {args}"

allowed_exts = ('.tex', '.py', '.jpg', '.bib')

def ignore_func(dir_path, names):
    ignored = []
    for name in names:
        full = os.path.join(dir_path, name)
        if os.path.isdir(full):
            continue
        if not name.endswith(allowed_exts):
            ignored.append(name)
    return ignored

def copyTemplate():
    shutil.copytree(template_dir, workdir, dirs_exist_ok=True, ignore=ignore_func)

def resetGlossaries():
    main_file = path.join(workdir, 'thesis.tex')
    with open(main_file, 'r') as f:
        content = f.read()
    content = content.replace(r'\makeglossaries', r'\makenoidxglossaries')
    content = content.replace(r'\printglossary', r'\printnoidxglossary')
    with open(main_file, 'w') as f:
        f.write(content)

def resetPreamble():
    main_file = path.join(workdir, 'thesis.tex')
    with open(main_file, 'r') as f:
        content = f.read()
    content = content.replace(r'\csname endofdump\endcsname % END OF PREAMBLE', '')
    with open(main_file, 'w') as f:
        f.write(content)

def generateDummyFiles():
    copyTemplate()
    if mode == 'COMBINED':
        pass
    if mode != 'MAKEGLOSSARIES':
        resetGlossaries()
    if mode != 'PREAMBLE':
        resetPreamble()

def checkTexLiveContainer():
    os.system(f'docker load -i /app/benchmark/texlive.tar')

def runCompilation():
    standard_pdflatex_run = 'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error thesis.tex'
    switcher = {
        'ORIGINAL': [
            standard_pdflatex_run,
            'bibtex thesis',
            standard_pdflatex_run,
            standard_pdflatex_run
        ],
        'MAKEGLOSSARIES': [
            standard_pdflatex_run,
            'bibtex thesis',
            'makeglossaries thesis',
            standard_pdflatex_run,
            standard_pdflatex_run
        ],
        'DRAFTING': [
            'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -draftmode thesis.tex',
            'bibtex thesis',
            'pdflatex -synctex=1 -interaction=nonstopmode -file-line-error -draftmode thesis.tex',
            standard_pdflatex_run
        ],
        'NOCONSOLE': [
            'pdflatex -synctex=1 -interaction=batchmode -file-line-error thesis.tex',
            'bibtex thesis',
            'pdflatex -synctex=1 -interaction=batchmode -file-line-error thesis.tex',
            'pdflatex -synctex=1 -interaction=batchmode -file-line-error thesis.tex'
        ],
        'PREAMBLE': [
            'pdflatex -ini -jobname=thesis "&pdflatex" mylatexformat.ltx thesis.tex',
            'pdflatex "&thesis" thesis.tex',
            'bibtex thesis',
            'pdflatex "&thesis" thesis.tex',
            'pdflatex "&thesis" thesis.tex'
        ],
        'COMBINED': [
            'pdflatex -ini -jobname=thesis "&pdflatex" mylatexformat.ltx thesis.tex',
            'pdflatex -interaction=batchmode -draftmode "&thesis" thesis.tex',
            'bibtex thesis',
            'makeglossaries thesis',
            'pdflatex -interaction=batchmode -draftmode "&thesis" thesis.tex',
            'pdflatex -interaction=batchmode "&thesis" thesis.tex'
        ],
    }
    commands = switcher.get(mode, [])
    os.chdir(workdir)
    for command in commands:
        os.system(getDockerRunCommand(command))

def check_run_successful():
    return path.exists(path.join(workdir, 'thesis.pdf'))

if __name__ == "__main__":
    wait_for_docker()

    # generate content
    generateDummyFiles()

    checkTexLiveContainer()

    start = time.time()

    # execute the processing
    runCompilation()

    end = time.time()

    if check_run_successful():
        print(f"Compilation took {end - start:.3f} seconds.")
    else:
        print("Compilation failed.")
