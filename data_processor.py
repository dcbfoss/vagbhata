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


