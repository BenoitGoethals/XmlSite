class Robot:

    __potential_physical: float
    __potential_psychic:float
    def __init__(self, name, build_year, lk=0.5, lp=0.5):
        self.name = name
        self.build_year = build_year
        self.__potential_physical = lk
        self.__potential_psychic = lp

    @property
    def condition(self):
        s = self.__potential_physical + self.__potential_psychic
        if s <= -1:
            return "I feel miserable!"
        elif s <= 0:
            return "I feel bad!"
        elif s <= 0.5:
            return "Could be worse!"
        elif s <= 1:
            return "Seems to be okay!"
        else:
            return "Great!"


class Person:
  __name: str
  __forName:str

  def __init__(self,name,forname) -> None:
    self.__name=name
    self.__forName=forname

  @property
  def name(self):
    return self.__name

  def __set_name__(self, owner, name):
    self.__name=name

  @name.setter
  def name(self,name):
    self.__name=name



if __name__ == "__main__":
    x = Robot("Marvin", 1979, 0.2, 0.4)
    y = Robot("Caliban", 1993, -0.4, 0.3)
    print()
    print(y.condition)
    p=Person("fdsfd","ddsfdsf")

    p.name="dsfdsfdsf"
    print(p.name)

