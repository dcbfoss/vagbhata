from math import ceil
import os
import csv

class File_Processor:

    def __init__(self, file_path):

        self.file_path = file_path
        print(self.file_path)
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
