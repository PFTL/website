"""
Module People
=============
Defines two classes, Person and Teacher.
You define a person by supplying a name, for example:

>>> me = Person('My Name')
>>> print(me.name)
My Name

"""
class Person:
    """Class to store a general person information. For example the name."""
    def __init__(self, name):
        """Create a person object by providing a name"""
        self.name = name


class Teacher(Person):
    """Class to store a teacher's information. It subclasses Person."""
    def __init__(self, name, course):
        """Create a teacher object by providing a name and the course it teaches."""
        super().__init__(name)
        self.course = course

    def get_course(self):
        """Get the course that the teacher teaches."""
        return self.course

    def set_course(self, new_course):
        """Set the course that the teacher teaches"""
        self.course = new_course