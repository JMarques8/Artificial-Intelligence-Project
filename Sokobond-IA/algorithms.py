import copy
from collections import deque
from boards import BOARDS
from elements import Atom, GridElement  
from constants import *  

class GameState:
    def __init__(self, level, player_position):
        self.level = level # Current level
        self.player_position = player_position # tuplo (x, y) passar a posiçao inicial de p/ cada nivel
        ####### iguais a GameLevel
        self.level_data = BOARDS[level]
        print("Entered in GameState")  # Debugging line
        print(player_position)  # Debugging line
        self.atom_player = Atom(player_position[0], player_position[1], RED, 1)
        self.player_connections = self.atom_player.connection # lista de conexoes do player
        self.board_elements = self.create_board_elements()

    """
    def __str__(self):
        # Include level and player position in the string representation
        return 'Level: ' + str(self.level) + ', Player Position: ' + str(self.player_position) + ', Player Connections: ' + str(self.player_connections)

    def __hash__(self):
        # Use a tuple of the level and player position
        return hash((self.level, self.player_position, self.player_connections))

    def __eq__(self, other):
        # Check if other is a GameState object
        if not isinstance(other, GameState):
            return False
        # Compare the level and player position
        return self.level == other.level and self.player_position == other.player_position and self.player_connections == other.player_connections
    
    """
    def __str__(self):
        # Include level, player position, and positions of connected atoms
        connections_str = [(atom.x, atom.y) for atom in self.player_connections]
        return 'Level: {}, Player Position: {}, Player Connections: {}'.format(self.level, self.player_position, connections_str)

    def __hash__(self):
        # Use a tuple of the level, player position, and positions of connected atoms
        connections_tuple = tuple((atom.x, atom.y) for atom in self.player_connections)
        return hash((self.level, self.player_position, connections_tuple))

    def __eq__(self, other):
        # Check if other is a GameState object
        if not isinstance(other, GameState):
            return False

        # Compare the level and player position
        level_equal = self.level == other.level
        position_equal = self.player_position == other.player_position

        # Compare the positions of the atoms in player_connections
        self_connections = [(atom.x, atom.y) for atom in self.player_connections]
        other_connections = [(atom.x, atom.y) for atom in other.player_connections]
        connections_equal = self_connections == other_connections

        return level_equal and position_equal and connections_equal

    ####### Game State exclusive  #####
    def get_possible_moves(self):
        moves = []
        # Check each direction: up, down, left, right
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            #verificar se a move é válida
            if self.is_valid_move(self.atom_player, dx, dy):
                #adicionar a lista de moves possiveis se for valida
                print("Valid move: ", dx, dy)
                moves.append((dx, dy))
        return moves

    def get_neighbors(self): #child_nodes
        # Generate all possible successor states
        neighbors = []
        for move in self.get_possible_moves():
            new_state = self.make_move(move) #new_state = return GameState(self.level, new_player_position)  # Create new GameState object
            if new_state:
                neighbors.append((new_state, move))  # Return move along with state
        return neighbors

    def make_move(self, move):
        dx, dy = move
        # Make the move on the copy
        new_player_position = self.move_atom_player(dx, dy)
        new_player_connections = self.atom_player.connection
        # Return a new GameState object that represents the new game state
        new_state = copy.deepcopy(self)  # Create a deep copy of the current state
        new_state.update_state(new_player_position, new_player_connections)  # Update the state of the copy
        return new_state  # Return the new state
    
    def update_state(self, new_player_position, new_player_connections):
        self.player_position = new_player_position
        self.player_connections = new_player_connections
        # Assuming the atom_player's position is updated with the player's position
        self.atom_player.x, self.atom_player.y = new_player_position
    
    def create_board_elements(self):
        board_elements = []
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_elements.append(GridElement(x, y, DARK_YELLOW))
                elif cell == 'G':
                    board_elements.append(GridElement(x, y, GRAY))
                elif cell == 'H':
                    board_elements.append(Atom(x, y, RED,1))
                elif cell == 'O':
                    board_elements.append(Atom(x, y, BLUE,2))
                elif cell == 'C':
                    board_elements.append(Atom(x, y, DARK_YELLOW,4))
        return board_elements
    
    def is_valid_move(self, atom, dx, dy, visited=None):
        if visited is None:
            visited = set()

        new_x = atom.x + dx
        new_y = atom.y + dy

        print("Checking if move is valid: ", new_x, new_y)
        # Check if new position is outside the grid
        if new_x < 0 or new_x >= GRID_SIZE or new_y < 0 or new_y >= GRID_SIZE:
            #print("Invalid move: Outside Grid")
            return False

        # Check if new position is a wall
        if self.level_data[new_y][new_x] == '#':
            #print("Invalid move: Wall")
            return False

        # Check for all connected atoms
        for connected_atom in atom.connection:
            if connected_atom not in visited:
                visited.add(connected_atom)
                # Recursive call to check the move for each connected atom
                if not self.is_valid_move(connected_atom, dx, dy, visited):
                    print("Connected atom invalid move")
                    return False
        # If all checks pass, the move is valid
        return True

    #used to check if there's an atom at a specific location on the game board that can be connected to the player's atom
    def is_atom_connection(self, target_x, target_y):
        for element in self.board_elements: #iterates over the board elements and checks if there's an atom at the target location
            if isinstance(element, Atom) and element != self.atom_player and element.x == target_x and element.y == target_y:
                return element  #returning an atom object if it's found at the target location
        return None

    def move_atom_player(self, dx, dy):
        #### SINGLE ATOM CASE
        if len(self.atom_player.connection) == 0: #check if the player's atom is NOT connected to any other atoms
            new_x = self.atom_player.x + dx
            new_y = self.atom_player.y + dy
            #checks if there is an atom at the new position that can be connected to the player's atom
            atom = self.is_atom_connection(new_x, new_y) #estamos a adicionar uma conexao na mesma celula que o player ???
            if atom is not None and atom not in self.atom_player.connection:
                #no updates on the player's position since there's an atom there
                if self.atom_player.add_connection(atom): #adicionar nova conexao SE respeitar as condições
                    print("Connection successfully added")
                    print("atom info:", atom.x, atom.y, atom.max_connection, len(atom.connection))
                    print("player info:", self.atom_player.x, self.atom_player.y, self.atom_player.max_connection, len(self.atom_player.connection))
            return (new_x, new_y)
        
        #### CHANGED HERE 
        elif len(self.atom_player.connection) > 0:
            print("Player has connections")
            #Gather all atoms in the molecule
            all_atoms = self.gather_molecule_atoms(self.atom_player)
            # Get a LIST of atoms on the edge of the molecule
            edge_atom = self.get_extreme_atoms(all_atoms, dx, dy) #returns a list

            #if len(edge_atom) == 1:
                #target position é em relação ao edge_atom
            new_x = edge_atom[0].x + dx
            new_y = edge_atom[0].y + dy
            #checks if there is an atom at the new position that can be connected to the edge_atom
            atom = self.is_atom_connection(new_x, new_y)
            if atom is not None and atom not in all_atoms:
                #no updates on the player's position since there's an atom there
                if edge_atom[0].add_connection(atom): #adicionar nova conexao se respeitar as condições
                    print("New molecule connection")
                else: #PUSH
                    print("Can not connect Atom")
                    valid_move = self.is_valid_move(atom, dx, dy)
                    if valid_move: ## Move the atom if the move is valid
                        self.update_positions(atom, dx, dy,set())
                        self.update_positions(edge_atom[0], dx, dy,set())
            else: #there's no atom at the new position
                #updates the x and y coordinates of all atoms in the molecule to the new position            
                visited = set()
                self.update_positions(self.atom_player, dx, dy, visited)
            return (self.atom_player.x, self.atom_player.y)

            """
            elif len(edge_atom) > 1:
                print("Multiple edge atoms")
                atom_found = False
                for atom_element in edge_atom:
                    #target position é em relação a todos os atomos na borda
                    new_x = atom_element.x + dx
                    new_y = atom_element.y + dy

                    #checks if there is an atom at the new position that can be connected
                    atom = self.is_atom_connection(new_x, new_y)
                    if atom is not None and atom not in all_atoms:
                        atom_found = True
                        if atom_element.add_connection(atom): #adicionar nova conexao se respeitar as condições
                            print("New molecule connection")
                        else:
                            print("Can not connect Atom")
                            valid_move = self.is_valid_move(atom, dx, dy)
                            if valid_move: ## Move the atom if the move is valid
                                print("Atom is being pushed")
                                self.update_positions(atom, dx, dy,set())
                                self.update_positions(self.atom_player, dx, dy, set())
                        return (self.atom_player.x, self.atom_player.y)
                    if not atom_found:
                        #updates the x and y coordinates of all atoms in the molecule to the new position            
                        visited = set()
                        self.update_positions(self.atom_player, dx, dy, visited)
                        return (self.atom_player.x, self.atom_player.y)
            """

    def gather_molecule_atoms(self, atom, visited=None):
        if visited is None:
            visited = set()
        visited.add(atom)
    
        for connected_atom in atom.connection:
            if connected_atom not in visited:
                self.gather_molecule_atoms(connected_atom, visited)
    
        return visited
        
    ### GET ATOM ON THE EDGE OF THE MOLECULE FUNCTIONS ###
    def get_extreme_atoms(self, atoms, dx, dy):
        if dx < 0:  # left (-1,0)
            min_x = min(atom.x for atom in atoms)
            return [atom for atom in atoms if atom.x == min_x]
        elif dx > 0:  # right (1,0)
            max_x = max(atom.x for atom in atoms)
            return [atom for atom in atoms if atom.x == max_x]
        elif dy < 0:  # up (0,-1)
            min_y = min(atom.y for atom in atoms)
            return [atom for atom in atoms if atom.y == min_y]
        else:  # down
            max_y = max(atom.y for atom in atoms)
            return [atom for atom in atoms if atom.y == max_y]

    ### UPDATE POSITIONS OF ALL ATOMS FUNCTIONS ###
    def update_positions(self, atom, dx, dy, visited=None):
        if visited is None:
            visited = set()
        # Update the position of the current atom
        atom.x += dx
        atom.y += dy
        # Add the current atom to the set of visited atoms
        visited.add(atom)

        # Recursively update the positions of all connected atoms that haven't been visited yet
        for connected_atom in atom.connection:
            if connected_atom not in visited:
                self.update_positions(connected_atom, dx, dy, visited)


    def is_goal(self): #same as GameLevel.check_all_connections_filled
        # Iterate over all atom elements in the game grid
        for element in self.board_elements:
            # Check if the element is an instance of Atom
            if isinstance(element, Atom):
                # Check if the atom's connections are less than its max connections
                print(f"Atom at ({element.x}, {element.y}) has {len(element.connection)} connections out of {element.max_connection}")
                if len(element.connection) < element.max_connection:
                    # Found an atom that doesn't have all connections filled
                    return False
        # All atoms have their connections filled
        return True
        
    

#### Depth-first search algorithm
def dfs(initial_state):
    stack = [(initial_state, [])]  # Stack stores tuples of (GameState, path_to_this_point)
    visited = set()  # Set to store visited states
    print("Entered in DFS")  # Debugging line
    print("Stack", stack)  # Debugging line

    while stack:
        current_state, path = stack.pop()  # Get the most recent state and path
        state_id = str(current_state)  # Unique identifier for the state
        print("Current State: ", state_id)  # Debugging line

        if state_id in visited:  # Skip if we've already visited this state
            continue

        visited.add(state_id)  # Mark the current state as visited

        if current_state.is_goal():  # Check if the current state satisfies the goal condition
            print("Goal State: ", state_id)  # Debugging line
            return path  # Return the path leading to this goal state

        # Explore neighbors (successor states) that haven't been visited
        for neighbor, move in current_state.get_neighbors():
            neighbor_id = str(neighbor)
            if neighbor_id not in visited:
                print("Neighbor State: ", neighbor_id)  # Debugging line
                stack.append((neighbor, path + [move]))  # Add neighbor state and the path leading to it to the stack

    print("Visited Set:", visited)  # Debugging line
    return None  # Return None if no goal state is found

#### BFS: Breadth-first search algorithm

def bfs(initial_state):
    queue = deque([(initial_state, [])])  # Queue stores tuples of (GameState, path_to_this_point)
    visited = set()  # Set to store visited states

    while queue:
        current_state, path = queue.popleft()  # Get the oldest state and path
        state_id = str(current_state)  # Unique identifier for the state

        if state_id in visited:  # Skip if we've already visited this state
            continue

        visited.add(state_id)  # Mark the current state as visited

        if current_state.is_goal():  # Check if the current state satisfies the goal condition
            return path  # Return the path leading to this goal state

        # Explore neighbors (successor states) that haven't been visited
        for neighbor, move in current_state.get_neighbors():
            neighbor_id = str(neighbor)
            if neighbor_id not in visited:
                queue.append((neighbor, path + [move]))  # Add neighbor state and the path leading to it to the queue

    return None  # Return None if no goal state is found