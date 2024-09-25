import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class DynamicDSLinkedList:
    def __init__(self, strategy='incremental'):
        self.head = None
        self.size = 0
        self.insert_time = 0
        self.comparison_count = 0
        self.strategy = strategy
        self.next_threshold = 10  # Initial threshold for all strategies
        self.fib_prev = 0
        self.fib_curr = 1

    def search(self, word):
        current = self.head
        index = 0
        while current:
            if current.data == word:
                return index
            elif current.data > word:
                return -1  # Word not found, but would be inserted at this index
            current = current.next
            index += 1
        return -1

    def insert(self, word):
        start_time = time.time()
        new_node = Node(word)
        
        if not self.head or word < self.head.data:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and current.next.data < word:
                current = current.next
                self.comparison_count += 1
            
            if current.next and current.next.data == word:
                # Word already exists, don't insert
                end_time = time.time()
                self.insert_time += (end_time - start_time)
                return

            new_node.next = current.next
            current.next = new_node
        
        self.size += 1
        end_time = time.time()
        self.insert_time += (end_time - start_time)

        # Apply growth strategy
        if self.size == self.next_threshold:
            self.apply_strategy()

    def apply_strategy(self):
        if self.strategy == 'incremental':
            self.next_threshold += 10
        elif self.strategy == 'doubling':
            self.next_threshold *= 2
        elif self.strategy == 'fibonacci':
            self.fib_prev, self.fib_curr = self.fib_curr, self.fib_prev + self.fib_curr
            self.next_threshold = self.fib_curr

    def __str__(self):
        current = self.head
        words = []
        while current:
            words.append(current.data)
            current = current.next
        return str(words)
    
    def delete(self, word):
        if not self.head:
            return False

        if self.head.data == word:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == word:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next

        return False

def load_words_linked_list(filename, strategy):
    linked_list = DynamicDSLinkedList(strategy=strategy)
    word_count = 0
    
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip()
            linked_list.insert(word)
            word_count += 1
            
            if word_count % 1000 == 0:
                print(f"Linked List ({strategy}): Processed {word_count} words. Current size: {linked_list.size}")
    
    return linked_list, word_count

# Main program
filename = 'words_2000.txt'

for strategy in ['incremental', 'doubling', 'fibonacci']:
    print(f"\nRunning with Linked List ({strategy} strategy)")
    linked_list, word_count = load_words_linked_list(filename, strategy)

    print(f"Total words loaded: {word_count}")
    print(f"Final list size: {linked_list.size}")
    print(f"Total time for inserts: {linked_list.insert_time:.4f} seconds")
    print(f"Average insert time: {(linked_list.insert_time / word_count):.8f} seconds")
    print(f"Total comparisons: {linked_list.comparison_count}")
    print(f"Average comparisons per insert: {linked_list.comparison_count / word_count:.2f}")
    print(f"Final threshold: {linked_list.next_threshold}")