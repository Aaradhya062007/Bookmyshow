#name=input("Enter your name:")
#print("Hello,"+name)
#fruits=["apple","mango","kids","play"]
#ff=["apple","banana"]
#for fruit in fruits:
#    print(fruit)
def function1(name):
    print("Hello,", name)
function1("girish")
class example:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def greet(self):
        print(f"Hello my name is {self.name} and age is {self.age}")
person1=example("girish",22)
person1.greet()            
            