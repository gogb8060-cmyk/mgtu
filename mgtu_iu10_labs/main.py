# Лабораторная работа №3. Линейные списки.
# Вариант: 24. Студент: Темирезов Р.Б., группа ИУ10-38

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# ============ ЗАДАНИЕ 1: 6 версий списка ============

# Версия 1: ручное связывание узлов
print("=== Задание 1: Версия 1 (ручное связывание) ===")
head = Node(1)
head.next = Node(2)
head.next.next = Node(3)

current = head
while current:
    print(current.data, end=" -> ")
    current = current.next
print("None\n")


# Версия 2: базовый контейнер
class LinkedListV2:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")


print("=== Задание 1: Версия 2 (базовый контейнер) ===")
ll2 = LinkedListV2()
ll2.append(10)
ll2.append(20)
ll2.display()
print()


# Версия 3: добавляем tail и prepend
class LinkedListV3(LinkedListV2):
    def __init__(self):
        super().__init__()
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        self.tail = new_node

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        if not self.tail:
            self.tail = new_node


print("=== Задание 1: Версия 3 (+ tail и prepend) ===")
ll3 = LinkedListV3()
ll3.append(10)
ll3.append(20)
ll3.prepend(5)
ll3.display()
print()


# Версия 4: поиск и удаление
class LinkedListV4(LinkedListV3):
    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                return True
            current = current.next
        return False

    def delete(self, key):
        current = self.head
        previous = None
        while current:
            if current.data == key:
                if previous:
                    previous.next = current.next
                    if current == self.tail:
                        self.tail = previous
                else:
                    self.head = current.next
                    if not self.head:
                        self.tail = None
                return True
            previous = current
            current = current.next
        return False


print("=== Задание 1: Версия 4 (+ search и delete) ===")
ll4 = LinkedListV4()
ll4.append(10)
ll4.append(20)
ll4.append(30)
print(f"Поиск 20: {ll4.search(20)}")
print(f"Поиск 99: {ll4.search(99)}")
ll4.delete(20)
ll4.display()
print()


# Версия 5: итератор и счётчик (задание 5)
class LinkedListV5(LinkedListV4):
    def __init__(self):
        super().__init__()
        self._length = 0

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        if not self.tail:
            self.tail = new_node
        self._length += 1

    def delete(self, key):
        current = self.head
        previous = None
        while current:
            if current.data == key:
                if previous:
                    previous.next = current.next
                    if current == self.tail:
                        self.tail = previous
                else:
                    self.head = current.next
                    if not self.head:
                        self.tail = None
                self._length -= 1
                return True
            previous = current
            current = current.next
        return False

    def __len__(self):
        return self._length

    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        data = self._current.data
        self._current = self._current.next
        return data


print("=== Задание 5: Версия 5 (итератор и len) ===")
ll5 = LinkedListV5()
ll5.append("Python")
ll5.append("JS")
ll5.append("C++")
print(f"Длина списка: {len(ll5)}")
print("Обход через for:")
for lang in ll5:
    print(f"  {lang}")
print()


# Версия 6: финальная (reverse, sort, индив. задание)
class LinkedListV6(LinkedListV5):
    def __repr__(self):
        elements = [str(x) for x in self]
        return " -> ".join(elements) + " -> None"

    def __getitem__(self, index):
        if index < 0:
            index = self._length + index
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def reverse(self):
        if not self.head or not self.head.next:
            return
        prev = None
        current = self.head
        self.tail = current
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sort(self):
        if not self.head or not self.head.next:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next

    def remove_elements_more_than_two(self):
        if not self.head:
            return
        counts = {}
        current = self.head
        while current:
            if current.data in counts:
                counts[current.data] += 1
            else:
                counts[current.data] = 1
            current = current.next

        previous = None
        current = self.head
        new_tail = None
        while current:
            if counts[current.data] > 2:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                self._length -= 1
            else:
                previous = current
                new_tail = current
            current = current.next
        self.tail = new_tail


# ============ ЗАДАНИЕ 2: reverse ============
print("=== Задание 2: reverse ===")
ll6 = LinkedListV6()
ll6.append(1)
ll6.append(2)
ll6.append(3)
ll6.append(4)
print("Исходный список:")
print(ll6)

ll6.reverse()
print("После reverse:")
print(ll6)
print()


# ============ ЗАДАНИЕ 3: sort ============
print("=== Задание 3: sort ===")
ll7 = LinkedListV6()
ll7.append(5)
ll7.append(2)
ll7.append(8)
ll7.append(1)
ll7.append(4)
print("Исходный список:")
print(ll7)

ll7.sort()
print("После sort:")
print(ll7)
print()


# ============ ЗАДАНИЕ 4: индивидуальное (вариант 24) ============
print("=== Задание 4: индивидуальное задание (вариант 24) ===")
print("Удалить элементы, встречающиеся более 2 раз\n")

ll8 = LinkedListV6()
ll8.append(1)
ll8.append(2)
ll8.append(2)
ll8.append(2)
ll8.append(3)
ll8.append(3)
ll8.append(4)

print("Исходный список:")
print(ll8)
print(f"Длина: {len(ll8)}")

ll8.remove_elements_more_than_two()
print("\nПосле удаления элементов, встречающихся более 2 раз:")
print(ll8)
print(f"Длина: {len(ll8)}")
print()

print("=== Все задания выполнены ===")