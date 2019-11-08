import random
from room import Room
from player import Player
from world import World

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        if vertex not in self.vertices.keys():
          self.vertices[vertex] = set()
        else:
          pass
    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 and v2 in self.vertices.keys():
         #self.vertices[v2].add(v1)
          self.vertices[v1].add(v2)

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        ret_list = []
        if starting_vertex is None:
          return None
        my_q = Queue()
        visited = [starting_vertex]
        my_q.enqueue(starting_vertex)
        while len(my_q.queue) > 0:
          point = my_q.queue[0]
          joins = self.vertices[point]
          for j in joins:
            if j not in visited:
              my_q.enqueue(j)
              visited.append(j)
          #print(my_q.dequeue())
          ret = my_q.dequeue()
          ret_list.append(ret)
        return ret_list
          


    def dft(self, starting_vertex, chooser=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        ret_list = []
        if starting_vertex is None:
          return None
        my_s = Stack()
        visited = [starting_vertex]
        my_s.push(starting_vertex)
        while len(my_s.stack) > 0:
          point = my_s.stack[-1]
          joins = self.vertices[point]
          r = my_s.pop()   ##new code
          ret_list.append(r)  ##new code
          #print(r)  ##changed to r from pop
          if chooser is None:
            pass
          elif chooser == 'random':
            joins = random.sample(joins,len(joins))
          elif chooser == 'shortest':
            joins = find_longest_clique(point,self,visited)
          for j in joins:
            if j not in visited:
              my_s.push(j)
              visited.append(j)
        return ret_list


    def dft_recursive(self, starting_vertex, visited = []):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        print(starting_vertex)
        visited.append(starting_vertex)
        joins = self.vertices[starting_vertex]
        if joins is None:
          return None
        for j in joins:
          if j in visited:
            pass
          else:
            self.dft_recursive(j,visited)



    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        q.enqueue([starting_vertex])
        
        while destination_vertex not in q.queue[0]:
          current_point = q.queue[0][-1]
          joins = self.vertices[current_point]
          for j in joins:
            _ = [x for x in q.queue[0]]
            _.append(j)
            q.enqueue(_)
          q.dequeue()

        return q.queue[0]

          


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])
        
        while destination_vertex not in s.stack[-1]:
          current_point = s.stack[-1][-1]
          
          joins = self.vertices[current_point]
          if joins is None:
            s.pop()
          else:
            temp_list = []
            for j in joins:
              _ = [x for x in s.stack[-1]]
              _.append(j)
              temp_list.append(_)
            for tl in temp_list:
              s.push(tl)
          #s.pop()

        return s.stack[-1]

def create_starting_map(world):
  my_map = Graph()
  player = Player("Name", world.startingRoom)
  exits = player.currentRoom.getExits()
  exit_dict = {}
  for e in exits:
    exit_dict[e] = '?'
  my_map.vertices[player.currentRoom.id] = exit_dict
  return my_map,player


def pop_map_on_move(my_map,world,player,move):
  reverse_dir ={'n':'s','s':'n','w':'e','e':'w'}
  old_room = player.currentRoom.id
  player.travel(move)
  new_room = player.currentRoom.id
  if new_room not in my_map.vertices:
    exit_dict = {}
    for exits in player.currentRoom.getExits():
        for e in exits:
          exit_dict[e] = '?'
    my_map.vertices[new_room] = exit_dict
  my_map.vertices[old_room][move] = new_room
  reverse_move = reverse_dir[move]
  my_map.vertices[new_room][reverse_move] = old_room

def count_unmapped(my_map):
  counter = 0
  for val1 in my_map.vertices.values():
    for val2 in val1.values():
      if val2=='?':
        counter += 1
  return counter

def bfs_for_q(my_map,player):
  room = player.currentRoom.id
  q = Queue()
  q.enqueue([room])
  
  room = player.currentRoom.id
  q = Queue()
  q.enqueue([room])
  while '?' not in my_map.vertices[room].values(): 
    
    joins = my_map.vertices[room]
    for j in joins.values():
      if j in q.queue[0]:
        pass
      else:
        _ = [x for x in q.queue[0]]
        _.append(j)
        q.enqueue(_)
    q.dequeue()
    room = q.queue[0][-1]

  return q.queue[0]

def get_dirs(my_map,traversal):
  point = traversal[0]
  dir_list = []
  for t in traversal[1:]:
    for key in my_map.vertices[point]:
      if my_map.vertices[point][key]==t:
        dir_list.append(key)
    point = t
  return dir_list

def dfs_random(world, parent_graph, how='random'):
  my_map, player = create_starting_map(world)
  unmapped_number = count_unmapped(my_map)
  moves = []
  while unmapped_number > 0:
    room = player.currentRoom.id
    unvisited_exits = [x for x in my_map.vertices[room] if my_map.vertices[room][x]=='?']
    if unvisited_exits !=[]:
      if how =='random':
        move = random.choice(unvisited_exits)
      elif how[:7] =='chooser':
        if len(unvisited_exits)==1:
            move = unvisited_exits[0]
        else:
            rg = roomgraph_to_graph(parent_graph)
            flc = find_longest_clique(room,rg,list(my_map.vertices.keys()),how=how )
            #print(flc, type(rg.vertices),rg.vertices[room],unvisited_exits,room)
            for m in unvisited_exits:
                if m in  parent_graph[room][1].keys() and parent_graph[room][1][m] ==flc[-1]:
                    move = m
            #print('chooser move',move,flc)
      moves.append(move)
      pop_map_on_move(my_map,world,player,move)
      unmapped_number = count_unmapped(my_map)
    else:   
      #print('back track on') 
      backtrack = bfs_for_q(my_map,player)
      #print('backtrack is', backtrack)
      backtrack_dirs = get_dirs(my_map,backtrack)
      for item in backtrack_dirs:
        moves.append(item)
        player.travel(item)
  
  return moves, my_map.vertices

def find_longest_clique(node,parent_graph,visited = [], how='chooser'):
  joins = parent_graph.vertices[node]
  joins = [x for x in joins if x not in visited]
  join_dict = {}
  for j in joins:
    new_graph = Graph()
    exclude_list = [y for y in joins if y!=j]
    new_node_list = [x for x in parent_graph.vertices if x not in visited or exclude_list]
    for nn in new_node_list:
      new_graph.vertices[nn] = set([z for z in parent_graph.vertices[nn] if z not in (visited+exclude_list)])
    join_dict[j] = len(new_graph.bft(j))
  ret = sorted(join_dict.items(), key=lambda kv: kv[1],reverse=True)
  #print(ret)
  if how == 'chooserrandom':
      if len(ret)>1:
        #if abs(ret[-1][1] - ret[-2][1])<3:
        if ret[-1][1]>40:
            swap = random.sample([ret[-1],ret[-2]],2)
            ret[-1] = swap[0]
            ret[-2] = swap[1]
  ret = [x[0] for x in ret]
  return ret

def roomgraph_to_graph(rg):
  my_graph = Graph()
  connection_strip = {}
  for key in rg:
    my_graph.add_vertex(key)
    connection_strip[key] = set(rg[key][1].values())
  my_graph.vertices = connection_strip
  return my_graph