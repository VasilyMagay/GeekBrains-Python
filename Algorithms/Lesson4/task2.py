from math import sqrt
import cProfile


def prime_number_sqrt(n):

    # Если число n не является простым, оно может быть разделено на два фактора a и b:
    #     n = a * b
    # Если бы и a и b были больше квадратного корня из n, то a * b было бы больше, чем n.
    # Таким образом, хотя бы один из этих факторов должен быть меньше или равен квадратному корню из n,
    # и если мы не можем найти какие-либо факторы, меньшие или равные квадратному корню, n должно быть простым.

    i = 2
    while i <= sqrt(n):
        if n % i == 0:
            return False
        i += 1
    return True


# Поиск n-ого простого числа вторым способом
def prime_sqrt(n):
    counter = 0
    i = 2
    while True:
        counter += 1 if prime_number_sqrt(i) else 0
        if counter == n:
            break
        i += 1
    return i


def prime_eratosthene(f):

    def _to_sieve(n):  # Решето Эратосфена

        n0 = len(sieve)  # n0 - кол-во обработанных натуральных чисел
        for i in range(n0, n):
            sieve.append(i)

        for i in range(2, n):
            if sieve[i] != 0:
                j = i + i
                while j < n:
                    if j >= n0:
                        sieve[j] = 0
                    j += i

        return [i for i in sieve if i != 0]

    sieve = [0, 0]
    n = 2
    res = 0
    while True:
        primes = _to_sieve(n)
        if len(primes) >= f:
            res = primes[f-1]
            break
        n *= 2

    return res


# i = 1000
# prime = prime_eratosthene(i)
# print(f'Решето Эратосфена, {i} - {prime}')
# prime = prime_sqrt(i)
# print(f'Квадратный корень, {i} - {prime}')

# prime_eratosthene -----------------------------------------------------------------

# cProfile.run('prime_eratosthene(200)')  # 10, 100, 200

#   10    0.000    0.000    0.000    0.000 {built-in method builtins.len}      - 10
#   30    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects} - 10

#   20    0.000    0.000    0.000    0.000 {built-in method builtins.len}      - 100
# 1022    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects} - 100

#   22    0.000    0.000    0.000    0.000 {built-in method builtins.len}      - 200
# 2046    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects} - 200


# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(10)"
# 100 loops, best of 3: 20.7 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(20)"
# 100 loops, best of 3: 76.4 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(40)"
# 100 loops, best of 3: 152 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(80)"
# 100 loops, best of 3: 322 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(160)"
# 100 loops, best of 3: 684 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(100)"
# 100 loops, best of 3: 712 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_eratosthene(1000)"
# 100 loops, best of 3: 6.38 msec per loop


# prime_sqrt --------------------------------------------------------------------------

# cProfile.run('prime_sqrt(200)')  # 10, 100, 200

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)      - 10
#     28    0.000    0.000    0.000    0.000 task2.py:5(prime_number_sqrt)
#     54    0.000    0.000    0.000    0.000 {built-in method math.sqrt}

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)      - 100
#    540    0.001    0.000    0.001    0.000 task2.py:5(prime_number_sqrt)
#   2437    0.000    0.000    0.000    0.000 {built-in method math.sqrt}

# ncalls  tottime  percall  cumtime  percall filename:lineno(function)      - 200
#   1222    0.002    0.000    0.003    0.000 task2.py:5(prime_number_sqrt)
#   7133    0.001    0.000    0.001    0.000 {built-in method math.sqrt}


# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(10)"
# 100 loops, best of 3: 18.8 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(20)"
# 100 loops, best of 3: 58.8 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(40)"
# 100 loops, best of 3: 177 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(80)"
# 100 loops, best of 3: 526 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(160)"
# 100 loops, best of 3: 1.58 msec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(100)"
# 100 loops, best of 3: 798 usec per loop

# python -m timeit -n 100 -s "import task2" "task2.prime_sqrt(1000)"
# 100 loops, best of 3: 26 msec per loop


# Выводы:
# 1. Скорость алгоритма с решетом Эратосфена примерно в 1,5-2 раза быстрее, чем алгоритм с квадратным корнем.
# 2. Сложность алгоритма с решетом O(n): при увеличении n в 100 раз время увеличилось в 300 раз
# 3. Сложность алгоритма с квадратным корнем также O(n).
