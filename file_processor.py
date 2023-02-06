from math import ceil

class File_Processor:

    def __init__(self, file_name : str ,path : str = None) -> None:
        self.path = path
        self.file_name = file_name
        self.file_path = f"{path}\{file_name}" if path is not None else f"{file_name}"
        self.lines = []
        self.file = None
        self.divisons = 0
        
        

    def print_path(self)-> str:
        return self.file_path
    
    def path_error_handling(self)-> None:
        try:
            self.file = open(f"{self.file_path}.txt", encoding= "utf8" )
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
        
        lines_len = len(lines)
        self.divisions = ceil(lines_len / line_count) if not cut else (lines_len // line_count)
        print(f"Divisions : {self.divisions}")

        split_matrix = []
        slice_list = lines.copy()

        for x in range(self.divisions):
            split_matrix.append(slice_list[:line_count])
            slice_list = slice_list[line_count:]
        
        return split_matrix

    def o_split(self, lines: list, line_count: int, cut: bool = False)-> list:
        
        lines_len = len(lines)

        self.divisions = (lines_len - line_count) + 1 if cut else (lines_len - line_count) + 2

        split_matrix = []

        for x in range(self.divisions):
            sliced_list = lines[x: line_count+x]
            split_matrix.append(sliced_list)        
        
        return split_matrix


    def split(self, lines: list = None ,line_count: int = 1, overlap: bool = False, cut: bool = False)-> list:
        
        if lines is None:
            lines = self.initialize()
            
        split_matrix = []

        if overlap:
            split_matrix = self.o_split(lines, line_count, cut)
        else:
            split_matrix = self.r_split(lines, line_count, cut)

        return split_matrix
        

# file = File_Processor("test")

# test = file.initialize()
# mat = file.split(lines=test, line_count=2)
# print(mat)

# print("")
# print("")

# file2 = File_Processor("test")
# matrix = file2.split(line_count= 3,cut=True)
# print(matrix)
# print(file2.divisions) 
