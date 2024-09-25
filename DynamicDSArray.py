import time
import math

class DynamicDSArray:
    def __init__(self, capacity=2, strategy='A'):
        self.array = [None] * capacity
        self.size = 0
        self.capacity = capacity
        self.strategy = strategy
        self.fibonacci = [1, 1]  # Initialize Fibonacci sequence for strategy C
        self.resize_count = 0
        self.total_resize_time = 0
        self.start_time = time.time()

    def append(self, element):
        if self.size == self.capacity:
            self._resize()
        self.array[self.size] = element
        self.size += 1

    def _resize(self):
        start_time = time.time()
        
        if self.strategy == 'incremental':
            new_capacity = self.capacity + 10
        elif self.strategy == 'double':
            new_capacity = self.capacity * 2
        elif self.strategy == 'fibonacci':
            while self.fibonacci[-1] <= self.capacity:
                self.fibonacci.append(self.fibonacci[-1] + self.fibonacci[-2])
            new_capacity = self.fibonacci[-1]
        
        new_array = [None] * new_capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity
        
        end_time = time.time()
        self.resize_count += 1
        self.total_resize_time += (end_time - start_time)

        self._print_status()

    def _print_status(self):
        elapsed_time = time.time() - self.start_time
        n = self.size
        elements = [
            self.array[0],
            self.array[n // 4] if n > 3 else None,
            self.array[n // 2] if n > 1 else None,
            self.array[3 * n // 4] if n > 3 else None,
            self.array[n - 1] if n > 0 else None
        ]
        elements = [str(e) if e is not None else '' for e in elements]
        # print(f"Size: {self.size}, Time: {elapsed_time:.4f}s, Elements: {' -> '.join(elements)}")

    def binary_search(self, word):
        left, right = 0, self.size - 1
        while left <= right:
            mid = (left + right) // 2
            if self.array[mid] == word:
                return mid
            elif self.array[mid] < word:
                left = mid + 1
            else:
                right = mid - 1
        return left

    def insert_sorted(self, word):
        index = self.binary_search(word)
        if index < self.size and self.array[index] == word:
            return  # word already exists 
        self.append(None)  # make space for the new word
        for i in range(self.size - 1, index, -1):
            self.array[i] = self.array[i - 1]
        self.array[index] = word


    def __str__(self):
        return str(self.array[:self.size])
    

def load_words(filename, strategy):
    eowl = DynamicDSArray(strategy=strategy)
    total_time = 0
    word_count = 0
    
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip()
            start_time = time.time()
            eowl.insert_sorted(word)
            end_time = time.time()
            total_time += (end_time - start_time)
            word_count += 1
            
            # if word_count % 10000 == 0:
            #     print(f"Strategy {strategy}: Processed {word_count} words. Current size: {eowl.size}, Capacity: {eowl.capacity}")
    
    return eowl, total_time, word_count

# Main program
filename = 'words_2000.txt'
strategies = ['incremental', 'double', 'fibonacci']

for strategy in strategies:
    print(f"\nRunning with Strategy {strategy}")
    eowl, total_time, word_count = load_words(filename, strategy)
    
    print(f"Total words loaded: {word_count}")
    print(f"Final array capacity: {eowl.capacity}")
    print(f"Number of resizes: {eowl.resize_count}")
    print(f"Total time for inserts: {total_time:.4f} seconds")
    print(f"Total time for resizes: {eowl.total_resize_time:.4f} seconds")
    print(f"Average insert time: {(total_time / word_count):.8f} seconds")
    if eowl.resize_count > 0:
        print(f"Average resize time: {(eowl.total_resize_time / eowl.resize_count):.8f} seconds")