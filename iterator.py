from abc import ABC, abstractmethod

# 迭代器接口
class Iterator(ABC):
    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

# 具体迭代器实现
class ConcreteIterator(Iterator):
    def __init__(self, collection):
        self._collection = collection
        self._index = 0

    def has_next(self):
        return self._index < len(self._collection)

    def next(self):
        if self.has_next():
            item = self._collection[self._index]
            self._index += 1
            return item
        raise StopIteration
    
    def is_first(self):
        return self._index==0