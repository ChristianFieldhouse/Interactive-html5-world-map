import pycountry
from matplotlib import cm

stupid_pycountry = {
    "south korea": "KR",
    "north korea": "KP",
    "cape verde": "CV",
    "democratic republic of congo": "CD",
    "laos": "LA",
    "swaziland": "SZ",
    
}

def string_to_country_code(string):
    
    if string.lower() in stupid_pycountry:
        return stupid_pycountry[string.lower()]  
    if '(' in string:
        return string_to_country_code(string.split('(')[0].rstrip())
    try:
        return pycountry.countries.search_fuzzy(string)[0].alpha_2
    except:
        print("is ", string, " a country?")
        return None

def csv_to_string_tuples(filename):
    with open(filename) as f:
        lines = f.readlines()
    
    split_lines = [line.split(",") for line in lines]
    return split_lines

def country_names_to_alpha_2_codes(string_tuples, country_col=0):
    for tuple in string_tuples:
        try:
            tuple[country_col] = string_to_country_code(tuple[country_col])
        except:
            print("Not a country : ", tuple[country_col])
            tuple[country_col] = None
    return [t for t in string_tuples if t[country_col] is not None]
    
def strings_to_numbers(string_tuples, number_col=-1):
    for tuple in string_tuples:
        tuple[number_col] = float(tuple[number_col]) # ok not tuples
        
    return string_tuples
    
def numbers_to_colours(rows, col=-1):

    max_entry = max([t[col] for t in rows])
    min_entry = min([t[col] for t in rows])
    range = max_entry -  min_entry
    
    for t in rows:
        r = [int(255 * e + 0.5) for e in cm.viridis(float(((t[col] - min_entry) / range)))]
        if t[col] == max_entry:
            print(float((t[col] - min_entry) / range))
            print(r, "{0:#0{1}x}".format(r[2] + (r[1] << 8) + (r[0] << 16), 8))
        t[col] = "{0:#0{1}x}".format(r[2] + (r[1] << 8) + (r[0] << 16), 8)
        
    return rows

d = csv_to_string_tuples("share-of-adults-defined-as-obese.csv")
d = [t for t in d if t[2]=="2016"]
d = country_names_to_alpha_2_codes(d)
d = strings_to_numbers(d)
d = numbers_to_colours(d)

as_json = {d0[0].lower(): '#'+d0[-1][2:] for d0 in d}
