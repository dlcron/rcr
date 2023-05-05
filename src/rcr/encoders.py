import heapq
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional


@dataclass(order=True)
class Command:
    name: str = field(compare=False)
    count: int = field(compare=True)
    left: Optional["Command"] = field(default=None, compare=False)
    right: Optional["Command"] = field(default=None, compare=False)

    @property
    def is_leaf(self: "Command") -> bool:
        return self.left is None and self.right is None


def encode(commands: list[str]) -> dict[str, str]:
    """Encode a list of commands into a dictionary of RCR codes.

    Steps:
    1. Count the number of occurrences of each command.
    2. Create a min-heap from that.
    3. Replace two smallest items, with a new item that has the sum of their counts.
    4. New item is a tree node, with the two replaced items as its children.
    5. Repeat step 3 until there is only one item left in the heap.
    6. Reconstruct the encoding from the tree. If we go left, append 0, if we go right append 1.
    """
    counter = Counter(commands)
    heap = [Command(name=name, count=count) for name, count in counter.items()]
    heapq.heapify(heap)

    if len(heap) == 1:  # handle just one command case
        return {heap[0].name: "0"}

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(
            heap,
            Command(name="-", count=left.count + right.count, left=left, right=right),
        )

    def collect(node: Command) -> dict[str, str]:
        def _traverse(node: Command, path: str, result: dict[str, str]) -> None:
            if node.is_leaf:
                result[node.name] = path
            if node.left:
                _traverse(node.left, path + "0", result)
            if node.right:
                _traverse(node.right, path + "1", result)

        result: dict[str, str] = {}
        _traverse(node, "", result)
        return result

    if not heap:
        return {}

    return collect(heapq.heappop(heap))
