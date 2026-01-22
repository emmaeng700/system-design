# TinyKey‑Value‑DB

A **durable key–value store** that fits in three files:

| File | Purpose |
|------|---------|
| `hash_index.py` | In‑memory chained‑bucket hash‑map (`MyHashMap`)  |
| `wal.py`        | Minimal implementation of a  **write‑ahead log (WAL)** that journals every mutating operation and supports checkpoints. |
| `database.py`   | `DurableHashMap` wrapper that glues the WAL to the hash index, handles crash recovery, and exposes a simple durable API. |


---

## 1  Quick start

```bash
$ python3 database.py
20    # ← prints the value for key 2 after a put/remove sequence
```
```
┌───────────────────────── app / user code ─────────────────────────┐
│                                                                   │
│   ┌─────────────── DurableHashMap ────────────────┐               │
│   │               high‑level API                  │               │
│   └───────────────┬───────────────────────────────┘               │
│                   │   WAL‑FIRST discipline                        │
│   ┌───────────────▼───────────────────────────────┐               │
│   │         WriteAheadLog (WAL) – durability layer│               │
│   └───────────────┬───────────────────────────────┘               │
│                   │   replays log on open()                       │
│   ┌───────────────▼───────────────────────────────┐               │
│   │              MyHashMap – pure in‑mem table    │               │
│   └───────────────────────────────────────────────┘               │
└───────────────────────────────────────────────────────────────────┘
```
