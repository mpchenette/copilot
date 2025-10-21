# class point that represents a point in 3D space, should have x, y, and z coordinates
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # to string function
    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"
    
    # distance function that calculates the distance between two points
    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)**0.5

    # calculate the average distance between a point and a list of points
    def average_distance(self, points):
        total_distance = 0
        for point in points:
            total_distance += self.distance(point)
        return total_distance / len(points) if points else 0