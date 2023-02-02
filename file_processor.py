from math import ceil

class File_Processor:

    def __init__(self, file_name : str ,path : str = None) -> None:
        self.path = path
        self.file_name = file_name
        self.file_path = f"{path}\{file_name}" if path is not None else f"{file_name}"
        self.lines = []
        self.file = None
        
        print(f"Class Created")

    def print_path(self)-> str:
        return self.file_path
    
    def path_error_handling(self)-> None:
        try:
            self.file = open(f"{self.file_path}.txt", 'r')
        except OSError as e:
            print(f"Path or File does not exist. Error Code: {e.errno}")
            
    def initialize(self)-> list[str]:
        
        self.path_error_handling()

        with self.file:
            temp_lines = self.file.readlines()
        
        lines = []

        for line in temp_lines:
            if line.rstrip():
                  lines.append(line.rstrip())
        
        return lines

    def r_split(self, lines: list ,line_count: int, cut: bool = False)-> list:
        
        lines = self.initialize()
        lines_len = len(lines)
        divisions = ceil(lines_len / line_count) if not cut else (lines_len // line_count)
        print(f"Divisions : {divisions}")
       
        split_matrix = []

        for x in range(divisions):
        
            sliced_list = []
            
            if len(lines) < line_count:
                line_count = len(lines)

            for y in range(line_count):
                sliced_list.append(lines[y])
                print(lines[y])
                
                
            lines = lines[line_count:]

            split_matrix.append(sliced_list)
        
        return split_matrix

    def o_split(self, lines: list, line_count: int, cut: bool = False)-> list:
        
        lines = self.initialize()
        lines_len = len(lines)

        divisions = (lines_len - line_count) + 1 if cut else (lines_len - line_count) + 2

        split_matrix = []

        for x in range(divisions):
            
            sliced_list = []
            sliced_list = lines[x: line_count+x]
            split_matrix.append(sliced_list)        
        
        return split_matrix

    def split(self, line_count: int, overlap: bool = False, cut: bool = False)-> list:
        
        split_matrix = []

        if overlap:
            split_matrix = self.o_split(self.lines, line_count, cut)
        else:
            split_matrix = self.r_split(self.lines, line_count, cut)

        return split_matrix
        

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