import data_processor as dp
import file_processor as fp
import gl
import graphics as gp
import stats as st


# Variables ------------------------

MODE = 'SN'     # SN/TL
BOOK = 'AS'     # AH/AS/CS
CHAPTER = 1     # 1/2/3/4/5/6
BLOCKSIZE = 40


# settings ------------------------


TEXTS = {'SN':'sanskrit','TL':'transliterated'}
filename = fp.get_filename(MODE,BOOK,CHAPTER)
inputfile = fp.File_Processor(filename)
content = inputfile.read()
text_obj = dp.Text(TEXTS[MODE],content)
no_digits = text_obj.remove_digit()
no_symbols = text_obj.remove_symbol(no_digits)
no_headings = text_obj.remove_headings(no_symbols)
sentence_only = text_obj.get_sentence(no_headings)
full_stop_remove = text_obj.remove_full_stop(sentence_only)
blocks = inputfile.split(full_stop_remove, BLOCKSIZE, True, True)

# Analysis ------------------------

this_data = []
header = ['Mode','Book','Chapter','Block']

for i in range(len(blocks)):
    for j in range(len(blocks)):
        a = st.chi_square(blocks[i], blocks[j])


