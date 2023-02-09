import data_processor as dp
import file_processor as fp
import gl
import graphics as gp



filename = fp.get_filename('SN','AS',1)
inputfile = fp.File_Processor(filename)
content = inputfile.read()
text_obj = dp.Text('sanskrit',content)
no_digits = text_obj.remove_digit()
#no_symbols = text_obj.remove_symbol(no_digits)
#sentence_only = text_obj.get_sentence(no_digits)
no_headings = text_obj.remove_headings(no_digits)
blocks = inputfile.split(no_headings, 40, False, False)

print(blocks[0])


