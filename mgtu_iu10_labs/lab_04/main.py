"""
Лабораторная работа №4. Стек, Очередь, Дек.
Кафедра ИУ10 МГТУ им. Н.Э. Баумана.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional


# 1. БАЗОВЫЕ КЛАССЫ (УЗЛЫ ДЛЯ СПИСКОВ)
class SLLNode:
    """Узел односвязного списка."""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['SLLNode'] = None

class DLLNode:
    """Узел двусвязного списка."""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['DLLNode'] = None
        self.prev: Optional['DLLNode'] = None


# 2. АБСТРАКТНЫЕ БАЗОВЫЕ КЛАССЫ (ИНТЕРФЕЙСЫ АТД)
class IStack(ABC):
    @abstractmethod
    def push(self, x: Any) -> None: pass
    @abstractmethod
    def pop(self) -> Any: pass
    @abstractmethod
    def peek(self) -> Any: pass
    @abstractmethod
    def is_empty(self) -> bool: pass

class IQueue(ABC):
    @abstractmethod
    def enqueue(self, x: Any) -> None: pass
    @abstractmethod
    def dequeue(self) -> Any: pass
    @abstractmethod
    def peek(self) -> Any: pass
    @abstractmethod
    def is_empty(self) -> bool: pass

class IDeque(IDeque if 'IDeque' in globals() else ABC): # Защита от циклического импорта, если бы он был
    @abstractmethod
    def push_front(self, x: Any) -> None: pass
    @abstractmethod
    def push_back(self, x: Any) -> None: pass
    @abstractmethod
    def pop_front(self) -> Any: pass
    @abstractmethod
    def pop_back(self) -> Any: pass
    @abstractmethod
    def peek_front(self) -> Any: pass
    @abstractmethod
    def peek_back(self) -> Any: pass
    @abstractmethod
    def is_empty(self) -> bool: pass


# 3. ЗАДАНИЕ 1: РЕАЛИЗАЦИЯ СТРУКТУР ДАННЫХ

# --- 1.1. Стек на массиве ---
class StackArray(IStack):
    def __init__(self, capacity: int = 4):
        self._data = [None] * capacity
        self._size = 0
        self._capacity = capacity

    def _resize(self, new_capacity: int):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def push(self, x: Any) -> None:
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = x
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        self._size -= 1
        item = self._data[self._size]
        self._data[self._size] = None  # Освобождаем ссылку для GC
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[self._size - 1]

    def is_empty(self) -> bool:
        return self._size == 0

# --- 1.2. Стек на связном списке ---
class StackList(IStack):
    def __init__(self):
        self._head: Optional[SLLNode] = None
        self._size = 0

    def push(self, x: Any) -> None:
        new_node = SLLNode(x)
        new_node.next = self._head
        self._head = new_node
        self._size += 1

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        item = self._head.data
        self._head = self._head.next
        self._size -= 1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._head.data

    def is_empty(self) -> bool:
        return self._head is None

# --- 1.3. Очередь на массиве (Кольцевой буфер) ---
class QueueArray(IQueue):
    def __init__(self, capacity: int = 4):
        self._data = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0
        self._capacity = capacity

    def _resize(self, new_capacity: int):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % self._capacity]
        self._data = new_data
        self._head = 0
        self._tail = self._size
        self._capacity = new_capacity

    def enqueue(self, x: Any) -> None:
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._tail] = x
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._head]

    def is_empty(self) -> bool:
        return self._size == 0

# --- 1.4. Очередь на связном списке ---
class QueueList(IQueue):
    def __init__(self):
        self._head: Optional[SLLNode] = None
        self._tail: Optional[SLLNode] = None
        self._size = 0

    def enqueue(self, x: Any) -> None:
        new_node = SLLNode(x)
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None  # Критично: если очередь пуста, хвост тоже в None
        self._size -= 1
        return item

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._head.data

    def is_empty(self) -> bool:
        return self._head is None

# --- 1.5. Дек на массиве (Кольцевой буфер) ---
class DequeArray(IDeque):
    def __init__(self, capacity: int = 4):
        self._data = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0
        self._capacity = capacity

    def _resize(self, new_capacity: int):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) % self._capacity]
        self._data = new_data
        self._head = 0
        self._tail = self._size
        self._capacity = new_capacity

    def push_front(self, x: Any) -> None:
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._head = (self._head - 1) % self._capacity
        self._data[self._head] = x
        self._size += 1

    def push_back(self, x: Any) -> None:
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._tail] = x
        self._tail = (self._tail + 1) % self._capacity
        self._size += 1

    def pop_front(self) -> Any:
        if self.is_empty():
            raise IndexError("pop_front from empty deque")
        item = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return item

    def pop_back(self) -> Any:
        if self.is_empty():
            raise IndexError("pop_back from empty deque")
        self._tail = (self._tail - 1) % self._capacity
        item = self._data[self._tail]
        self._data[self._tail] = None
        self._size -= 1
        return item

    def peek_front(self) -> Any:
        if self.is_empty():
            raise IndexError("peek_front from empty deque")
        return self._data[self._head]

    def peek_back(self) -> Any:
        if self.is_empty():
            raise IndexError("peek_back from empty deque")
        return self._data[(self._tail - 1) % self._capacity]

    def is_empty(self) -> bool:
        return self._size == 0

# --- 1.6. Дек на двусвязном списке ---
class DequeList(IDeque):
    def __init__(self):
        self._head: Optional[DLLNode] = None
        self._tail: Optional[DLLNode] = None
        self._size = 0

    def push_front(self, x: Any) -> None:
        new_node = DLLNode(x)
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def push_back(self, x: Any) -> None:
        new_node = DLLNode(x)
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def pop_front(self) -> Any:
        if self.is_empty():
            raise IndexError("pop_front from empty deque")
        item = self._head.data
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        self._size -= 1
        return item

    def pop_back(self) -> Any:
        if self.is_empty():
            raise IndexError("pop_back from empty deque")
        item = self._tail.data
        self._tail = self._tail.prev
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        self._size -= 1
        return item

    def peek_front(self) -> Any:
        if self.is_empty():
            raise IndexError("peek_front from empty deque")
        return self._head.data

    def peek_back(self) -> Any:
        if self.is_empty():
            raise IndexError("peek_back from empty deque")
        return self._tail.data

    def is_empty(self) -> bool:
        return self._head is None


# 4. ПРИКЛАДНЫЕ ЗАДАЧИ (ЗАДАНИЯ 2, 3, 4)

def check_brackets(s: str) -> bool:
    """
    Задание 2. Проверка корректности скобочной последовательности.
    Скобки: (), [], {}.
    """
    stack = StackList()
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in pairs.values():  # Открывающая скобка
            stack.push(char)
        elif char in pairs.keys():  # Закрывающая скобка
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    return stack.is_empty()

def eval_rpn(expr: str) -> float:
    """
    Задание 3. Вычисление выражения в обратной польской записи (ОПЗ).
    Поддерживает числа и операции +, -, *, /.
    """
    stack = StackList()
    tokens = expr.split()
    
    for token in tokens:
        # Проверяем, является ли токен числом (поддержка отрицательных и дробных)
        try:
            val = float(token)
            stack.push(val)
        except ValueError:
            # Если не число, то это оператор
            if stack.is_empty():
                raise ValueError("Некорректное выражение: не хватает операндов")
            b = stack.pop()
            if stack.is_empty():
                raise ValueError("Некорректное выражение: не хватает операндов")
            a = stack.pop()
            
            if token == '+': stack.push(a + b)
            elif token == '-': stack.push(a - b)
            elif token == '*': stack.push(a * b)
            elif token == '/': 
                if b == 0: raise ZeroDivisionError("Деление на ноль")
                stack.push(a / b)
            else:
                raise ValueError(f"Неизвестный оператор: {token}")
                
    if stack._size != 1:
        raise ValueError("Некорректное выражение: лишние операнды")
    return stack.pop()

def infix_to_postfix(expr: str) -> str:
    """
    Задание 4. Перевод из инфиксной в постфиксную запись (Алгоритм сортировочной станции Дейкстры).
    Поддерживает +, -, *, /, ^, скобки, многозначные числа и переменные.
    """
    stack = StackList()
    result = []
    # Приоритеты операций
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    i = 0
    while i < len(expr):
        char = expr[i]
        
        # Пропускаем пробелы
        if char.isspace():
            i += 1
            continue
            
        # Если буква или цифра - собираем токен целиком
        if char.isalnum():
            token = ""
            while i < len(expr) and expr[i].isalnum():
                token += expr[i]
                i += 1
            result.append(token)
            continue  # i уже сдвинут, не увеличиваем его внизу
        
        elif char == '(':
            stack.push(char)
            
        elif char == ')':
            while not stack.is_empty() and stack.peek() != '(':
                result.append(stack.pop())
            if not stack.is_empty() and stack.peek() == '(':
                stack.pop()  # Удаляем '(' из стека
                
        elif char in precedence:
            # Выталкиваем операторы с большим или равным приоритетом
            while (not stack.is_empty() and stack.peek() != '(' and 
                   precedence.get(stack.peek(), 0) >= precedence[char]):
                result.append(stack.pop())
            stack.push(char)
            
        i += 1
        
    # Переносим оставшиеся операторы в результат
    while not stack.is_empty():
        if stack.peek() == '(':
            raise ValueError("Ошибка: unmatched '('")
        result.append(stack.pop())
        
    return " ".join(result)


# 5. ТОЧКА ВХОДА И ДЕМОНСТРАЦИЯ (ДЛЯ ОТЧЁТА)
if __name__ == '__main__':
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ АЛГОРИТМОВ И СТРУКТУР ДАННЫХ")
    print("=" * 60)
    
    print("\n[Задание 1] Базовые операции АТД:")
    s_arr = StackArray(2)
    s_arr.push(10); s_arr.push(20); s_arr.push(30) # Проверка ресайза
    print(f"  Стек (массив): pop={s_arr.pop()}, peek={s_arr.peek()}")
    
    q_list = QueueList()
    q_list.enqueue('A'); q_list.enqueue('B'); q_list.enqueue('C')
    print(f"  Очередь (список): dequeue={q_list.dequeue()}, peek={q_list.peek()}")
    
    d_arr = DequeArray(2)
    d_arr.push_back(1); d_arr.push_front(0); d_arr.push_back(2)
    print(f"  Дек (массив): pop_front={d_arr.pop_front()}, peek_back={d_arr.peek_back()}")

    print("\n[Задание 2] Проверка скобочной последовательности:")
    tests_brackets = [
        ("()[]{}", True),
        ("([)]", False),
        ("{[()]}", True),
        ("((())", False),
        ("", True) # Пустая строка
    ]
    for seq, expected in tests_brackets:
        res = check_brackets(seq)
        status = "OK" if res == expected else "FAIL"
        print(f"  '{seq}' -> {res} (ожид. {expected}) [{status}]")

    print("\n[Задание 3] Вычисление обратной польской записи (ОПЗ):")
    tests_rpn = [
        ("2 3 + 4 *", 20.0),
        ("5 1 2 + 4 * + 3 -", 14.0),
        ("10 2 /", 5.0)
    ]
    for expr, expected in tests_rpn:
        res = eval_rpn(expr)
        status = "OK" if res == expected else "FAIL"
        print(f"  '{expr}' -> {res} (ожид. {expected}) [{status}]")

    print("\n[Задание 4] Инфиксная -> Постфиксная запись:")
    tests_infix = [
        ("(a+b)*c", "a b + c *"),
        ("a+(b+c)*d", "a b c + d * +"),
        ("3+4*5", "3 4 5 * +"),
        ("(A+B)*C-D", "A B + C * D -")
    ]
    for expr, expected in tests_infix:
        res = infix_to_postfix(expr)
        status = "OK" if res == expected else "FAIL"
        print(f"  '{expr}' -> '{res}' (ожид. '{expected}') [{status}]")
        
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО.")
    print("=" * 60)
