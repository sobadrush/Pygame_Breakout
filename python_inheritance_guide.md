# Python 繼承指南

## 什麼是繼承？

繼承（Inheritance）是物件導向(object-oriented)程式設計中的一個重要概念，允許一個類別（子類別）繼承另一個類別（父類別）的屬性和方法。這樣可以實現程式碼的重用和階層結構。

> Ｑ1：什麼是物件導向？

## 基本語法

### 定義子類別

```python
class ParentClass:
    def __init__(self):
        self.value = 10

    def method(self):
        print("Parent method")

class ChildClass(ParentClass):
    def __init__(self):
        super().__init__()  # 呼叫父類別的 __init__
        self.child_value = 20

    def child_method(self):
        print("Child method")
```

### 使用繼承

```python
child = ChildClass()
print(child.value)  # 10 (從父類別繼承)
print(child.child_value)  # 20 (子類別自己的屬性)
child.method()  # 呼叫父類別的方法
child.child_method()  # 呼叫子類別的方法
```

## 方法覆寫（Method Overriding）

子類別可以覆寫父類別的方法，以提供自己的實作：

```python
class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):  # 覆寫父類別的方法
        print("Woof!")

class Cat(Animal):
    def speak(self):  # 覆寫父類別的方法
        print("Meow!")

dog = Dog()
cat = Cat()
dog.speak()  # Woof!
cat.speak()  # Meow!
```

## super() 函數

`super()` 用於呼叫父類別的方法：

```python
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # 呼叫父類別的 __init__
        self.age = age
```

## 多重繼承

Python 支援多重繼承，一個類別可以繼承多個父類別：

```python
class A:
    def method_a(self):
        print("Method A")

class B:
    def method_b(self):
        print("Method B")

class C(A, B):  # 繼承 A 和 B
    def method_c(self):
        print("Method C")

c = C()
c.method_a()  # Method A
c.method_b()  # Method B
c.method_c()  # Method C
```

> Q2: 多重繼承會導致什麼問題？
A: 多重繼承可能導致「菱形繼承」問題（Diamond Problem），即子類別同時繼承自多個父類別，這些父類別又有共同的祖先，可能會造成方法解析順序混亂。

> Q3: 為什麼要有繼承？

## 在 Breakout 遊戲中的應用

在本專案中，所有核心類別都繼承自 `pygame.sprite.Sprite`：

```python
class Paddle(pygame.sprite.Sprite):  # 繼承 Sprite
    def __init__(self):
        super().__init__()  # 初始化父類別
        # 子類別特定的初始化

class Ball(pygame.sprite.Sprite):  # 繼承 Sprite
    # ...

class Brick(pygame.sprite.Sprite):  # 繼承 Sprite
    # ...
```

這樣，`Paddle`、`Ball` 和 `Brick` 都自動獲得了 Sprite 的所有功能，如位置管理、圖像渲染等，並可以添加自己的行為。

## 繼承的優點

1. **程式碼重用**：避免重複撰寫相似的程式碼
2. **階層結構**：建立有意義的類別關係
3. **多型性**：子類別可以有不同的行為
4. **擴展性**：容易添加新功能

## 注意事項

- **方法解析順序 (MRO)**：在多重繼承中，Python 使用 C3 線性化演算法決定方法呼叫順序
- **避免過度繼承**：過深的繼承階層可能導致複雜性
- **組合 vs 繼承**：有時使用組合（has-a 關係）比繼承（is-a 關係）更合適

## 常見問題

### Q: 如何檢查一個物件是否是某個類別的實例？
A: 使用 `isinstance(obj, Class)` 或 `issubclass(Child, Parent)`。

### Q: 如何防止方法被覆寫？
A: Python 沒有真正的私有方法，但可以使用雙底線前綴（如 `__private_method`）來實現名稱混淆。

### Q: 什麼是抽象基類？
A: 使用 `abc` 模組可以定義抽象基類，要求子類別實作特定方法。

---

*這個指南基於 Python 官方文件。如需更多詳細資訊，請參考 [Python 繼承文件](https://docs.python.org/3/tutorial/classes.html#inheritance)。*