import data_processor as dp
import file_processor as fp
import graphics as gr
import os


# Variables ------------------------

MODE = 'SN'     # SN/TL
BOOK = 'AS'     # AH/AS/CS
CHAPTER = 1     # 1/2/3/4/5/6
BLOCKSIZE = 25  # 25/50/75
ANALYSIS = 'Q'  # Q/R/C/I
                # Quantitative // GL-Richness // Chi-Square // Image


# settings ------------------------

SCALE = BLOCKSIZE * 10    # for image only (400/250/512/..)
blocks = fp.get_blocks(MODE,BOOK,CHAPTER,BLOCKSIZE)

# Analysis ------------------------

data_obj = dp.Analysis(blocks)
if ANALYSIS.upper() == 'Q':
    header, this_data = data_obj.get_quantitative(MODE,BOOK,CHAPTER)
elif ANALYSIS.upper() == 'I':
    header, this_data = data_obj.get_graphics_data(MODE,BOOK,CHAPTER,BLOCKSIZE, SCALE)
elif ANALYSIS.upper() == 'C':
    FILENAME = fp.get_analysis_name('R')+'_'+str(BLOCKSIZE)+'_'+'_'.join([MODE,BOOK,fp.get_chapter_name(CHAPTER,BOOK)])+'.csv'
    if not(os.path.exists(FILENAME)):
        header, this_data = data_obj.get_gl_richness(MODE,BOOK,CHAPTER)
        fp.write_data(MODE,BOOK,CHAPTER,'R',BLOCKSIZE,this_data,header)
    header, this_data = dp.get_chi_square(MODE,BOOK,CHAPTER,FILENAME)
else:
    header, this_data = data_obj.get_gl_richness(MODE,BOOK,CHAPTER)

# Writing Output ------------------

fp.write_data(MODE,BOOK,CHAPTER,ANALYSIS,BLOCKSIZE,this_data,header)


