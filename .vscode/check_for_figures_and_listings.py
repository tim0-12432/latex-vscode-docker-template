import re
import os


script_path = os.path.dirname(os.path.realpath(__file__))
latex_file_path = os.path.join(script_path, '..', 'src', 'content')
figures_file_path = os.path.join(script_path, '..', 'src', 'figures')
listings_file_path = os.path.join(script_path, '..', 'src', 'listings')
main_tex_files = ['src/thesis.tex', 'src/cover.tex', 'src/acronyms.tex', 'src/glossary.tex']

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

def get_all_figures():
    all_figures = []
    for root, dirs, files in os.walk(figures_file_path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
                dir = root.split('..\\')[-1]
                dir = dir.replace('\\', '/')
                all_figures.append(dir + '/' + file)
    return all_figures

def get_all_listings():
    all_figures = []
    for root, dirs, files in os.walk(listings_file_path):
        for file in files:
            dir = root.split('..\\')[-1]
            dir = dir.replace('\\', '/')
            all_figures.append(dir + '/' + file)
    return all_figures

if __name__ == '__main__':
    latex_content = get_all_latex()
    figures = get_all_figures()
    listings = get_all_listings()
    
    not_used_figures = []
    for figure in figures:
        if not figure in latex_content:
            not_used_figures.append(figure)

    not_used_listings = []
    for listing in listings:
        if not listing in latex_content:
            not_used_listings.append(listing)

    if not_used_figures:
        print('The following figures are not used in the latex files:')
        for figure in not_used_figures:
            print(' - ' + figure)
    else:
        print('All figures are used in the latex files.')

    print()

    if not_used_listings:
        print('The following listings are not used in the latex files:')
        for listing in not_used_listings:
            print(' - ' + listing)
    else:
        print('All listings are used in the latex files.')
