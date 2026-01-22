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