import heapq
from collections import defaultdict, Counter

class HuffmanCoding:
    def __init__(self):
        self.huffman_dict = {}

    def build_tree(self, message):
        frequency = Counter(message)
        heap = [[weight, [char, ""]] for char, weight in frequency.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        self.huffman_dict = {a[0]: a[1] for a in heapq.heappop(heap)[1:]}

    def encode(self, message):
        if not self.huffman_dict:
            self.build_tree(message)
        return ''.join(self.huffman_dict[char] for char in message)