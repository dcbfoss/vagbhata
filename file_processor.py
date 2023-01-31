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
            
    def initialize(self)-> list:
        
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
        

