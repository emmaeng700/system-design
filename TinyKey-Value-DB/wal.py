import json, time, os, pathlib, tempfile
from hash_index import MyHashMap

class WriteAheadLog:
    """
    Simple newline-delimited JSON WAL.
    Each record is: {"op": "put"|"remove", "key": <int>, "val": <int|None>, "ts": <unix-epoch>}
    """
    def __init__(self, path: str, create_dir=True):
        self.path = pathlib.Path(path)
        if create_dir:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        
        self._fh = self.path.open("a+", buffering=1)  
        self._fh.seek(0, os.SEEK_END)                 

    def _append(self, record: dict):
        self._fh.write(json.dumps(record, separators=(",", ":")) + "\n")
        self._fh.flush()          
        os.fsync(self._fh.fileno())   

    def log_put(self, key: int, value: int):
        self._append({"op": "put", "key": key, "val": value, "ts": time.time()})

    def log_remove(self, key: int):
        self._append({"op": "remove", "key": key, "val": None, "ts": time.time()})

    def replay(self):
        "Yield records in order (used at start-up)."
        self._fh.flush()
        self._fh.seek(0)
        for line in self._fh:
            if not line.strip():
                continue
            yield json.loads(line)

    def checkpoint(self, hashmap: "MyHashMap"):
        """
        Create a snapshot file, then atomically replace the WAL with an empty one.
        Call during a quiet period (or hold a write mutex) so the map is in a
        consistent state.
        """
        snap_path = self.path.with_suffix(".snap")

        with tempfile.NamedTemporaryFile("w", delete=False, dir=str(self.path.parent)) as tmp:
            json.dump(hashmap.dump_as_list(), tmp, separators=(",", ":"))
            tmp.flush()
            os.fsync(tmp.fileno())
            tmp_name = tmp.name
        
        os.replace(tmp_name, snap_path)
        self._fh.close()
        self.path.unlink(missing_ok=True)
        self._fh = self.path.open("a+", buffering=1)

    def close(self):
        self._fh.close()
