def fizzbuzz(n):
    for i in range(1, n+1):
        if i % 3 == 0 and i % 5 == 0:
            print("fizzbuzz")
            continue
        if i % 3 == 0:
            print("fizz")
            continue
        if i % 5 == 0:
            print("buzz")
            continue
        print(f"{i}")

def main():
    fizzbuzz(20)

if __name__ == "__main__":
    main()
