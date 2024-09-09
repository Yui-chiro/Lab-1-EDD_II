import pandas as pd
from AVLtree import *
import matplotlib.pyplot as plt

def main():
    # Crear el árbol AVL
    tree = AVLTree()
    root = None
    file_path = "C:\\Users\\agc17\\PycharmProjects\\lab12\\lab1\\dataset_movies.csv"

    # cargar csv con pandas
    df = pd.read_csv(file_path)

    # Bucle principal para interactuar con el usuario
    while True:
        print("\nMenú de opciones:")
        print("1. Agregar una película.")
        print("2. Eliminar una película.")
        print("3. Buscar una película.")
        print("4. Buscar un conjunto de películas.")
        print("5. Mostrar el recorrido del árbol.")
        print("6. Salir.")

        # Leer la elección del usuario
        try:
            choice = int(input("Elija lo que quisiera hacer con el árbol según el número: "))
        except ValueError:
            print("Por favor ingrese un número válido.")
            continue

        # Procesar la elección del usuario
        if choice == 1:
            # Agregar una película
            # pedir el título de la película
            Title = input("Ingrese el título de la película: ")

            # Buscar la fila correspondiente al título ingresado
            movie = df[df['Title'] == Title]

            if not movie.empty:
                # agarrar la información de la película
                Year = int(movie['Year'].values[0])
                Worldwide_Earnings = float(movie['Worldwide Earnings'].values[0])
                Domestic_Earnings = float(movie['Domestic Earnings'].values[0])
                Foreign_Earnings = float(movie['Foreign Earnings'].values[0])
                Domestic_Percent = float(movie['Domestic Percent Earnings'].values[0])
                Foreign_Percent = float(movie['Foreign Percent Earnings'].values[0])

                # Insertar la película en el árbol
                root = tree.insert(root, Title, Year, Worldwide_Earnings, Domestic_Earnings, Foreign_Earnings,
                                   Domestic_Percent, Foreign_Percent)
                print(f"Película '{Title}' agregada correctamente.")
                draw_tree(root)

            else:
                print(f"No se encontró la película '{Title}' en el archivo CSV.")

        elif choice == 2:
            Title = input("Ingrese el título de la película que desea eliminar: ")

            # Verificar si la película existe en el árbol
            if tree.exists(root, Title):
                # Eliminar la película del árbol
                root = tree.delete(root, Title)
                print(f"Película '{Title}' eliminada correctamente.")
                draw_tree(root)
            else:
                print(f"No se encontró la película '{Title}' en el árbol.")


        elif choice == 3:
            # Buscar una película
            Title = input("Ingrese el título de la película que desea buscar: ")
            tree.lookup_node(root, Title)

        elif choice == 4:
            # Buscar películas por criterio
            year = int(input("Ingrese el año: "))
            min_foreign_earnings = float(input("Ingrese las ganancias extranjeras mínimas: "))
            movies = tree.search_criteria(root, year, min_foreign_earnings)

            if movies:
                print(
                    f"Películas encontradas para el año {year} con ganancias extranjeras superiores a {min_foreign_earnings}:")
                for movie in movies:
                    print(f"- {movie.Title}")
            else:
                print("No se encontraron películas que cumplan los criterios.")

        elif choice == 5:
            # Mostrar el recorrido del árbol (en forma gráfica)
            draw_tree(root)
            # Datos extra de un nodo
            Title = input("Por favor ingrese el nombre de la película para obtener datos extra: ")

            # Nivel del nodo
            level = find_node_level(root, Title)
            if level != -1:
                print(f"Nivel del nodo '{Title}': {level}")
            else:
                print(f"Película '{Title}' no encontrada.")

            # Factor de balance
            balance = get_balance_of_node(tree, root, Title)
            if balance is not None:
                print(f"Factor de balance de '{Title}': {balance}")
            else:
                print(f"Película '{Title}' no encontrada o no tiene balance calculado.")

            # Padre del nodo
            parent = find_parent(root, Title)
            if parent:
                print(f"Padre de '{Title}': {parent.Title}")
            else:
                print(f"Película '{Title}' no tiene padre (es la raíz o no se encontró).")

            # Abuelo del nodo
            grandparent = find_grandparent(root, Title)
            if grandparent:
                print(f"Abuelo de '{Title}': {grandparent.Title}")
            else:
                print(f"Película '{Title}' no tiene abuelo o no se encontró.")

            # Tío del nodo
            uncle = find_uncle(root, Title)
            if uncle:
                print(f"Tío de '{Title}': {uncle.Title}")
            else:
                print(f"Película '{Title}' no tiene tío o no se encontró.")

        elif choice == 6:
            # Salir del programa
            print("Saliendo del programa.")
            break

        else:
            print("Por favor elija una opción válida.")


if __name__ == "__main__":
    main()
