import re
import os


script_path = os.path.dirname(os.path.realpath(__file__))
latex_file_path = os.path.join(script_path, '..', 'src', 'content')
main_tex_files = ['src/thesis.tex', 'src/cover.tex', 'src/acronyms.tex', 'src/glossary.tex']
acronym_file = 'src/acronyms.tex'
glossary_file = 'src/glossary.tex'
libs_file = 'src/libraries.tex'
cites_file = 'src/refs.bib'

def get_all_latex():
    all_latex = []
    for file in main_tex_files:
        with open(os.path.join(script_path, '..', file), 'r') as f:
            all_latex.append(f.read())
    for root, dirs, files in os.walk(latex_file_path):
        for file in files:
            if file.endswith('.tex'):
                with open(os.path.join(root, file), 'r') as f:
                    all_latex.append(f.read())
    return '\n'.join(all_latex)

def get_all_labels(text):
    all_figures = []
    all_tables = []
    all_listings = []
    figures = re.findall(r'\\label{fig:(.*?)}', text)
    tables = re.findall(r'\\label{tab:(.*?)}', text)
    listings = re.findall(r'label={code:(.*?)}', text)
    all_figures.extend(figures)
    all_tables.extend(tables)
    all_listings.extend(listings)
    return all_figures, all_tables, all_listings

def get_all_acronyms():
    with open(os.path.join(script_path, '..', acronym_file), 'r') as f:
        acr_text = f.read()
    acronyms = []
    acronyms.extend(re.findall(r'\\newacronym{(.+)}{.*}{.*}', acr_text))
    return acronyms

def get_all_glossary():
    with open(os.path.join(script_path, '..', glossary_file), 'r') as f:
        gloss_text = f.read()
    glossary = []
    glossary.extend(re.findall(r'\\newglossaryentry{(.+)}', gloss_text))
    return glossary

def get_all_libs():
    with open(os.path.join(script_path, '..', libs_file), 'r') as f:
        libs_text = f.read()
    libraries = []
    libraries.extend(re.findall(r'\\newglossaryentry{(.+)}', libs_text))
    return libraries

def get_all_refs():
    with open(os.path.join(script_path, '..', cites_file), 'r') as f:
        cites_text = f.read()
    cites = []
    cites.extend(re.findall(r'@[a-zA-Z]+{(.+),', cites_text))
    return cites

def check_if_ref(tag, text):
    return re.search(r'\\ref{' + tag + '}', text) != None

def check_if_acronym(tag, text):
    return re.search(r'\\acr(.*?){' + tag + '}', text) != None

def check_if_glossary(tag, text):
    return re.search(r'\\glsy(Pl)?{' + tag + '}', text) != None

def check_if_libs(tag, text):
    return re.search(r'\\lib{' + tag + '}', text) != None

def check_if_cited(tag, text):
    return re.search(r'\\cite(\[.*\])?{' + tag + '}', text) != None

if __name__ == '__main__':
    latex_content = get_all_latex()
    figures, tables, listings = get_all_labels(latex_content)
    
    not_used_figures = []
    for figure in figures:
        tag_name = f'fig:{figure}'
        if not check_if_ref(tag_name, latex_content):
            not_used_figures.append(tag_name)

    not_used_tables = []
    for table in tables:
        tag_name = f'tab:{table}'
        if not check_if_ref(tag_name, latex_content):
            not_used_tables.append(tag_name)

    not_used_listings = []
    for listing in listings:
        tag_name = f'code:{listing}'
        if not check_if_ref(tag_name, latex_content):
            not_used_listings.append(tag_name)

    acronyms = get_all_acronyms()
    not_used_acronyms = []
    for acronym in acronyms:
        if not check_if_acronym(acronym, latex_content):
            not_used_acronyms.append(acronym)

    glossary = get_all_glossary()
    not_used_glossary = []
    for gloss in glossary:
        if not check_if_glossary(gloss, latex_content):
            not_used_glossary.append(gloss)

    libraries = get_all_libs()
    not_used_libs = []
    for lib in libraries:
        if not check_if_libs(lib, latex_content):
            not_used_libs.append(lib)

    refs = get_all_refs()
    not_used_refs = []
    for ref in refs:
        if not check_if_cited(ref, latex_content):
            not_used_refs.append(ref)

    if not_used_figures:
        print('The following figures are not used in the latex files:')
        for figure in not_used_figures:
            print(' - ' + figure)
    else:
        print('All figures are used in the latex files.')

    print()

    if not_used_tables:
        print('The following tables are not used in the latex files:')
        for table in not_used_tables:
            print(' - ' + table)
    else:
        print('All tables are used in the latex files.')

    print()

    if not_used_listings:
        print('The following listings are not used in the latex files:')
        for listing in not_used_listings:
            print(' - ' + listing)
    else:
        print('All listings are used in the latex files.')

    print()

    if not_used_acronyms:
        print('The following acronyms are not used in the latex files:')
        for acronym in not_used_acronyms:
            print(' - ' + acronym)
    else:
        print('All acronyms are used in the latex files.')

    print()

    if not_used_glossary:
        print('The following glossary entries are not used in the latex files:')
        for gloss in not_used_glossary:
            print(' - ' + gloss)
    else:
        print('All glossary entries are used in the latex files.')

    print()

    if not_used_libs:
        print('The following libraries are not used in the latex files:')
        for lib in not_used_libs:
            print(' - ' + lib)
    else:
        print('All libraries are used in the latex files.')

    print()

    if not_used_refs:
        print('The following refs are not cited in the latex files:')
        for ref in not_used_refs:
            print(' - ' + ref)
    else:
        print('All refs are cited in the latex files.')
