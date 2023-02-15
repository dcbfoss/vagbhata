import data_processor as dp
import file_processor as fp
import graphics as gr


# Variables ------------------------

MODE = 'SN'     # SN/TL
BOOK = 'AS'     # AH/AS/CS
CHAPTER = 1     # 1/2/3/4/5/6
BLOCKSIZE = 25  # 25/50/75
ANALYSIS = 'I'  # Q/R/C/I
                # Quantitative // GL-Richness // Chi-Square // Image
SCALE = 400     # for image only (400/250/512/..)


# settings ------------------------

blocks = fp.get_blocks(MODE,BOOK,CHAPTER,BLOCKSIZE)

# Analysis ------------------------

data_obj = dp.Analysis(blocks)
if ANALYSIS.upper() == 'Q':
    header, this_data = data_obj.get_quantitative(MODE,BOOK,CHAPTER)
elif ANALYSIS.upper() == 'I':
    header, this_data = data_obj.get_graphics_data(MODE,BOOK,CHAPTER, SCALE)
else:
    header, this_data = data_obj.get_gl_richness(MODE,BOOK,CHAPTER)

# Writing Output ------------------

fp.write_data(MODE,BOOK,CHAPTER,ANALYSIS,BLOCKSIZE,this_data,header)


