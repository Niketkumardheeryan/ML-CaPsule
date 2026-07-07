# Adjacency Matrix representation in Python
class Graph(object):


 # Initialize the matrix
    def __init__(self, size):
        self.adjMatrix = []
        self.size = size
        for i in range(size):
            self.adjMatrix.append([0 for i in range(size)])
        


 # Add edges
    def add_edge(self, v1, v2):
        if v1 == v2:
            print("Same vertex %d and %d" % (v1, v2))
        self.adjMatrix[v1][v2] = 1
        


 # Remove edges
    def remove_edge(self, v1, v2):
        if self.adjMatrix[v1][v2] == 0:
            print("No edge between %d and %d" % (v1, v2))
            return
        self.adjMatrix[v1][v2] = 0

        
       

    def __len__(self):
        return self.size


 # Print the matrix
    def print_matrix(self):
        for row in self.adjMatrix:
            for val in row:
                print('{:4}'.format(val),end=''),
            print()



def main():

    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.remove_edge(2, 3)
    g.print_matrix()


if __name__ == '__main__':
 main()