import time

class Compression:
    def get_input_file(self, input_file):
        with open(input_file, 'rb') as BINARY_FILE:
            BINARY_CONTENT = BINARY_FILE.read()
        return BINARY_CONTENT

    def find_patterns(self, BINARY_CONTENT):
        print(f"Finding patterns")
        seen = set()
        patterns_found = []
        for byte in BINARY_CONTENT:
            if byte in seen:
                patterns_found.append(byte)
            else:
                seen.add(byte)
        return patterns_found

    def create_patref_file(self, input_file, patterns_found):
        print(f"Creating pattern reference file.")
        PATREF_FILE = input_file + ".patref"
        with open(PATREF_FILE, 'w', encoding='utf-8') as pattern_file:
            pattern_file.write(','.join(map(str, patterns_found)))
        return PATREF_FILE
    
    def replace_input_patterns(self, BINARY_CONTENT, patterns_found):
        replaced_content = bytearray(BINARY_CONTENT)
        for index, pattern in enumerate(patterns_found):
            pattern_bytes = bytes([pattern])
            replacement_bytes = f"({index})".encode('utf-8')
            replaced_content = replaced_content.replace(pattern_bytes, replacement_bytes)
        return bytes(replaced_content)
    
    def create_patport_file(self, input_file, replaced_content):
        patport_file = input_file + ".patport"
        with open(patport_file, 'wb') as output_file:
            output_file.write(replaced_content)
        return patport_file

if __name__ == '__main__':
    compress = Compression()
    input_file = "Test-Lapce.msi"

    binary_content = compress.get_input_file(input_file)
    start_time = time.time()
    patterns_found = compress.find_patterns(binary_content)
    end_time = time.time()
    print(f"Time taken to find patterns: {end_time - start_time:.2f} seconds")
    patref_file = compress.create_patref_file(input_file, patterns_found)
    replaced_content = compress.replace_input_patterns(binary_content, patterns_found)
    patport_file = compress.create_patport_file(input_file, replaced_content)

    print(f"Pattern reference file created: {patref_file}")
    print(f"Output file created: {patport_file}")