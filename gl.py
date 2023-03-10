import itertools
connector = 2381
signs = [i for i in range(2366,2373)];signs.extend([2375,2376,2379,2380,2402,2403])
numbers = [j for j in range(2406,2416)]
special = [k for k in range(2305,2308)]
vowels = [a for a in range(2309,2317)];vowels.extend([2319,2320,2323,2324,2365,2401])
constants = [b for b in range(2325,2345)];constants.extend([c for c in range(2346,2353)]);constants.extend([2354,2357,2358,2359,2360,2361])
removables = [2404,2405]
signsandconnector = list(signs);signsandconnector.append(connector);signsandconnector.extend(special)

def get_syllables(text: str):
    output = [];connected = False
    length = len(text)
    for index in range(length):
        if ord(text[index])<2304 or ord(text[index])>2431:connected = False;continue
        if not connected:output.append(text[index])
        else:output[-1] += text[index]
        if index+1 >= length:continue
        elif ord(text[index+1]) in signsandconnector:connected = True
        elif ord(text[index]) in [connector]:connected = True
        else:connected = False
    return output

def get_lg(syllables: list):
    skip = [2365, 2381];output = []
    laghu_chars = [2309, 2311, 2313, 2315, 2316, 2318, 2322, 2325, 2326, 2327,
                   2328, 2329, 2330, 2331, 2332, 2333, 2334, 2335, 2336, 2337,
                   2338, 2339, 2340, 2341, 2342, 2343, 2344, 2345, 2346, 2347,
                   2348, 2349, 2350, 2351, 2352, 2353, 2354, 2355, 2356, 2357,
                   2358, 2359, 2360, 2361, 2367, 2369, 2371, 2374, 2378, 2381,
                   2392, 2393, 2394, 2395, 2396, 2397, 2398, 2399, 2402]
    for index, syllable in enumerate(syllables):
        if ord(syllable[-1]) in removables:output.append(chr(45))
        elif ord(syllable[-1]) in numbers:output.append(chr(45))
        elif ord(syllable[-1]) in skip:output.append(chr(45))
        else:
            l_data = [True if (ord(i) in laghu_chars) else False for i in syllable]
            if (index < (len(syllables)-1)):
                if ((all(l_data)) and not((chr(skip[-1]) in syllables[index+1]))):output.append(chr(76))
                else:output.append(chr(71))
            elif (index == (len(syllables)-1)):
                if all(l_data):output.append(chr(76))
                else:output.append(chr(71))
            else:pass
    return output

def slice_list(syllables: list, cropsize: int=40):
    if len(syllables)<=cropsize:return [syllables]
    output = []
    while len(syllables)>0:
        output.append(syllables[0:25])
        syllables = syllables[25:]
    return output

def create_matrix(sanskrit_lines: list,frame_width: int=40):
    val_arr = {chr(45):-1,chr(76):0,chr(71):1}
    output = [[-1 for j in range(frame_width)] for i in range(len(sanskrit_lines))]
    for index, line in enumerate(sanskrit_lines):
        gl = slice_list(get_lg(get_syllables(line)),frame_width)[0]
        for ind, entry in enumerate(gl):
            output[index][ind] = val_arr[gl[ind]]
    return output

def get_gl_count(sankskrit_lines: list):
    g_count = 0; l_count= 0
    for line in sanskrit_lines:
        gl = "".join(get_lg(get_syllables(line)))
        g_count += gl.count(chr(71))
        l_count += gl.count(chr(76))
    return {chr(71):g_count, chr(76):l_count}

def get_gl_ratio(sankskrit_lines: list):
    count = get_gl_count(sankskrit_lines)
    g_ratio = count[chr(71)]/(count[chr(71)]+count[chr(76)])
    l_ratio = count[chr(76)]/(count[chr(71)]+count[chr(76)])
    return (g_ratio, l_ratio)

def crop_by_three(text):
    output = []
    while len(text)>0:
        output.append(text[0:3])
        text = text[3:]
    return output

def gl_patterns(block):
    output = list(itertools.chain.from_iterable([crop_by_three(''.join(get_lg(get_syllables(i))).replace('-','')) for i in block]))
    return output

def gl_pattern_header(matrix):
    header = []
    for i in matrix:
        this_head = list(set(i))
        for j in this_head:
            if not(j in header):header.append(j)
    return header

def gl_richness(header, data):
    output = []
    for d in data:
        this_d = [0 for i in header]
        for e in d:
            this_d[header.index(e)] += 1
        output.append(this_d)
    return output
