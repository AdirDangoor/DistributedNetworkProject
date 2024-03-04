import importlib
import json
import os
import queue
import random
import sys
import numpy
import computer

# a custom priority queue, which puts according to message_format[4] which is the arrival time
class CustomPriorityQueue(queue.PriorityQueue):
    def put(self, message_format):
        super().put((message_format[5], message_format))
    # retrieves the message, without the priority part of the tuple
    def get(self):
        priority, message_format = super().get()
        return message_format

class Initialization:
    '''
    Initialization Class - creates the basic parameters we get from the user in the visualization class
    and then we create the basic base for the simulation to run on
    '''
    #Defualt constructor
    def __init__(self):
        with open('network_variables.json', 'r') as f:
            data = json.load(f)
        self.numberOfComputers = int(data.get('Number of Computers',0))
        self.topologyType = data.get('Topology','L')
        self.IdType = data.get('ID Type','S')
        self.connectedComputers = []
        self.delayType = data.get('Delay','0')
        self.connectedComputersCreation()
        self.createComputersIds()
        algorithms = data.get('Algorithm', 'no_alg_provided')
        self.loadAlgorithms(algorithms)
        self.networkMessageQueue = CustomPriorityQueue()

    def toString(self):
        print(self.numberOfComputers)
        print(self.topologyType)
        print(self.IdType)
        for computer in self.connectedComputers:
            print(computer)
        print(self.delayType)

    #Getters
    def getNumberOfComputers(self):
        return self.numberOfComputers
    def getTopologyType(self):
        return self.topologyType
    def getConnectedComputers(self):
        return self.connectedComputers
    
    # Create the delays that the computer has according to what he choose
    def createDelays(self):
        for comp in self.connectedComputers:
            comp.delays = {connected_to: self.delayType for connected_to in comp.connectedEdges}
        return

    #Creates the connectedComputers list
    def connectedComputersCreation(self):
        self.connectedComputers = [computer.Computer() for _ in range(self.numberOfComputers)] 
        self.createComputersIds() #Fill the Id's according to the user choice
        
        if (self.topologyType == "R"):
            self.createRandomTopology()
        elif (self.topologyType == "L"):
            self.createLineTopology()
        elif (self.topologyType == "C"):
            self.createCliqueTopology()
        self.createDelays()
        return
    
    # Create the clique topology for the network
    def createCliqueTopology():
        pass 

    # Create computer IDs based on the IdType
    def createComputersIds(self):
        if self.IdType == "R":
            self.createRandomIds()
        elif self.IdType == "S":
            self.createSequentialIds()

    # Create random computer IDs (ensuring uniqueness)
    def createRandomIds(self):
        used_ids = set()
        for comp in self.connectedComputers:
            comp_id = random.randint(100, 100 * self.numberOfComputers - 1)
            while comp_id in used_ids:
                comp_id = random.randint(100, 100 * self.numberOfComputers - 1)
            comp.id = comp_id
            used_ids.add(comp_id)

    # Create uniform computer IDs
    def createSequentialIds(self):
        for i, comp in enumerate(self.connectedComputers):
            comp.id = i

    def createRandomTopology(self):
        for i, comp in enumerate(self.connectedComputers):
            # Determine a random number of edges (between 1 and numberOfComputers - 1)
            num_edges = random.randint(1, self.numberOfComputers - 1)
            # Choose num_edges unique vertices (excluding i)
            connected_to_vertices = random.sample([j for j in range(self.numberOfComputers) if j != i], num_edges)

            # Add connections
            comp.connectedEdges.extend(connected_to_vertices)

            # Ensure bi-directional connection
            for connected_to in connected_to_vertices:
                self.connectedComputers[connected_to].connectedEdges.append(i)

        # removing duplicates
        for comp in self.connectedComputers:
            comp.connectedEdges=list(set(comp.connectedEdges))

    def createLineTopology(self):
        for i in range(self.numberOfComputers - 1):
            # Connect each computer to the next one in line
            self.connectedComputers[i].connectedEdges.append(i + 1)
            self.connectedComputers[i + 1].connectedEdges.append(i)  # Ensure bi-directional connection

    def loadAlgorithms(self, algorithm_module_path):
        if algorithm_module_path == 'no_alg_provided':
            print("No algorithm was provided")
            exit()
        try:
            directory, file_name = os.path.split(algorithm_module_path)
            base_file_name, _ = os.path.splitext(file_name)
            sys.path.insert(0,directory)

            algorithm_module = importlib.import_module(base_file_name)
            for comp in self.connectedComputers:
                comp.algorithmFile = algorithm_module
                print(comp.algorithmFile)

        except ImportError:
            print(f"Error: Unable to import {base_file_name}.py")
            return None

def main():
    init = Initialization()
    init.toString()

if __name__=="__main__":
    main()