import stats as st
import file_processor as fp
import graphics as gr
import gl
from tqdm import tqdm

class Text:

    def __init__(self, language, text_list = None):
        
        languages = ['sanskrit','Sanskrit','sn', 's', 'transliterated', 'Transliterated', 'tl', 't']
        if language not in languages:
            raise ValueError(f"Invalid language, must be either {', '.join(languages)}")
        
        self.symbols_list = ['?', '(', ')', ',', '.', '/' , '\\', '-', '_', '!', '[', ']', '`','~', '{', '}', ':', ';', '+']
        self.digits_list = list(map(str, range(0,10)))

        if language in languages[0:4]:

            sans_digits = [chr(x) for x in range(2406,2416)]
            self.digits_list.extend(sans_digits)

            sans_symbols = [chr(2416), chr(2417), chr(2429)]
            self.symbols_list.extend(sans_symbols)
        
        self.text_list = text_list
        self.heading_dict = None

    def check_initialized(self, text_list):
        if not text_list and self.text_list: 
            text_list = self.text_list
            return text_list
        elif not text_list and not self.text_list:
            raise OSError(f"text_list has not been initialized for instance.")
            
      

    def remove_digit(self, text_list = None):
        
        if not text_list:
            text_list = self.check_initialized(text_list)

        filter_list = text_list.copy()
        for line in range(len(filter_list)):
            filter_list[line] = ''.join([x for x in filter_list[line] if x not in (self.digits_list)]).strip()
        
        self.text_list = filter_list.copy()

        return filter_list
    
    def remove_symbol(self, text_list = None):
        
        if not text_list:
            text_list = self.check_initialized(text_list)

        filter_list = text_list.copy()
        for line in range(len(filter_list)):
            filter_list[line] = ''.join([x for x in filter_list[line] if x not in (self.symbols_list)]).strip()
        
        self.text_list = filter_list.copy()

        return filter_list
    
    def find_headings(self, text_list = None):

        if not text_list:
            text_list = self.check_initialized(text_list)
        
        line_count = 0
        headings_dict = {}
        heading = ''.join([x for x in text_list[0] if not x.isdigit()]).strip()

        curr_heading = text_list[0]

        for x in range(1,len(text_list)):

            if(text_list[x].startswith(heading)):
                headings_dict[curr_heading] = line_count
                line_count = 0
                curr_heading = text_list[x]
                continue
            
            line_count += 1

        if curr_heading != text_list[-1]:
            headings_dict[curr_heading] = len(text_list[text_list.index(curr_heading) + 1:])

        self.heading_dict = headings_dict.copy()
        return headings_dict  

    def remove_headings(self, text_list = None, heading = None):
        if not text_list:
            text_list = self.check_initialized(text_list)

        if not heading:
            heading = ''.join([x for x in text_list[0] if not x.isdigit()]).strip()

        heading_removed_list = [x for x in text_list if not x.startswith(heading)]
        
        self.text_list = heading_removed_list

        return heading_removed_list
    
    def remove_full_stop(self, text_list = None, count = 2):
        
        if not text_list:
            text_list = self.check_initialized(text_list)

        filter_list = text_list.copy()

        for x in range(len(text_list)):
            filter_list[x] = filter_list[x].replace('॥', '', count).strip()
            filter_list[x] = filter_list[x].replace('।', '', count).strip()
        
        filter_list = [x for x in filter_list if x]

        self.text_list = filter_list.copy()
        return filter_list
    
    def remove_full_stop_CS(self, text_list = None, count = 4):
        
        if not text_list:
            text_list = self.check_initialized(text_list)

        filter_list = text_list.copy()

        for x in range(len(text_list)):
            filter_list[x] = filter_list[x].replace('|', '', count).strip()
        
        filter_list = [x for x in filter_list if x]
            
        self.text_list = filter_list.copy()
        return filter_list

    def get_sentence(self, text_list = None):
        
        if not text_list:
            text_list = self.check_initialized(text_list)
            
         
        temp_str = ' '.join(text_list)
        sentence_list = []
        iter = 0
        while temp_str:
            
            if temp_str[iter] == '॥' or temp_str[iter] == '।':
                
                sentence_list.append(temp_str[:iter+1])
                
                temp_str = temp_str[iter+1:].strip()
                iter = 0
            else:
                iter += 1
            
            if (len(temp_str)-1) < iter or (len(temp_str)-1) < (iter + 1):
                sentence_list.append(temp_str)
                break   
        
        self.text_list = sentence_list.copy()
        return sentence_list 
    

    def get_sentence_CS(self, text_list = None):
        
        if not text_list:
            text_list = self.check_initialized(text_list)
            
         
        temp_str = ' '.join(text_list)
        sentence_list = []
        iter = 0
        while temp_str:
            
            offset = 1

            if temp_str[iter] == '|':
                
                if temp_str[iter+1] == '|':
                    offset += 1
                sentence_list.append(temp_str[:iter+offset])
                temp_str = temp_str[iter+offset:].strip()
                iter = 0
            else:
                iter += 1
            
            if (len(temp_str)-1) < iter or (len(temp_str)-1) < (iter + 1):
                sentence_list.append(temp_str)
                break   
        
        self.text_list = sentence_list.copy()
        return sentence_list 

    # Getter methods for testing and debugging
    def get_list(self):
        return self.text_list
    
    def get_heading_dict(self):
        return self.heading_dict

    def get_digits_list(self):
        return self.digits_list
    
    def get_symbol_lists(self):
        return self.symbols_list

class Analysis:
    def __init__(self, data):
        self.data = data
        
    def get_quantitative(self,MODE,BOOK,CHAPTER):
        this_data = []
        header = ['Text_Type','Book','Chapter','Window','Avg Word Len', 'Avg Sen Len (Word)', 'Avg Sen Len (Chr)', 'Richness', 'Shannon', 'Avg Compound Words']
        for INDEX, block in enumerate(self.data):
            txt_obj = st.text_object(block)
            avg_word_len = txt_obj.average_word_len()
            avg_sen_len_w = txt_obj.average_sentence_word_len()
            avg_sen_len_c = txt_obj.average_sentence_chr_len()
            rich_ratio = txt_obj.get_richness_ratio()
            shannon = txt_obj.get_shannon()
            avg_compound_words = txt_obj.average_compound_words()
            this_data.append([MODE,BOOK,fp.get_chapter_name(CHAPTER,BOOK).split('_')[0],INDEX+1,round(avg_word_len,2),round(avg_sen_len_w,2),round(avg_sen_len_c,2),round(rich_ratio,2),round(shannon,2),round(avg_compound_words,2)])
        return (header, this_data)

    def get_gl_richness(self,MODE,BOOK,CHAPTER):
        this_data = []
        header = ['Text_Type','Book','Chapter','Window']
        block_patterns = []
        for i in range(len(self.data)):
            val = gl.gl_patterns(self.data[i])
            block_patterns.append(val)
        this_header = gl.gl_pattern_header(block_patterns)
        this_richness = gl.gl_richness(this_header, block_patterns)
        for i in this_header:
            header.append(i)
        for i, j in enumerate(this_richness):
            this_row = [MODE,BOOK,fp.get_chapter_name(CHAPTER,BOOK).split('_')[0],str(i+1)]
            for k in j:
                this_row.append(str(k))
            this_data.append(this_row)
        return (header, this_data)

    def get_graphics_data(self, MODE, BOOK, CHAPTER, BLOCKSIZE, SCALE = 400):
        HEADER = []; DATA = []
        for INDEX, block in enumerate(self.data):
            this_matrix = gl.create_matrix(block, int(SCALE/10))
            this_img_data = gr.prepare_image(this_matrix,SCALE)
            FILENAME = '_'.join([MODE,BOOK,str(BLOCKSIZE),str(CHAPTER),fp.get_chapter_name(CHAPTER,BOOK).split('_')[0],str(INDEX+1)])
            HEADER.append(FILENAME)
            DATA.append(this_img_data)
        return (HEADER, DATA)

def chi_square(block1, block2):
    w1 = []; w2 = []; sum_list = []; output = 0
    for i in range(len(block1)):
        if block1[i] == 0 and block2[i] == 0:pass
        else:w1.append(block1[i]); w2.append(block2[i]);sum_list.append(w1[-1]+w2[-1])
    b1_sum = 0; b2_sum = 0;total = 1;b1_arr = []; b2_arr = []
    b1_sum = sum(w1); b2_sum = sum(w2); total = sum(sum_list)
    for i in range(len(sum_list)):
        output += (((w1[i] - ((sum_list[i]*b1_sum)/total))**2)/((sum_list[i]*b1_sum)/total))
        output += (((w2[i] - ((sum_list[i]*b2_sum)/total))**2)/((sum_list[i]*b2_sum)/total))
    return output
    

def get_chi_square(MODE,BOOK,CHAPTER,FILENAME):
    this_data = []; header = ['Text_Type','Book','Chapter','Window']
    temp_data = []
    with open(FILENAME, 'r') as inpfile:
        for i, line in enumerate(inpfile):
            if i>0:temp_data.append([float(i) for i in line.rstrip().split(',')[4:]])
    for INDEX, i in tqdm(enumerate(temp_data)):
        header.append(str(INDEX+1))
        this_row = [MODE,BOOK,fp.get_chapter_name(CHAPTER,BOOK).split('_')[0],str(INDEX+1)]
        for j in temp_data:
            this_row.append(round(chi_square(i, j),2))
        this_data.append(this_row)
    return (header, this_data)

