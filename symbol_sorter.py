from file_processor import File_Processor as fp


class Symbol_Sorter:

    def __init__(self, language:str, text_list: list[str] = None) -> None:
        
        languages = ['sanskrit','Sanskrit', 'transliterated', 'Transliterated']
        if language not in languages:
            raise ValueError(f"Invalid language, must be one in {languages}")
        
        self.symbols_list = ['?', '(', ')', ',', '.', '/' , '\\', '-', '_', '!', '[', ']', '`','~', '{', '}', ':', ';', '+']
        self.digits_list = list(map(str, range(0,10)))

        if language in languages[0:2]:

            sans_digits = [chr(x) for x in range(2406,2416)]
            self.digits_list.extend(sans_digits)

            sans_symbols = [chr(2416), chr(2417), chr(2429)]
            self.symbols_list.extend(sans_symbols)
        
        self.text_list = text_list
        self.heading_dict = None
        

    def digit_remover(self, text_list: list[str] = None) -> list[str]:
        
        if not text_list and self.text_list: 
            text_list = self.text_list
        elif not text_list and not self.text_list:
            print(f"text_list has not been initialized for instance.")
            return

        filter_list = text_list.copy()
        for line in range(len(filter_list)):
            filter_list[line] = ''.join([x for x in filter_list[line] if x not in (self.digits_list)]).strip()
        
        self.text_list = filter_list.copy()

        return filter_list
    
    def symbol_remover(self,  text_list: list[str] = None) -> list[str]:
        
        if not text_list and self.text_list: 
            text_list = self.text_list
        elif not text_list and not self.text_list:
            print(f"text_list has not been initialized for instance.")
            return

        filter_list = text_list.copy()
        for line in range(len(filter_list)):
            filter_list[line] = ''.join([x for x in filter_list[line] if x not in (self.symbol_remover)]).strip()
        
        self.text_list = filter_list.copy()

        return filter_list
    
    def headings_finder(self, text_list: list[str] = None) -> dict:

        if not text_list and self.text_list: 
            text_list = self.text_list
        elif not text_list and not self.text_list:
            print(f"text_list has not been initialized for instance.")
            return
        
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

    def heading_remover(self, text_list: list[str] = None, heading: str = None):
        
        if not text_list and self.text_list: 
            text_list = self.text_list
        elif not text_list and not self.text_list:
            print(f"text_list has not been initialized for instance.")
            return

        if not heading:
            heading = ''.join([x for x in text_list[0] if not x.isdigit()]).strip()
        
        heading_removed_list = [x for x in text_list if not x.startswith(heading)]
        
        self.text_list = heading_removed_list

        return heading_removed_list
    
    def full_stop_remover(self, text_list: list[str] = None):
        
        if not text_list and self.text_list: 
            text_list = self.text_list
        elif not text_list and not self.text_list:
            print(f"text_list has not been initialized for instance.")
            return

        filter_list = text_list.copy()

        for x in range(len(text_list)):
            filter_list[x] = filter_list[x].replace('|', '', 4).strip()
        
        self.text_list = filter_list.copy()
        return filter_list
            
    
    # Getter methods for testing and debugging
    def processed_list(self)->list[str]:
        return self.text_list
    
    def heading_dict(self)->list[str]:
        return self.heading_dict

    def get_digits_list(self)->list:
        return self.digits_list
    
    def get_symbol_lists(self)->list:
        return self.symbols_list



sort = Symbol_Sorter('Transliterated')

test1 = fp('test', 'tests')
lines_list = test1.read()

a = sort.digit_remover(lines_list)
print(a)
print("")
print("")
a = sort.heading_remover(a)
print(a)
print("")
print("")
a = sort.full_stop_remover(a)
print(a)