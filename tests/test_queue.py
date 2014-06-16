from whizbang.queue.queue import async

@async
def add(a, b):
    return a + b

def test_direct_call():
    """Can we still call the function directly (no async functionality)?"""
    assert add(3, 4) == 7
