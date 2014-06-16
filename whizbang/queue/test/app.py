from queue import async

@async
def add(a, b):
    return a + b

def main():
    result = add.delay(3, 4, want_results=True)
    print result.get()
    print add(3, 4)

if __name__ == '__main__':
    main()
