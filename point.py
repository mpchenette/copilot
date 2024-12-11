
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def toString(self):
    return f"({self.x}, {self.y})"
  
  def distance(self, other):
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

class Line:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
  
  def toString(self):
    return f"({self.p1.toString()}, {self.p2.toString()})"
  
  def length(self):
    return self.p1.distance(self.p2)
  
  def slope(self):
    return (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
  
  def y_intercept(self):
    return self.p1.y - self.slope() * self.p1.x
  
  def x_intercept(self):
    return -self.y_intercept() / self.slope()
  
  def midpoint(self):
    return Point((self.p1.x + self.p2.x) / 2, (self.p1.y + self.p2.y) / 2)

class Fibonacci:
  def __init__(self, n):
    self.n = n
  
  def calculate(self):
    if self.n <= 0:
      return []
    elif self.n == 1:
      return [0]
    elif self.n == 2:
      return [0, 1]
    else:
      fib = [0, 1]
      for i in range(2, self.n):
        fib.append(fib[i-1] + fib[i-2])
      return fib