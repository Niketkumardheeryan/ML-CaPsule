def add_numbers(a, b):
    return a + b


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def is_prime(num):

    if num <= 1:
        return False

    for i in range(2, int(num ** 0.5) + 1):

        if num % i == 0:
            return False

    return True


def reverse_string(text):
    return text[::-1]


def count_vowels(sentence):

    vowels = "aeiouAEIOU"

    return sum(
        1 for char in sentence
        if char in vowels
    )


def find_max(numbers):

    maximum = numbers[0]

    for num in numbers:

        if num > maximum:
            maximum = num

    return maximum


def fibonacci(n):

    sequence = [0, 1]

    while len(sequence) < n:

        sequence.append(
            sequence[-1] + sequence[-2]
        )

    return sequence


def remove_duplicates(items):
    return list(set(items))


def calculate_average(values):

    if not values:
        return 0

    return sum(values) / len(values)


def sort_dictionary_by_value(data):

    return dict(
        sorted(
            data.items(),
            key=lambda item: item[1]
        )
    )


def count_words(paragraph):

    words = paragraph.split()

    return len(words)


def celsius_to_fahrenheit(celsius):

    return (celsius * 9/5) + 32


def palindrome_check(word):

    cleaned = word.lower()

    return cleaned == cleaned[::-1]


def merge_lists(list1, list2):

    return list1 + list2


def find_even_numbers(numbers):

    return [
        num for num in numbers
        if num % 2 == 0
    ]