class Node:
    def __init__(self, val=(-1,-1), next=None):
        self.val = val
        self.next = next

class Bucket:
    def __init__(self):
        self.bucket = Node()
    
    def update(self, key, val):
        curr = self.bucket

        while curr.next:
            if curr.next.val[0] == key:
                curr.next.val = (key, val)
                return
            curr = curr.next

        curr.next = Node((key,val), None)

    def get(self, key):
        curr = self.bucket

        while curr.next:
            if curr.next.val[0] == key:
                return curr.next.val[1]
            else:
                curr = curr.next
        
        return -1
    
    def remove(self, key):
        curr = self.bucket

        while curr.next:
            if curr.next.val[0] == key:
                curr.next = curr.next.next
            else:
                curr = curr.next

class MyHashMap:
    def __init__(self):
        self.size = 2069
        self.hashMap = [Bucket() for _ in range(self.size)]

    def put(self, key: int, value: int) -> None:
        idx = key % self.size
        self.hashMap[idx].update(key, value)

    def get(self, key: int) -> int:
        idx = key % self.size
        return self.hashMap[idx].get(key)

    def remove(self, key: int) -> None:
        idx = key % self.size
        self.hashMap[idx].remove(key)
        


