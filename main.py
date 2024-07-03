import time
from collections import defaultdict, deque

class AhoCorasickAutomation:
    def __init__(self):
        self.transitions = [{}]
        self.failures = {}
        self.outputs = defaultdict(list)
        self.pattern_count = 1

    def add_pattern(self, pattern, output):
        current_state = 0
        for byte in pattern:
            if byte not in self.transitions[current_state]:
                self.transitions.append({})
                self.transitions[current_state][byte] = self.pattern_count
                current_state = self.pattern_count
                self.pattern_count += 1
            else:
                current_state = self.transitions[current_state][byte]
        self.outputs[current_state].append(output)

    def build(self):
        queue = deque()
        for byte in range(256):
            if byte in self.transitions[0]:
                state = self.transitions[0][byte]
                self.failures[state] = 0
                queue.append(state)
            else:
                self.transitions[0][byte] = 0

        while queue:
            state = queue.popleft()
            for byte, next_state in self.transitions[state].items():
                queue.append(next_state)
                fail_state = self.failures[state]
                while byte not in self.transitions[fail_state]:
                    fail_state = self.failures[fail_state]
                self.failures[next_state] = self.transitions[fail_state][byte]
                self.outputs[next_state].extend(self.outputs[self.failures[next_state]])

    def search(self, text):
        state = 0
        for index, byte in enumerate(text):
            while byte not in self.transitions[state]:
                state = self.failures[state]
            state = self.transitions[state][byte]
            for pattern in self.outputs[state]:
                yield index, pattern


class Compression:

    def get_input_file(self, input_file):
        with open(input_file, 'rb') as binary_file:
            binary_content = binary_file.read()
        return binary_content

    def find_patterns(self, binary_content, min_pattern_length):
        print(f"Finding patterns")
        pattern_count = defaultdict(int)

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
                pattern_file.write(f"({index})".encode('utf-8') + b" " + pattern + b"\n")
        return patref_file
    
    def replace_input_patterns(self, binary_content, patterns_found):
        automation = AhoCorasickAutomation()
        pattern_dict = {pattern: f"({index})".encode('utf-8') for index, pattern in enumerate(patterns_found)}

        for pattern, ref in pattern_dict.items():
            automation.add_pattern(pattern, ref)
        automation.build()

        replaced_content = bytearray()
        last_match_end = 0

        for index, ref in automation.search(binary_content):
            pattern_length = len(patterns_found[int(ref[1:-1])])
            start = index - pattern_length + 1
            replaced_content.extend(binary_content[last_match_end:start])
            replaced_content.extend(ref)
            last_match_end = index + 1
        
        replaced_content.extend(binary_content[last_match_end:])
        return bytes(replaced_content)
    
    def create_patport_file(self, input_file, replaced_content):
        patport_file = input_file + ".patport"
        with open(patport_file, 'wb') as output_file:
            output_file.write(replaced_content)
        return patport_file

if __name__ == '__main__':
    compress = Compression()
    input_file: str = input("File >>> ")
    pattern_length: int = int(input("Pattern Length >>> "))
    binary_content = compress.get_input_file(input_file)

    start_time = time.time()
    patterns_found = compress.find_patterns(binary_content, min_pattern_length=pattern_length)
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
    print(f"Time taken to create output file: {patport_end_time - patport_start_time:.2f} seconds")

    print(f"Pattern reference file created: {patref_file}")
    print(f"Output file created: {patport_file}")