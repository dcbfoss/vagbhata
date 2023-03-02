from math import ceil
import data_processor as dp
import graphics as gr
import os
import csv


SN_AH = 'data/Sanskrit/AH/'
SN_AS = 'data/Sanskrit/AS/'
SN_CS = 'data/Sanskrit/CS/'

TL_AH = 'data/Transliterated/AH/'
TL_AS = 'data/Transliterated/AS/'
TL_CS = 'data/Transliterated/CS/'

AH_AS_DOC_NAMES = ['chikitsa_sthana','kalpa_sthana','nidana_sthana','shareera_sthana','sutra_sthana','uttara_sthana']
CS_DOC_NAMES = ['chikitsa_sthana','kalpa_sthana','nidana_sthana','shareera_sthana','siddi_sthana','indriya_sthana']

DIRS = {'AS_TL':TL_AS,
        'AS_SN':SN_AS,
        'AH_TL':TL_AH,
        'AH_SN':SN_AH,
        'CS_TL':TL_CS,
        'CS_SN':SN_CS,}

def get_chapter_name(number, book):
    if book == 'CS':return CS_DOC_NAMES[number-1]
    else:return AH_AS_DOC_NAMES[number-1]

def get_analysis_name(val):
    val = val.upper()
    info = {'Q':'Quantitative','R':'GL-Richness','C':'Chi-Square','I':'Image'}
    return info.get(val,'Unknown')

def get_filename(mode='SN', book='AS', chapter=1):
    # mode = TL/SN
    # book = AS/AH/CS
    # chapter = 1/2/3/4/5
    selected_mode = 'SN';selected_book = 'AS';selected_chapter='chikitsa_sthana'
    if (mode.upper() == 'SN'):selected_mode = 'SN'
    else:selected_mode = 'TL'
    if (book.upper() == 'AS'):selected_book = 'AS'
    elif (book.upper() == 'AH'):selected_book = 'AH'
    else:selected_book = 'CS'
    if ((chapter > 0) and (chapter < 7)):selected_chapter = get_chapter_name(chapter, selected_book)
    elif (chapter < 1):selected_chapter = get_chapter_name(1, selected_book)
    elif (chapter > 6):selected_chapter = get_chapter_name(6, selected_book)
    else:selected_chapter = get_chapter_name(1, selected_book)
    FILENAME = '_'.join([selected_book, selected_chapter, selected_mode.lower()])+'.txt'
    DIRNAME = DIRS['_'.join([selected_book,selected_mode])]
    return DIRNAME+FILENAME


class File_Processor:

    def __init__(self, file_path):

        self.file_path = file_path
        self.file = None
        self.divisons = 0
        self.lines = None
        self.split_matrix = []
        
        

    def print_path(self):
        return self.file_path
    
    def path_error_handling(self):
        try:
            self.file = open(self.file_path , encoding= "utf8" )
        except OSError as e:
            print(f"Path or File does not exist. Error Code: {e.errno}")

            
    def read(self):
        
        self.path_error_handling()

        with self.file:
            temp_lines = self.file.readlines()
        
        lines = []

        for line in temp_lines:
            if line.rstrip():
                  lines.append(line.rstrip())

        self.lines = lines.copy()        
        return lines


    def r_split(self, lines ,line_count, cut = False):
        
        lines_len = len(lines)
        self.divisions = ceil(lines_len / line_count) if not cut else (lines_len // line_count)

        split_matrix = []
        slice_list = lines.copy()

        for x in range(self.divisions):
            split_matrix.append(slice_list[:line_count])
            slice_list = slice_list[line_count:]
        
        return split_matrix

    def o_split(self, lines, line_count, cut = False):
        
        lines_len = len(lines)

        self.divisions = (lines_len - line_count) + 1 if cut else (lines_len - line_count) + 2

        split_matrix = []

        for x in range(self.divisions):
            sliced_list = lines[x: line_count+x]
            split_matrix.append(sliced_list)        
        
        return split_matrix


    def split(self, lines = None ,line_count = 1, overlap = False, cut = False):
        
        if not lines and not self.lines:
            self.lines = self.read()
        elif lines is not None:
            self.lines = lines.copy()
            
        if overlap:
            self.split_matrix = self.o_split(self.lines, line_count, cut)
        else:
            self.split_matrix = self.r_split(self.lines, line_count, cut)
        
        return self.split_matrix

    def get_lines(self):
        return self.lines

    def get_split_matrix(self):
        return self.split_matrix
        

    def write(self, file_path, data = None, fields = None):

        if '/' in file_path:
            file = file_path.split('/')
            if not os.path.exists(file[0]):
                raise OSError(f"Diretctory {file[0]} does not exist: {OSError.errno}")
        
        assert len(data[0]) == len(fields), "Lengths do not match for data and fields"

        with open(file_path, 'w', newline='',encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            writer.writerows(data)

# To Create directories and to get a list of required file names and paths
class Manage_Files:

    def __init__(self, divisions:int = None, book:str = 'AS', data_type:str = "Chi-Square", abs_path = None):

        if(divisions not in [25,50,75,None]):
            raise ValueError
        self.divisions = divisions

        if not divisions and not abs_path:
            self.dir_path = os.path.join('data','result', book, data_type)
        elif abs_path:
            self.dir_path = abs_path
        else:
            self.dir_path = os.path.join('data', 'result', book, data_type, str(self.divisions))
   
    # Gets the list of file names
    def get_file_paths(self):

        file_names = []
        for path in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path,path)
            if os.path.isfile(file_path):
                file_names.append(file_path)

        return file_names

    def make_dir(self,dir_name, dir_parent = ""):

        dir_path = os.path.join(str(dir_parent), str(dir_name))
        exists = os.path.exists(dir_path)
    
        if not exists:
            os.mkdir(dir_path)

        return dir_path




def get_blocks(MODE,BOOK,CHAPTER,BLOCKSIZE):
    TEXTS = {'SN':'sanskrit','TL':'transliterated'}
    filename = get_filename(MODE,BOOK,CHAPTER)
    inputfile = File_Processor(filename)
    content = inputfile.read()
    text_obj = dp.Text(TEXTS[MODE],content)
    no_digits = text_obj.remove_digit()
    no_symbols = text_obj.remove_symbol(no_digits)
    no_headings = text_obj.remove_headings(no_symbols)
    if BOOK == 'CS':
        sentence_only = text_obj.get_sentence_CS(no_headings)
        full_stop_remove = text_obj.remove_full_stop_CS(sentence_only)
    else:
        sentence_only = text_obj.get_sentence(no_headings)
        full_stop_remove = text_obj.remove_full_stop(sentence_only)
    blocks = inputfile.split(full_stop_remove, BLOCKSIZE, True, True)
    return blocks

def write_data(MODE,BOOK,CHAPTER,ANALYSIS,BLOCKSIZE,this_data,header):
    if ANALYSIS=='I':
        for i, j in zip(header, this_data):
            gr.draw_png(i, j)
    else:
        OUTPUT_FILENAME = get_analysis_name(ANALYSIS)+'_'+str(BLOCKSIZE)+'_'+'_'.join([MODE,BOOK,get_chapter_name(CHAPTER,BOOK)])+'.csv'
        File_Processor.write(None,OUTPUT_FILENAME, this_data, header)
