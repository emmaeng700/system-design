from hash_index import MyHashMap
from wal import WriteAheadLog

class DurableHashMap:
    """
    Thin wrapper that marries MyHashMap + WriteAheadLog.
    Call .close() when finished.
    """
    def __init__(self, wal_path="wal/hashmap.wal"):
        self.wal = WriteAheadLog(wal_path)
        self.map = MyHashMap()
        
        for rec in self.wal.replay():
            if rec["op"] == "put":
                self.map.put(rec["key"], rec["val"])
            else:
                self.map.remove(rec["key"])

    def put(self, key: int, value: int):
        self.wal.log_put(key, value)     
        self.map.put(key, value)         

    def remove(self, key: int):
        self.wal.log_remove(key)         
        self.map.remove(key)    
        
        
    def get(self, key: int) -> int:
        return self.map.get(key)

    def close(self):
        self.wal.close()

    def checkpoint(self):
        self.wal.checkpoint(self)

    def dump_as_list(self):
        """
        Return the current contents as list of (key,value) pairs.
        Order is not important for restore speed.
        """
        all_items = []
        for bucket in self.map.hashMap:
            curr = bucket.bucket.next
            while curr:
                k, v = curr.val
                all_items.append((k, v))
                curr = curr.next
        return all_items

if __name__ == "__main__":
    dh = DurableHashMap()
    dh.put(1, 10)
    dh.put(2, 20)
    dh.remove(1)
    print(dh.get(2))   
    dh.checkpoint()    
    dh.close()
  