class Animal:
  def __init__(self):
    self.weight = 50
  
  def speak(self):
    print("wa wa wa")
    
########################### 
    
class Horse(Animal):
  def __init__(self):
    super().__init__()
  
  def speak(self):
    print("La La La")

###########################

class Donkey(Animal):
  def __init__(self):
    super().__init__()
  
  def speak(self):
    print("ear ear")
    
###########################
    
class Mule(Horse, Donkey):
  def __init__(self):
    super().__init__()
    
  # def speak(self):
  #  print("一齁一齁一齁")
  
###########################

my_mule = Mule()
my_mule.speak()
