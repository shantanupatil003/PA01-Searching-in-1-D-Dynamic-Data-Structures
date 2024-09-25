import time
import sys

class PythonListasArrayList:
    def __init__(self):
        self.words = []
        self.insert_time = 0
        self.resize_count = 0
        self.total_resize_time = 0

    def binary_search(self, word):
        left, right = 0, len(self.words) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.words[mid] == word:
                return mid
            elif self.words[mid] < word:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def insert_word(self, word):
        start_time = time.time()
        index = self.binary_search(word)
        if index < len(self.words) and self.words[index] == word:
            end_time = time.time()
            self.insert_time += (end_time - start_time)
            return  # Word already exists

        self.words.insert(index, word)
        end_time = time.time()
        self.insert_time += (end_time - start_time)

        if len(self.words) % 100 == 0:  # Assuming resize happens every 100 insertions
            self.resize_count += 1
            resize_start = time.time()
            # Python handles resizing internally, so we're just simulating the event
            resize_end = time.time()
            self.total_resize_time += (resize_end - resize_start)
            self.print_status()

    def print_status(self):
        n = len(self.words)
        if n > 0:
            indices = [0, n // 4, n // 2, 3 * n // 4, n - 1]
            selected_words = [self.words[i] for i in indices]
            print(f"Size: {n} |  Time: {self.insert_time:.4f}s, Words: {' -> '.join(selected_words)}")

    def get_memory_usage(self):
        return sys.getsizeof(self.words)

def load_words(filename):
    word_storage = PythonListasArrayList()
    word_count = 0
    
    start_time = time.time()
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip()
            word_storage.insert_word(word)
            word_count += 1
    end_time = time.time()
    
    total_time = end_time - start_time
    return word_storage, word_count, total_time

# Main program
filename = 'words_2000.txt'

print("Running with Python List like ArrayList)")
word_storage, word_count, total_time = load_words(filename)

print(f"Total words loaded: {word_count}")
print(f"Final list size: {len(word_storage.words)}")
print(f"Total time: {total_time:.4f} seconds")
print(f"Insert time: {word_storage.insert_time:.4f} seconds")
print(f"Number of resizes: {word_storage.resize_count}")
print(f"Total resize time: {word_storage.total_resize_time:.4f} seconds")
print(f"Average insert time: {(word_storage.insert_time / word_count):.8f} seconds")
print(f"Memory usage: {word_storage.get_memory_usage()} bytes")