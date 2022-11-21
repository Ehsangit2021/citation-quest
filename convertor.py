import os
import re
import shutil
from builtins import enumerate
import tika
from tika import parser
from collections import Counter
import streamlit as st
import numpy as np
tika.initVM()

# def clear_session():
#     set_keys_1 = [key[0] for key in st.session_state.items() if 'type_' in key[0]]
#     for k in set_keys_1:
#         del st.session_state[k]

def generate_vocab_dict(lines):
    vocab_dict = Counter()
    for line in lines:
        vocab_dict.update(line[0].split())
    return vocab_dict

@st.cache(suppress_st_warning=True)
def recites_extraction(file_name):
    # clear_session() # Clear all previous pdf variable from session
    diagram=[]
    # pars pdf file
    raw = parser.from_file(file_name)
    # te = parser.parse1(urlOrPath=file_name, option=, services={'text':'all'})

    _pages = raw['content'].split('\n\n\n\n')
    # raw['content']
    # raw['metadata']
    pages = []
    for page in filter(None, _pages):
        page: str
        page = page.strip()
        if page:
            pages.append(page)
    
    
    # _lines = raw['content'].splitlines()
    # _lines = raw['content'].split('\n\n\n\n')
    ietr = 1
    lines = []
    lines_page = []
    for _lines in pages:
        _lines = _lines.splitlines()
        for line in filter(None, _lines):
            line: str
            line = line.strip()
            if line:
                lines.append((line,ietr))
                lines_page.append(ietr)
        ietr +=1
    
    # generate regexs
    regex = [
        r'[A-Z]{1}[a-z\u0000-\u007F]+ \([0-9]{4}\)|\([A-Z]{1}[a-z\u0000-\u007F]+, [0-9]{4}\)|\([A-Z]{1}[a-z\u0000-\u007F]+, [0-9]{4}; [A-Za-z ' \
        r'\u0000-\u007F,;]*\)|[A-Z]{1}[a-z\u0000-\u007F]+ \([0-9]{4},[A-Za-z0-9\u0000-\u007F ]*\)|[A-Z]{1}[a-z\u0000-\u007F ]+ [a-z]{2} [a-z]{2}. '
        r'\([0-9]{4}\)',
        # r'\(([^)]+)?(?:19|20)\d{2}?([^)]+)?\)'
    ]
    
    result = {}

    for index, pattern in enumerate(regex):
        if result.get(index, None) is None:
            result[index] = []
        for line_index, line in enumerate(lines[1:], start=1):
            if not line:
                continue
            match = re.search(pattern, line[0])
            if match:
                # result[index].append([match.group(), lines[line_index - 1], lines[line_index], lines[line_index + 1]])
                if line_index < 4:
                    result[index].append([match.group(),  ' '.join([lines[line_index+ii][0] for ii in range(-1,2)]), lines[line_index][1]])
                else:
                    result[index].append([match.group(), ' '.join([lines[line_index+ii][0] for ii in range(-2,3)]), lines[line_index][1]])
                    

    result_path = '.'.join(file_name.split('.')[:-1]) + "_csv"
    if os.path.isdir(result_path):
        shutil.rmtree(result_path)
    os.makedirs(result_path)
    json_result = {}
    for key, values in result.items():
        with open(os.path.join(result_path, f"result{key}.csv"), "w", encoding='utf-8') as f:
            for idx_line, each_match in enumerate(values):
                json_result[idx_line] = [each_match[0], each_match[1], each_match[2]]
                # json_key[idx_line] = each_match[0]
                for line in each_match:
                    try:
                        f.write(line.replace(',', '-') + ',')
                    except Exception as e:
                        print(e)
                f.write('\n')
    vocab_dict = generate_vocab_dict(lines)
    count = sum(vocab_dict.values())
    return json_result,vocab_dict,count,diagram


if __name__ == '__main__':
    list_of_pdf = os.scandir('.')
    for file in list_of_pdf:
        file_name = file.name.split('.')
        if len(file_name) > 1 and file_name[-1] == 'pdf':
            extract_pdf(file.name)
