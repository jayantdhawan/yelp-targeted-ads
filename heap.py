"""
https://joernhees.de/blog/2010/07/19/min-heap-in-python/
"""

import heapq

class Heap(object):
    """ A neat min-heap wrapper which allows storing items by priority
        and get the lowest item out first (pop()).
        Also implements the iterator-methods, so can be used in a for
        loop, which will loop through all items in increasing priority order.
        Remember that accessing the items like this will iteratively call
        pop(), and hence empties the heap! """
    
    def __init__(self, size):
        """ create a new min-heap. """
        self._heap = []
        self.size = size
    
    def push(self, priority, item):
        """ Push an item with priority into the heap.
            Priority 0 is the highest, which means that such an item will
            be popped first."""
        if priority < 0:
            return
        heapq.heappush(self._heap, (priority, item))
        if len(self._heap) == self.size + 1:
            heapq.heappop(self._heap)

    def pop(self):
        """ Returns the item with lowest priority. """
        item = heapq.heappop(self._heap) # (prio, item)[1] == item
        return item
    
    def __len__(self):
        return len(self._heap)
    
    def __iter__(self):
        """ Get all elements ordered by asc. priority. """
        return self
    
    def next(self):
        """ Get all elements ordered by their priority (lowest first). """
        try:
            return self.pop()
        except IndexError:
            raise StopIteration

    def get_list(self):
        return self._heap
