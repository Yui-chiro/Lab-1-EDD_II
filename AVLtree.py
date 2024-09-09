import pandas as pd
import matplotlib.pyplot as plt
from collections import deque



# define la clase nodo
class AVLTreeNode:
    def __init__(self, Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings, Domestic_Percent,
                 Foreign_Percent):
        self.Title = Title
        self.Year = Year
        self.Worldwide_Earnings = Worldwide_Earnings
        self.Domestic_Earnings = Domestic_Earnings
        self.Foreign_Earnings = Foreign_Earnings
        self.Domestic_Percent = Domestic_Percent
        self.Foreign_Percent = Foreign_Percent
        self.height = 1
        self.left = None
        self.right = None


# Define  la clase Arbol AVL
class AVLTree:

    def exists(self, root, Title):
        # Busca el nodo a ver si se encuentra en el arbol
        node = self.lookup(root, Title)
        return node is not None

    def insert(self, root, Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings, Domestic_Percent,
               Foreign_Percent):
        if not root:
            return AVLTreeNode(Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings, Domestic_Percent,
                               Foreign_Percent)

        if Title < root.Title:
            root.left = self.insert(root.left, Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings,
                                    Domestic_Percent, Foreign_Percent)
        elif Title > root.Title:
            root.right = self.insert(root.right, Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings,
                                     Domestic_Percent, Foreign_Percent)
        else:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and Title < root.left.Title:
            return self.right_rotate(root)
        if balance < -1 and Title > root.right.Title:
            return self.left_rotate(root)
        if balance > 1 and Title > root.left.Title:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and Title < root.right.Title:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def delete(self, root, Title):
        if not root:
            return root

        if Title < root.Title:
            root.left = self.delete(root.left, Title)
        elif Title > root.Title:
            root.right = self.delete(root.right, Title)
        else:
            if not root.left:
                temp = root.right
                root = None
                return temp
            elif not root.right:
                temp = root.left
                root = None
                return temp

            temp = self.get_min_value_node(root.right)
            root.Title = temp.Title
            root.Year = temp.Year
            root.Worldwide_Earnings = temp.Worldwide_Earnings
            root.Domestic_Earnings = temp.Domestic_Earnings
            root.Foreign_Earnings = temp.Foreign_Earnings
            root.Domestic_Percent = temp.Domestic_Percent
            root.Foreign_Percent = temp.Foreign_Percent
            root.right = self.delete(root.right, temp.Title)

        if not root:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def lookup(self, root, Title):
        if not root:
            return None
        if Title == root.Title:
            return root
        if Title < root.Title:
            return self.lookup(root.left, Title)
        return self.lookup(root.right, Title)

    def lookup_node(self, root, Title):
        result = self.lookup(root, Title)
        if result:
            print(f"Title: {result.Title}")
            print(f"Year: {result.Year}")
            print(f"Worldwide Earnings: {result.Worldwide_Earnings}")
            print(f"Domestic Earnings: {result.Domestic_Earnings}")
            print(f"Foreign Earnings: {result.Foreign_Earnings}")
            print(f"Domestic Percent Earnings: {result.Domestic_Percent}")
            print(f"Foreign Percent Earnings: {result.Foreign_Percent}")
        else:
            print(f"La pelicula '{Title}' no se encontró")

    def search_criteria(self, root, year, min_foreign_earnings):
        result = []

        def inorder_traversal(node):
            if node is None:
                return
            inorder_traversal(node.left)
            if (node.Year == year and
                    node.Domestic_Percent < node.Foreign_Percent and
                    node.Foreign_Earnings >= min_foreign_earnings):
                result.append(node)
            inorder_traversal(node.right)

        inorder_traversal(root)
        return result

    def print_titles(self, result):
        if not result:
            print("No hay películas que cumplan con los criterios.")
        else:
            for node in result:
                print(node.Title)


def build_avl_tree_from_dataframe(df):
    tree = AVLTree()
    root = None
    for index, row in df.iterrows():
        Title = row['Title']
        Year = int(row['Year'])
        Worldwide_Earnings = float(row['Worldwide Earnings'])
        Domestic_Earnings = float(row['Domestic Earnings'])
        Foreign_Earnings = float(row['Foreign Earnings'])
        Domestic_Percent = float(row['Domestic Percent Earnings'])
        Foreign_Percent = float(row['Foreign Percent Earnings'])
        root = tree.insert(root, Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings, Domestic_Percent,
                           Foreign_Percent)
    return root

def plot_avl_tree(node, x=0, y=0, dx=1, dy=1, ax=None, level=0):
    if node is None:
        return
    ax.text(x, y, f'{node.Title}', ha='center', va='center', fontsize=8,
            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.3'))
    if node.left:
        ax.plot([x, x - dx], [y, y - dy], color='black')
        plot_avl_tree(node.left, x - dx, y - dy, dx / 2.5, dy, ax, level + 1)
    if node.right:
        ax.plot([x, x + dx], [y, y - dy], color='black')
        plot_avl_tree(node.right, x + dx, y - dy, dx / 2.5, dy, ax, level + 1)

def draw_tree(root):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    plot_avl_tree(root, ax=ax, dx=5, dy=2)
    plt.show()


def level_order_traversal(root):
    if not root:
        return

    queue = deque([root])

    while queue:
        node = queue.popleft()
        print(node.Title)  # mostrar los titulos

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)


# Para encontrar el nivel del nodo
def find_node_level(root, title, level=1):
    if root is None:
        return -1  # si no existe

    if root.Title == title:
        return level

    left_level = find_node_level(root.left, title, level + 1)
    if left_level != -1:
        return left_level

    return find_node_level(root.right, title, level + 1)


# factor de balance
def get_balance_of_node(tree, root, title):
    node = tree.lookup(root, title)
    if node:
        return tree.get_balance(node)
    return None


# padre de un nodo
def find_parent(root, title, parent=None):
    if not root:
        return None

    if root.Title == title:
        return parent

    if title < root.Title:
        return find_parent(root.left, title, root)
    else:
        return find_parent(root.right, title, root)


# abuelo del nodo
def find_grandparent(root, title):
    parent = find_parent(root, title)
    if parent:
        return find_parent(root, parent.Title)
    return None


# tio de un nodo
def find_uncle(root, title):
    parent = find_parent(root, title)
    grandparent = find_grandparent(root, title)

    if not grandparent:
        return None

    if grandparent.left == parent:
        return grandparent.right
    else:
        return grandparent.left

