
connector = 2381
signs = [i for i in range(2366,2373)];signs.extend([2375,2376,2379,2380,2402,2403])
numbers = [j for j in range(2406,2416)]
special = [k for k in range(2305,2308)]
vowels = [a for a in range(2309,2317)];vowels.extend([2319,2320,2323,2324,2365,2401])
constants = [b for b in range(2325,2345)];constants.extend([c for c in range(2346,2353)]);constants.extend([2354,2357,2358,2359,2360,2361])
removables = [2404,2405]
signsandconnector = list(signs);signsandconnector.append(connector);signsandconnector.extend(special)

def get_syllables(text):
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

def get_lg(syllables):
    skip = [2365, 2381];output = []
    laghu_chars = [2309, 2311, 2313, 2315, 2316, 2318, 2322, 2325, 2326, 2327,
                   2328, 2329, 2330, 2331, 2332, 2333, 2334, 2335, 2336, 2337,
                   2338, 2339, 2340, 2341, 2342, 2343, 2344, 2345, 2346, 2347,
                   2348, 2349, 2350, 2351, 2352, 2353, 2354, 2355, 2356, 2357,
                   2358, 2359, 2360, 2361, 2367, 2369, 2371, 2374, 2378, 2381,
                   2392, 2393, 2394, 2395, 2396, 2397, 2398, 2399, 2402]
    for index, syllable in enumerate(syllables):
        if ord(syllable[-1]) in removables:output.append('-')
        elif ord(syllable[-1]) in numbers:output.append('-')
        elif ord(syllable[-1]) in skip:output.append('-')
        else:
            l_data = [True if (ord(i) in laghu_chars) else False for i in syllable]
            if (index < (len(syllables)-1)):
                if ((all(l_data)) and not((chr(skip[-1]) in syllables[index+1]))):output.append('L')
                else:output.append('G')
            elif (index == (len(syllables)-1)):
                if all(l_data):output.append('L')
                else:output.append('G')
            else:pass
    return output
