# citation-quest
This project leads to find academic citation in scientific paper. It also helps to label each cite and give you a graphical demonstration about frequency of citations type.


The below is an illustration of the webpage.

![page1](https://user-images.githubusercontent.com/84702784/203112710-0d254e7f-df76-4e5d-8b91-580011c9fa3c.png)

----------------------------------------------------------------------------------------------------------------
All citation with the type shown above will be axtracted after uploading pdf file.
On each you have access to page number, a whole sentence including the cite, and labeling option set.

![page2](https://user-images.githubusercontent.com/84702784/203112747-2526b231-2c3f-40bb-9984-cef19e294dc4.png)

----------------------------------------------------------------------------------------------------------------
And finally the reporting plot helps to have the report of citation-type labels.

![page3](https://user-images.githubusercontent.com/84702784/203112777-8c1df0ae-9e75-4ac5-be2d-ef3a9feb3bb0.png)

Try to have online evaluation: cite-quest.ir

----------------------------------------------------------------------------------------------------------------
PDF_Show.py is the main python file. The following command will let you strat the web page with streamlit package.

streamlit run PDF_Show.py

There are some switches for this command. You may find them there.
https://streamlit.io/

converter.py is the python script that performs regular expression in order to find the aforementioned citations. The reqular expression can be extended to cover other type of citations. If you are interested in, please let me know for contributions.

To find a real demonstration follow the following url.   cite-quest.ir
