import heapq
from typing import Generic, Tuple, TypeVar


T = TypeVar("T")


class PriorityQueue(Generic[T]):
    
    """

    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.

    Credits: Berkley AI Pacman Project
    
    """

    def __init__(self):
        self.heap: list[Tuple[float, int, T]] = []
        self.count = 0

    def push(self, item: T, priority: float):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self) -> T:
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def isEmpty(self):
        return self.is_empty()

    def update(self, item: T, priority: float):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)
