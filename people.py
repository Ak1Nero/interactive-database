from faker import Faker
import faker_edu
import random
import faker
import color

fake = faker.Faker()
#инкапсуляция(модификаторы), наследование, полиморфизм
class Person:
  def __init__(self, name : str, age : int):
    if age >= 150 or age < 0:
      raise ValueError(color.red + f"Invalid age: {age}" + color.reset)
    self.__age = age
    self.__name = name
    self.__adult = (age >= 18)

  def get_age(self):
    return self.__age
  
  def set_age(self, age):
    if 0 < age and age < 150:
      print("OK")
    else:
      raise ValueError(color.red + f"Invalid age: {age}" + color.reset)
    self.__age = age
    self.__adult = (age >= 18)

  def get_name(self):
    return self.__name
  
  def set_name(self, name):
    self.__name = name
    return
  
  def get_adult(self):
    return self.__adult
  
  def str_data(self):
    return (f"ФИО: {self.__name}, Возраст: {self.__age}, " + 
           f"Совершеннолетие: {self.__adult}")
  
  def __str__(self):
    return self.str_data()
  
  def __repr__(self):
    return self.str_data()

class Student(Person):
  def __init__(self, name: str, age: int, facility : str, year : int):
    super().__init__(name, age)

    if year <= 0 or year >= 5:
      raise ValueError(color.red + f"Invalid year: {year}" + color.reset)
    
    self.__facility = facility
    self.__year = year

  def get_facility(self):
    return self.__facility
  
  def set_facility(self, facility):
    self.__facility = facility
    return
  
  def get_year(self):
    return self.__year
  
  def set_year(self, year):
    if year <= 0 or year >= 5:
      raise ValueError(color.red + f"Invalid year: {year}" + color.reset)
    self.__year = year

  def __str__(self):
    return self.str_data()
  
  def str_data(self):
    return (super().str_data() + f", УЗ: {self.__facility}, Курс: {self.__year}")
  
  def __repr__(self):
    return self.str_data()

def FindStudents(L, facility):
    M = []
    for i in L:
        if isinstance(i, Student) and facility == i.get_facility():
            M.append(i)
    return M

class Worker(Person):
  def __init__(self, name : str, age : int, job: str, wage: int):
    super().__init__(name, age)
    if wage < 0:
      raise ValueError(color.red + f"Invalid wage: {wage}" + color.reset)
    self.__job = job
    self.__wage = wage

  def get_job(self):
    return self.__job
  
  def set_job(self, job):
    self.__job = job
    return
  
  def get_wage(self):
    return self.__wage
  
  def set_wage(self, wage):
    self.__wage = wage
    return 
  
  def str_data(self):
    return (super().str_data() + f", Работа: {self.__job}, ЗП: {self.__wage}")
  
  def __repr__(self):
    return self.str_data()

def gen_person():
  name = fake.name()
  age = fake.random_int(0, 100)
  person = Person(name, age)
  return person

def gen_worker():
  person = gen_person()
  job = fake.job()
  wage = fake.random_int(300, 600)
  worker = Worker(person.get_name(), person.get_age(), job, wage)
  return worker

def gen_student():
  person = gen_person()
  year = fake.random_int(1, 4)
  facilities = open("facilities.txt", "r")
  Universities = (facilities.readline()).split()
  facilities.close()
  random_facility = random.randint(0, len(Universities) - 1)
  university = Universities[random_facility]
  student = Student(person.get_name(), person.get_age(), university, year)
  return student

def SortByWage(workers):
  n = len(workers)
  for i in range(n):
    for j in range(0, n - i - 1):
      if workers[j].get_wage() < workers[j + 1].get_wage():
        workers[j], workers[j + 1] = workers[j + 1], workers[j]
  return workers

#print(gen_person())
#def gen_student():
#  fake = Faker()
#  person = gen_person()
#  facility = fake.add_provider(faker_edu.Provider)
#  year = fake.random_int(0, 5)
#  student = Student(person.get_age(), person.get_name(), facility, year)
#  return student

def gen_class():
  number = random.randint(0, 2)
  if number == 0:
    return gen_person()
  if number == 1:
    return gen_worker()
  return gen_student()

def gen_obj_list(length):
  list = []

  if length <= 0:
    raise ValueError(color.red + f"Invalid length: {length}" + color.reset)
  
  for i in range(0, length):
    list.append(gen_class())
  return list

def obj_list_to_file(file_name, obj_list):
  objects = open(file_name, "w" )

  for i in obj_list:
    if isinstance(i,Student):
      objects.write(f"Student;{i.get_name()};{i.get_age()};{i.get_facility()};{i.get_year()} \n")
    elif isinstance(i,Worker):
      objects.write((f"Worker;{i.get_name()};{i.get_age()};{i.get_job()};{i.get_wage()} \n"))
    elif isinstance(i,Person):
      objects.write(f"Person;{i.get_name()};{i.get_age()} \n")

  objects.close()
  return

def file_to_obj_list(file_name):
  objects = open(file_name, "r")
  result = []
  lines = objects.readlines()

  for i in lines:
    f = i.split(";")
    if f[0] == "Person":
      person = Person(f[1], int(f[2]))
      result.append(person)
    elif f[0] == "Student":
      student = Student(f[1], int(f[2]), f[3], int(f[4]))
      result.append(student)
    elif f[0] == "Worker":
      worker = Worker(f[1], int(f[2]), f[3], int(f[4]))
      result.append(worker)

  objects.close()
  return result

if __name__ == "__main__":
  print("Person.py")
  print(Person("Noname", -1))