import unittest
from point import Point, Line, Fibonacci

# FILE: test_point.py


class TestPoint(unittest.TestCase):
  def test_point_init(self):
    p = Point(3, 4)
    self.assertEqual(p.x, 3)
    self.assertEqual(p.y, 4)

  def test_point_toString(self):
    p = Point(3, 4)
    self.assertEqual(p.toString(), "(3, 4)")

  def test_point_distance(self):
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    self.assertEqual(p1.distance(p2), 5.0)

class TestLine(unittest.TestCase):
  def test_line_init(self):
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    line = Line(p1, p2)
    self.assertEqual(line.p1, p1)
    self.assertEqual(line.p2, p2)

  def test_line_toString(self):
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    line = Line(p1, p2)
    self.assertEqual(line.toString(), "((0, 0), (3, 4))")

  def test_line_length(self):
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    line = Line(p1, p2)
    self.assertEqual(line.length(), 5.0)

  def test_line_slope(self):
    p1 = Point(0, 0)
    p2 = Point(3, 3)
    line = Line(p1, p2)
    self.assertEqual(line.slope(), 1.0)

  def test_line_y_intercept(self):
    p1 = Point(0, 0)
    p2 = Point(3, 3)
    line = Line(p1, p2)
    self.assertEqual(line.y_intercept(), 0.0)

  def test_line_x_intercept(self):
    p1 = Point(0, 0)
    p2 = Point(3, 3)
    line = Line(p1, p2)
    self.assertEqual(line.x_intercept(), 0.0)

  def test_line_midpoint(self):
    p1 = Point(0, 0)
    p2 = Point(4, 4)
    line = Line(p1, p2)
    midpoint = line.midpoint()
    self.assertEqual(midpoint.x, 2)
    self.assertEqual(midpoint.y, 2)

class TestFibonacci(unittest.TestCase):
  def test_fibonacci_init(self):
    fib = Fibonacci(5)
    self.assertEqual(fib.n, 5)

  def test_fibonacci_calculate_zero(self):
    fib = Fibonacci(0)
    self.assertEqual(fib.calculate(), [])

  def test_fibonacci_calculate_one(self):
    fib = Fibonacci(1)
    self.assertEqual(fib.calculate(), [0])

  def test_fibonacci_calculate_two(self):
    fib = Fibonacci(2)
    self.assertEqual(fib.calculate(), [0, 1])

  def test_fibonacci_calculate_five(self):
    fib = Fibonacci(5)
    self.assertEqual(fib.calculate(), [0, 1, 1, 2, 3])

if __name__ == '__main__':
  unittest.main()