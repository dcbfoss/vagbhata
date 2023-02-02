class Symbol_Sorter:

    def __init__(self, language:str) -> None:
        
        languages = ['sanskrit','Sanskrit', 'transliterated', 'Transliterated']
        if language not in languages:
            raise ValueError(f"Invalid language must be in {languages}")
        
        self.symbols_list = ['?', '(', ')', ',', '.', '/' , '\\', '-', '_', '!', '[', ']', '`','~', '{', '}', ':', ';', '+']
        self.digits_list = list(map(str, range(0,10)))

        if language in languages[0:2]:

            sans_digits = [chr(x) for x in range(2406,2416)]
            self.digits_list.extend(sans_digits)

            sans_symbols = [chr(2416), chr(2417), chr(2429)]
            self.symbols_list.extend(sans_symbols)
        

    def digit_remover(self, text: str) -> str:
        
        filter_list = list(text)
        filtered_text = ''.join([x for x in filter_list if x not in (self.digits_list)])
        return filtered_text
    
    def symbol_remover(self, text: str) -> str:
        
        filter_list = list(text)
        filtered_text = ''.join([x for x in filter_list if x not in (self.symbols_list)])
        return filtered_text
    
    def heading_finder(self, text_list: list[str]) -> dict:
        
        line_count = 0
        headings_dict = {}
        heading = ''.join([x for x in text_list[0] if not x.isdigit()]).strip()

        curr_heading = text_list[0]

        for x in range(len(text_list)):

            if(text_list[x].startswith(heading)):
                headings_dict[curr_heading] = line_count
                line_count = 0
                curr_heading = text_list[x]
            
            line_count += 1

        if curr_heading != text_list[-1]:
            headings_dict[curr_heading] = len(text_list[text_list.index(curr_heading) + 1:])

        return headings_dict  
        
    
    # Getter methods for testing and debugging
    def get_digits_list(self)->list:
        return self.digits_list
    
    def get_symbol_lists(self)->list:
        return self.symbols_list



sort = Symbol_Sorter('sanskrit')

print(sort.digit_remover('ॷॳ९८४'))
print(sort.symbol_remover('ॷॳ९८४!,[]()/\\'))