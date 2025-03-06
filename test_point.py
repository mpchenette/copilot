import unittest
from point import Fibonacci
from point import Point, Line

class TestFibonacci(unittest.TestCase):
  def test_fibonacci_zero(self):
    fib = Fibonacci(0)
    self.assertEqual(fib.calculate(), [])

  def test_fibonacci_one(self):
    fib = Fibonacci(1)
    self.assertEqual(fib.calculate(), [0])

  def test_fibonacci_two(self):
    fib = Fibonacci(2)
    self.assertEqual(fib.calculate(), [0, 1])

  def test_fibonacci_five(self):
    fib = Fibonacci(5)
    self.assertEqual(fib.calculate(), [0, 1, 1, 2, 3])

  def test_fibonacci_ten(self):
    fib = Fibonacci(10)
    self.assertEqual(fib.calculate(), [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
    class TestPoint(unittest.TestCase):
      def test_point_creation(self):
        p = Point(3, 4)
        self.assertEqual(p.x, 3)
        self.assertEqual(p.y, 4)

      def test_point_to_string(self):
        p = Point(3, 4)
        self.assertEqual(p.toString(), "(3, 4)")

      def test_point_distance(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        self.assertEqual(p1.distance(p2), 5.0)

    class TestLine(unittest.TestCase):
      def test_line_creation(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        line = Line(p1, p2)
        self.assertEqual(line.p1, p1)
        self.assertEqual(line.p2, p2)

      def test_line_to_string(self):
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
        p2 = Point(3, 4)
        line = Line(p1, p2)
        self.assertEqual(line.slope(), 4/3)

      def test_line_y_intercept(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        line = Line(p1, p2)
        self.assertEqual(line.y_intercept(), 0)

      def test_line_x_intercept(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        line = Line(p1, p2)
        self.assertEqual(line.x_intercept(), 0)

      def test_line_midpoint(self):
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        line = Line(p1, p2)
        midpoint = line.midpoint()
        self.assertEqual(midpoint.x, 1.5)
        self.assertEqual(midpoint.y, 2)
if __name__ == '__main__':
  unittest.main()