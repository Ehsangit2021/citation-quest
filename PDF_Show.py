import streamlit as st
import base64
from convertor import recites_extraction
# import streamlit.components.v1 as components
# import pandas as pd
# import numpy as np
# from streamlit.components.v1 import html



st.set_page_config(layout="wide")


if 'page_num' not in st.session_state:
    st.session_state.page_num = 1


vocab_dict = None
diagrammmm = None
json_result = None

st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" \
            integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">', unsafe_allow_html=True)

type_list = ('select','Adjectivizing','General references','Non-citation','Pronoun replacement', \
             'Unconventional citation','Fragmentary citation','Naming','Verb-controlling',\
             '--------','Background citation','Support for objectives','Suppoert for topic',\
             'Support for findings','Support for a claim or an argument', \
             'Support for materials, procedures, and instruments','Endophoric citation', \
             'Further reference','Blended Sources', \
             'Applied recommendations','Research recommendations','Evaluation','Comparisons', \
             'Establishing link (sources with similar findings)','Establishing link (sources \
              with similar arguments)','Establishing link (sources with similar foci)', \
             'Extracts from other sources','Source (attribution)','Source (origin)','Explanation')

def clear_session():
    set_keys_1 = [key[0] for key in st.session_state.items() if 'type_' in key[0]]
    set_keys_2 = [key[0] for key in st.session_state.items() if 'sb' in key[0]]
    for k in set_keys_1:
        print("deleted: ", st.session_state[k])
        del st.session_state[k]
    
    for k in set_keys_2:
        print("deleted: ", st.session_state[k])
        del st.session_state[k]

# @st.cache(suppress_st_warning=True)
def show_pdf(file_path, page_num = 1, type_list=type_list):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<div id="linkto_top"><embed src="data:application/pdf;base64,{base64_pdf}#page={page_num} \
                    &zoom=130" width="100%" height="1400" type="application/pdf"></div>'
    st.markdown(pdf_display, unsafe_allow_html=True)
#     go_to()

# def go_to():
#     import webbrowser
#     webbrowser.open('http://127.0.0.1:8501/#linkto_top')

st.title('This project is to identify all citation types autonomously from scientific papers.')

# html(my_html)

st.write('There are different known citation protocols, such as MLA, APA, Chicago, Harvard, Vancover!')
st.write('Currently, we support vancover citation finding in this project!')
pdf_file = st.file_uploader("Select your PDF file", type=["pdf"], on_change=clear_session)


if pdf_file is not None:
    save_image_path = './Uploaded_Resumes/'+pdf_file.name
    with open(save_image_path, "wb") as f:
        f.write(pdf_file.getbuffer())
    show_pdf(save_image_path, page_num=st.session_state.page_num)

    # process the PDF
    json_result, vocab_dict, word_count, diagram = recites_extraction(save_image_path)


the_selected_item = []
def update_diagram(key=0):
    if st.session_state.get('sb'+str(key), None):
        print('*******************')
        print('st.session_state.key is:', st.session_state['sb'+str(key)])
        st.session_state['type_'+str(key)] = ('').join((st.session_state['sb'+str(key)]).replace(" ", "_"))

def change_page(page_num):
    st.session_state.page_num = page_num
    print('page number is: ', page_num)


if json_result:
    if vocab_dict is not None:
        st.header('Found citations:')
        for key, values in json_result.items():
            with st.expander(str(key+1) + ' : ' + values[0]):
                with st.container():
                    st.info(values[1])
                    st.button(f'go to page {int(values[2])+1}', key='btn'+str(key), on_click=change_page, args=(int(values[2])+1,))
                    st.write('----------------------------------')
                    st.selectbox('Please select the type!', type_list, key='sb'+str(key), on_change=update_diagram, args=(key,))

    diagram_str = {}
    set_keys = []       
    diagrammmm = {}
    set_keys = [key[0] for key in st.session_state.items() if 'type_' in key[0]]
    diagram_str = { k: st.session_state[k] for k in set_keys}

    from collections import Counter
    diagrammmm = Counter(diagram_str.values())

else:
    st.write('Still no found citation!!!')

if not "initialized" in st.session_state:
    st.session_state.initialized = True

# https://medium.com/@max.lutz./how-to-build-a-data-visualization-page-with-streamlit-4ca4999eba64
if diagrammmm:
    import matplotlib
    import matplotlib.pyplot as plt
    # import seaborn as sns
    # import os
    from matplotlib.backends.backend_agg import RendererAgg

    matplotlib.use("agg")
    _lock = RendererAgg.lock

    st.header("Frequency diagram for citation types!")

    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.2, 1, .2, 1, .2))

    with row0_1, _lock:
        fig, ax = plt.subplots(figsize=(5, 5))
        k=[]
        v=[]
        for key in diagrammmm:
            k.append(key)
            v.append(diagrammmm[key])
        
        ax.pie(v, labels=k, wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white'})
        p = plt.gcf()
        p.gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
        st.pyplot(fig)

    st.write(diagrammmm)
