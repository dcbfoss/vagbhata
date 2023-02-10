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
header = ['Mode','Book','Chapter','Block','Avg Word Len', 'Avg Sen Len (Word)', 'Avg Sen Len (Chr)', 'Richness', 'Shannon', 'Avg Compound Words']

for INDEX, block in enumerate(blocks):
    txt_obj = st.text_object(block)
    avg_word_len = txt_obj.average_word_len()
    avg_sen_len_w = txt_obj.average_sentence_word_len()
    avg_sen_len_c = txt_obj.average_sentence_chr_len()
    rich_ratio = txt_obj.get_richness_ratio()
    shannon = txt_obj.get_shannon()
    avg_compound_words = txt_obj.average_compound_words()
    this_data.append([MODE,BOOK,fp.get_chapter_name(CHAPTER,BOOK).split('_')[0],INDEX+1,avg_word_len,avg_sen_len_w,avg_sen_len_c,rich_ratio,shannon,avg_compound_words])

OUTPUT_FILENAME = '_'.join([MODE,BOOK,fp.get_chapter_name(CHAPTER,BOOK)])+'.csv'
inputfile.write(OUTPUT_FILENAME, this_data, header)


