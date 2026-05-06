while True:
    try:
        height = int(input("Height: "))
        if 1 <= height <= 8:
            break
    except ValueError:
        pass
    print("Enter a valid height")

for i in range(height):
    print(" " * (height - 1 - i), end="")
    print("#" * (i + 1) + "  " + "#" * (i + 1))
