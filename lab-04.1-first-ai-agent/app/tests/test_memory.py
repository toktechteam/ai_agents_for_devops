from memory import Memory


def test_memory_store_and_get():
    m = Memory()
    m.remember("key1", 123)
    assert m.get("key1") == 123
    assert m.get("missing", "default") == "default"


def test_memory_dump():
    m = Memory()
    m.remember("a", 1)
    m.remember("b", 2)
    dump = m.dump()
    assert dump == {"a": 1, "b": 2}
