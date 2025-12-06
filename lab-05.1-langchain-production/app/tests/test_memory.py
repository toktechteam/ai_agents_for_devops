from app.memory import Memory

def test_memory():
    m = Memory()
    m.remember("a", 1)
    assert m.get("a") == 1
    assert m.dump() == {"a": 1}
