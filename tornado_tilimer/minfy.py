from .js_tools import jsmin
import .static_data as static_data

from csscompressor import compress
import hashlib
import os.path
import os


def _md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def md5_for_file(fname):
    with open(fname, 'rb') as f:
        return _md5_for_file(f)


def _minfy_static_files(root_path, dealer):
    
    raw_list = os.listdir(root_path)
    
    min_data_filename = os.path.join(root_path, '.min.json')
    min_data = static_data.get_data(min_data_filename)
    min_list = []
    
    for line in raw_list:
        if os.path.isdir( os.path.join( root_path, line ) ):
            continue
        if ".min." in line:
            continue
        file = ".".join(line.split(".")[0:-1])
        ext = line.split(".")[-1]
        file_path = os.path.join( root_path, line )
        file_md5 = md5_for_file(file_path)
        
        if file not in min_data or min_data.get(file, None) != file_md5:
            
            print(("minfy file " + file_path).title())
            
            minfy_path = os.path.join( root_path, file + ".min." + ext )
            
            with open(file_path, "r", encoding = "utf-8") as input_f:
                minfy_file = dealer(input_f.read())
            with open(minfy_path, "w", encoding = "utf-8") as output_f:
                output_f.write(minfy_file)
            
            min_data[file] = file_md5
        
        min_list.append(file)
    
    for index in min_data:
        if index not in min_list:
            del min_data[min_data]
    
    if cmp(static_data.get_data(min_data_filename), min_data) != 0:
        static_data.write_data(min_data_filename, min_data)

def init_minfy(css_list = [], js_list = []):
    for line in css_list:
        minfy_static_files(line, compress)
    for line in js_list:
        minfy_static_files(line, jsmin)
