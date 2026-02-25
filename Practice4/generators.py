# --- ОПРЕДЕЛЕНИЕ ГЕНЕРАТОРОВ ---

# 1. Квадраты чисел от 1 до N
def squares_generator(n):
    for i in range(1, n + 1):
        yield i * i

# 2. Четные числа от 0 до N
def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i

# 3. Числа, делящиеся на 3 и 4 (т.е. на 12)
def divisible_generator(n):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. Квадраты в диапазоне от A до B
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

# 5. Обратный отсчет от N до 0
def countdown(n):
    for i in range(n, -1, -1):
        yield i


# --- ТЕСТОВЫЙ БЛОК ---

def run_tests():
    try:
        print("=== Запуск тестов генераторов ===\n")

        # Тест 1
        print("Задание 1: Квадраты от 1 до N")
        n1 = int(input("Введите N: "))
        print("Результат:", list(squares_generator(n1)))
        print("-" * 30)

        # Тест 2
        print("Задание 2: Четные числа через запятую")
        n2 = int(input("Введите N: "))
        result = [str(num) for num in even_generator(n2)]
        print("Результат:", ",".join(result))
        print("-" * 30)

        # Тест 3
        print("Задание 3: Делятся на 3 и 4")
        n3 = int(input("Введите N: "))
        print("Результат:", end=" ")
        for num in divisible_generator(n3):
            print(num, end=" ")
        print("\n" + "-" * 30)

        # Тест 4
        print("Задание 4: Квадраты от A до B")
        a = int(input("Введите начало (A): "))
        b = int(input("Введите конец (B): "))
        print("Результат:")
        for sq in squares(a, b):
            print(sq, end=" ")
        print("\n" + "-" * 30)

        # Тест 5
        print("Задание 5: Обратный отсчет")
        n5 = int(input("Введите N: "))
        print("Результат:")
        for num in countdown(n5):
            print(num, end=" ")
        print("\n\nВсе тесты завершены!")

    except ValueError:
        print("\nОшибка: Пожалуйста, вводите только целые числа.")

if __name__ == "__main__":
    run_tests()