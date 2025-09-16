class LogMixin:
    def __init__(self, **kwargs):
        print("LogMixin init")
        super().__init__(**kwargs)

class Person:
    def __init__(self, **kwargs):
        self.name = "Marry"
        super().__init__(**kwargs)

class Student(LogMixin, Person):
    def __init__(self, **kwargs):
        print("Student init")
        super().__init__(**kwargs)

s = Student()
p = Person()
l = LogMixin()
# Order: Student -> LogMixin -> Person -> object
