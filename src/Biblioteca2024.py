import sqlite3
import re   
from datetime import datetime, timedelta


def conectar_db():
    try:
        # Ruta de la base de datos
        conn = sqlite3.connect('src/database/GestionBiblioteca.db')
        cursor = conn.cursor()
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None



class Usuario:
    def __init__(self):
        pass

    def agregar_libro(self, titulo, genero, autor, copias):
        if not titulo or not genero or not autor or copias is None:
            print("Error: Todos los campos deben estar llenos y el número de copias debe ser válido.")
            return
        
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Verificar si el libro ya existe
            cursor.execute("SELECT Copias FROM libro WHERE Titulo = ? COLLATE NOCASE", (titulo,))
            resultado = cursor.fetchone()

            if resultado:
                # Si el libro existe, aumentar la cantidad de copias
                copias = resultado[0] + 1
                cursor.execute("UPDATE libro SET Copias = ? WHERE Titulo = ?", (copias, titulo))
                print(f'Copias del libro "{titulo}" aumentadas a {copias}.')
            else:
                # Si no existe, insertar un nuevo libro
                cursor.execute("INSERT INTO libro (Titulo, Genero, Autor, Copias) VALUES (?, ?, ?, ?)",
                               (titulo, genero, autor, copias))
                print(f'Libro "{titulo}" agregado con éxito.')
                
            conn.commit()  # Guardar los cambios
        except sqlite3.Error as e:
            print(f"Error al agregar el libro: {e}")
        finally:
            conn.close()  # Cerrar la conexión

    def eliminar_libro(self, titulo):
        if not titulo or copias is None:
            print("Error: Todos los campos deben estar llenos y el número de copias debe ser válido.")
            return
        
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()


            # Verificar si el libro ya existe
            cursor.execute("SELECT Copias FROM libro WHERE LOWER(Titulo) = ?", (titulo,))
            resultado = cursor.fetchone()

            if resultado:
                copias = resultado[0]  # Obtener la cantidad actual de copias

                if copias > 0:
                    # Preguntar al usuario si desea eliminar todas las copias o una cantidad específica
                    respuesta = input(f'El libro "{titulo}" tiene {copias} copias. ¿Desea eliminar todas las copias (t) o una cantidad específica (n)? (t/n): ').strip().lower()
                
                    if respuesta == 't':
                        # Eliminar todas las copias
                        cursor.execute("UPDATE libro SET Copias = 0 WHERE LOWER(Titulo) = ?", (titulo,))
                        print(f'Se han eliminado todas las copias del libro "{titulo}".')
                    elif respuesta == 'n':
                        # Pedir al usuario cuántas copias desea eliminar
                        try:
                            cantidad_a_eliminar = int(input(f'¿Cuántas copias desea eliminar del libro "{titulo}"? (Máximo {copias}): '))
                            if 0 < cantidad_a_eliminar <= copias:
                                # Actualizar la cantidad de copias
                                cursor.execute("UPDATE libro SET Copias = Copias - ? WHERE LOWER(Titulo) = ?", (cantidad_a_eliminar, titulo))
                                print(f'Se han eliminado {cantidad_a_eliminar} copias del libro "{titulo}".')
                            else:
                                print('Cantidad no válida. No se han realizado cambios.')
                        except ValueError:
                            print("Por favor, ingrese un número válido.")
                    else:
                        print('Opción no válida. No se han realizado cambios.')
                else:
                    print(f'No hay copias del libro "{titulo}" para eliminar.')
            else:
                print(f'Libro "{titulo}" no existe o no se encontró.')

            conn.commit()  # Guardar los cambios
        except sqlite3.Error as e:
            print(f"Error al eliminar el libro: {e}")
        finally:
            conn.close()  # Cerrar la conexión






class Libro:
    def __init__(self) -> None:
        pass

    # Método para ver todos los libros
    def ver_libros(self):
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Seleccionar todos los libros
            cursor.execute("SELECT id_libro, Titulo, Genero, Autor, Copias FROM libro")
            libros = cursor.fetchall()  # Obtener todos los resultados

            # Mostrar los libros
            for libro in libros:
                id_libro, Titulo, Genero, Autor, Copias = libro
                print(f"ID LIBRO: {id_libro},Titulo: {Titulo}, Genero: {Genero},Autor: {Autor}, Numero de copias: {Copias} ")
        except sqlite3.Error as e:
            print(f"Error al obtener los libros: {e}")
        finally:
            conn.close()  # Cerrar la conexión


class Prestamos:
    def __init__(self) -> None:
        pass

    def obtener_id_usuario_por_email(self, email):
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Buscar el ID del usuario por su email
            cursor.execute("SELECT id_usuario FROM usuario WHERE Email = ?", (email,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None  # Retorna el ID del usuario o None si no se encuentra
        except sqlite3.Error as e:
            print(f"Error al buscar el usuario: {e}")
            return None
        finally:
            conn.close()  # Cerrar la conexión

    def mostrar_libros_disponibles(self):
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Seleccionar libros que tengan copias disponibles
            cursor.execute("SELECT id_libro, Titulo, Copias FROM libro WHERE Copias > 0")
            libros = cursor.fetchall()  # Obtener todos los resultados

            if libros:
                print("Libros disponibles:")
                for libro in libros:
                    id_libro, titulo, copias = libro
                    print(f"ID: {id_libro}, Título: {titulo}, Copias disponibles: {copias}")
            else:
                print("No hay libros disponibles en este momento.")
        except sqlite3.Error as e:
            print(f"Error al obtener los libros disponibles: {e}")
        finally:
            conn.close()  # Cerrar la conexión

    def realizar_prestamo(self, email, titulo_libro):
        # Obtener ID del usuario por su email
        id_usuario = self.obtener_id_usuario_por_email(email)
        if id_usuario is None:
            print(f"No se encontró un usuario con el email: {email}.")
            return

        # Mostrar libros disponibles
        self.mostrar_libros_disponibles()

        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Buscar el libro por su título
            cursor.execute("SELECT id_libro FROM libro WHERE LOWER(Titulo) = ? AND Copias > 0 COLLATE NOCASE", (titulo_libro,))
            resultado = cursor.fetchone()

            if resultado is None:
                print(f"No se encontró el libro con el título: {titulo_libro} o no hay copias disponibles.")
                return

            id_libro = resultado[0]

            # Obtener la fecha de inicio (hoy) y la fecha de finalización (un mes después)
            fecha_inicio = datetime.now()
            fecha_finalizacion = fecha_inicio + timedelta(days=30)

            # Insertar un nuevo préstamo
            cursor.execute("INSERT INTO prestamo (id_usuario, id_libro, FechaInicio, FechaFinalizacion) VALUES (?, ?, ?, ?)",
                           (id_usuario, id_libro, fecha_inicio, fecha_finalizacion))

            # Decrementar las copias disponibles del libro
            cursor.execute("UPDATE libro SET Copias = Copias - 1 WHERE id_libro = ?", (id_libro,))
            conn.commit()  # Guardar los cambios
            
            print(f'Préstamo realizado con éxito para el usuario con email {email} y libro "{titulo_libro}".')
            print(f'Fecha de inicio: {fecha_inicio.strftime("%Y-%m-%d")}, Fecha de finalización: {fecha_finalizacion.strftime("%Y-%m-%d")}')
        except sqlite3.Error as e:
            print(f"Error al realizar el préstamo: {e}")
        finally:
            conn.close()  # Cerrar la conexión

    def devolver_prestamo(self, email, titulo_libro):
        id_usuario = self.obtener_id_usuario_por_email(email)
        if id_usuario is None:
            print(f"No se encontró un usuario con el email: {email}.")
            return

        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Buscar el libro por su título
            cursor.execute("SELECT id_libro FROM libro WHERE LOWER(Titulo) = ? COLLATE NOCASE", (titulo_libro,))
            resultado = cursor.fetchone()

            if resultado is None:
                print(f"No se encontró un libro con el título: {titulo_libro}.")
                return

            id_libro = resultado[0]

            # Verificar si el préstamo existe
            cursor.execute("SELECT id_prestamo FROM prestamo WHERE id_usuario = ? AND id_libro = ?", (id_usuario, id_libro))
            prestamo = cursor.fetchone()

            if prestamo is None:
                print("No se encontró un préstamo activo para este libro.")
                return

            # Eliminar el préstamo de la base de datos
            cursor.execute("DELETE FROM prestamo WHERE id_usuario = ? AND id_libro = ?", (id_usuario, id_libro))
            
            # Incrementar las copias disponibles
            cursor.execute("UPDATE libro SET Copias = Copias + 1 WHERE id_libro = ?", (id_libro,))
            conn.commit()  # Guardar los cambios
            print(f'Préstamo devuelto con éxito para el usuario con email {email} y libro "{titulo_libro}".')
        except sqlite3.Error as e:
            print(f"Error al devolver el préstamo: {e}")
        finally:
            conn.close()  # Cerrar la conexión

    def ver_prestamos(self):
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

         # Seleccionar los préstamos y unir con las tablas de usuarios y libros
            cursor.execute('''
            SELECT prestamo.id_prestamo, usuario.Nombre, libro.Titulo, prestamo.FechaInicio, prestamo.FechaFinalizacion
            FROM prestamo
            INNER JOIN usuario ON prestamo.id_usuario = usuario.id_usuario
            INNER JOIN libro ON prestamo.id_libro = libro.id_libro
            ''')

            prestamos = cursor.fetchall()  # Obtener todos los resultados

        # Mostrar los préstamos
            for prestamo in prestamos:
                id_prestamo, Nombre_usuario, Titulo_libro, FechaInicio, FechaFinalizacion = prestamo
                print(f"ID PRESTAMO: {id_prestamo}, USUARIO: {Nombre_usuario}, LIBRO: {Titulo_libro}, Fecha del prestamo: {FechaInicio}, Fecha Finalizacion del prestamo: {FechaFinalizacion}")

        except sqlite3.Error as e:
            print(f"Error al obtener los préstamos: {e}")
        finally:
            conn.close()  # Cerrar la conexión





class Biblioteca:
    def __init__(self) -> None:
        self.ubicacion = "Cordoba"

    def agregar_usuario(self, nombre, apellido, email):
        # Expresión regular para validar el formato de correo electrónico
        regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        # Verificar si el email tiene el formato correcto
        if not re.match(regex_email, email):
            print("Error: El correo electrónico ingresado no es válido")
            return  # Detener la ejecución si el correo no es válido

        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Insertar un nuevo usuario solo si el correo es válido
            cursor.execute("INSERT INTO usuario (Nombre, Apellido, Email) VALUES (?, ?, ?)",
                           (nombre, apellido, email))

            conn.commit()  # Guardar los cambios
            print(f'Usuario "{nombre}" agregado con éxito al sistema.')
        except sqlite3.Error as e:
            print(f"Error al agregar el usuario: {e}")
        finally:
            conn.close()  # Cerrar la conexión

    def eliminar_usuario(self, id_usuario, email):
        if id_usuario is None:
            print(f"No se encontró un usuario con el email: {email}.")
            return
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,))
            resultado = cursor.fetchone()

            if resultado:
                # Confirmar la eliminación
                confirmacion = input(f'¿Está seguro de que desea eliminar al usuario con el email {email}? (si/no): ').strip().lower()
                if confirmacion == 'si':
                    # Eliminar el usuario
                    cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
                    print(f'Se ha eliminado el usuario con el email {email}')
                elif confirmacion == 'no':
                    print('Eliminación cancelada.')
            else:
                print(f'No se encontró un usuario con ID {id_usuario}.')

            conn.commit()  # Guardar los cambios
        except sqlite3.Error as e:
            print(f"Error al eliminar el usuario: {e}")
        finally:
            conn.close()  # Cerrar la conexión

    def ver_usuarios(self):
        try:
            conn = conectar_db()  # Conectar a la base de datos
            cursor = conn.cursor()

            # Seleccionar todos los libros
            cursor.execute("SELECT id_usuario, Nombre, Apellido, Email FROM usuario")
            usuarios = cursor.fetchall()  # Obtener todos los resultados

            # Mostrar los libros
            for usuario in usuarios:
                id_usuario, Nombre, Apellido, Email = usuario
                print(f"ID USUARIO: {id_usuario}, Nombre: {Nombre}, Apellido: {Apellido}, Email: {Email}")
        except sqlite3.Error as e:
            print(f"Error al obtener los usuarios: {e}")
        finally:
            conn.close()  # Cerrar la conexión


# ======================================= MENU =======================================

def main():
    biblioteca = Biblioteca()
    usuario = Usuario()
    libro = Libro()
    prestamo = Prestamos()

    while True:
        print("\n==========  Bienvenidos a la Biblioteca de Nueva Cordoba!  ==========")
        print("\n   Para realizar un prestamo, primero debera registrarse como un nuevo usuario.")
        print("\n   Opciones:\n")
        print("1. Agregar usuario")
        print("2. Eliminar usuario")
        print("3. Ver usuarios")
        print("4. Agregar libro")
        print("5. Eliminar libro")
        print("6. Ver libros")
        print("7. Realizar préstamo")
        print("8. Devolver préstamo")
        print("9. Ver préstamos")
        print("10. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            nombre = input("Ingrese el nombre del usuario: ")
            apellido = input("Ingrese el apellido del usuario: ")
            email = input("Ingrese el email del usuario: ").lower()
            biblioteca.agregar_usuario(nombre, apellido, email)
        elif opcion == '2':
            email = input("Ingrese el email del usuario: ").lower()
            usuarioAEliminar = prestamo.obtener_id_usuario_por_email(email)
            biblioteca.eliminar_usuario(usuarioAEliminar, email)
        elif opcion == '3':
            biblioteca.ver_usuarios()
        elif opcion == '4':
            titulo = input("Ingrese el título del libro: ").lower()
            genero = input("Ingrese el género del libro: ").lower()
            autor = input("Ingrese el autor del libro: ").lower()
            copias = input("Ingrese la cantidad de copias del libro: ")
            usuario.agregar_libro(titulo, genero, autor, copias)
        elif opcion == '5':
            titulo = input("Ingrese el título del libro: ").lower()
            usuario.eliminar_libro(titulo)
        elif opcion == '6':
            libro.ver_libros()
        elif opcion == '7':
            print('==========  Listado de libros disponibles para prestamo  ==========')
            prestamo.mostrar_libros_disponibles()
            print('===================================================================')
            email = input("Ingrese el email del usuario: ").lower()
            titulo_libro = input("Ingrese el título del libro que desea prestar: ").lower()
            prestamo.realizar_prestamo(email, titulo_libro)
        elif opcion == '8':
            email = input("Ingrese el email del usuario: ").lower()
            titulo_libro = input("Ingrese el título del libro que desea devolver: ").lower()
            prestamo.devolver_prestamo(email, titulo_libro)
        elif opcion == '9':
            prestamo.ver_prestamos()
        elif opcion == '10':
            break


if __name__ == "__main__":
    main()
