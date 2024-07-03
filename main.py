import time
from collections import defaultdict

class Compression:
    def get_input_file(self, input_file):
        with open(input_file, 'rb') as binary_file:
            binary_content = binary_file.read()
        return binary_content

    def find_patterns(self, binary_content, min_pattern_length=9):
        print(f"Finding patterns")
        pattern_count = defaultdict(int)
        patterns_found = []

        for i in range(len(binary_content) - min_pattern_length + 1):
            pattern = binary_content[i:i + min_pattern_length]
            pattern_count[pattern] += 1

        patterns_found = [pattern for pattern, count in pattern_count.items() if count > 1]
        return patterns_found

    def create_patref_file(self, input_file, patterns_found):
        print(f"Creating pattern reference file.")
        patref_file = input_file + ".patref"
        with open(patref_file, 'wb') as pattern_file:
            for index, pattern in enumerate(patterns_found):
                pattern_file.write(f'({index})'.encode('utf-8') + b' ' + pattern + b'\n')
        return patref_file
    
    def replace_input_patterns(self, binary_content, patterns_found):
        pattern_dict = {pattern: f"({index})".encode('utf-8') for index, pattern in enumerate(patterns_found)}
        replaced_content = bytearray()
        i = 0

        while i < len(binary_content):
            replaced = False
            for pattern, ref in pattern_dict.items():
                pattern_length = len(pattern)
                if binary_content[i:i + pattern_length] == pattern:
                    replaced_content.extend(ref)
                    i += pattern_length
                    replaced = True
                    break
            if not replaced:
                replaced_content.append(binary_content[i])
                i += 1

        return bytes(replaced_content)
    
    def create_patport_file(self, input_file, replaced_content):
        patport_file = input_file + ".patport"
        with open(patport_file, 'wb') as output_file:
            output_file.write(replaced_content)
        return patport_file

if __name__ == '__main__':
    compress = Compression()
    input_file = "Title.mp3"

    binary_content = compress.get_input_file(input_file)

    start_time = time.time()
    patterns_found = compress.find_patterns(binary_content)
    end_time = time.time()
    print(f"Time taken to find patterns: {end_time - start_time:.2f} seconds")

    patref_start_time = time.time()
    patref_file = compress.create_patref_file(input_file, patterns_found)
    patref_end_time = time.time()
    print(f"Time taken to create patref file: {patref_end_time - patref_start_time:.2f} seconds")

    replace_start_time = time.time()
    replaced_content = compress.replace_input_patterns(binary_content, patterns_found)
    replace_end_time = time.time()
    print(f"Time taken to replace patterns file: {replace_end_time - replace_start_time:.2f} seconds")

    patport_start_time = time.time()
    patport_file = compress.create_patport_file(input_file, replaced_content)
    patport_end_time = time.time()
    print(f"Time taken to replace patterns file: {patport_end_time - patport_start_time:.2f} seconds")

    print(f"Pattern reference file created: {patref_file}")
    print(f"Output file created: {patport_file}")