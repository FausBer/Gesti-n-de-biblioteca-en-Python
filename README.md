# Biblioteca - Sistema de Gestión

Este proyecto es un sistema de gestión de biblioteca desarrollado en Python, que permite manejar de manera eficiente libros, usuarios y préstamos. Utiliza programación orientada a objetos (POO) y una base de datos SQLite para almacenar la información de manera persistente.

## Descripción

El sistema permite realizar operaciones básicas de gestión de una biblioteca mediante una interfaz de línea de comandos, como agregar y eliminar libros, registrar usuarios, y gestionar préstamos. Está diseñado para ser escalable y fácil de mantener.

## Características

- **Libros**: Registro de libros en la biblioteca con información como título, autor, género y cantidad de copias disponibles.
- **Usuarios**: Registro de usuarios con datos básicos, lo que permite identificar a cada persona que usa el sistema.
- **Préstamos**: Sistema de registro y control de préstamos de libros, incluyendo fechas de préstamo y devolución.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal del proyecto.
- **SQLite**: Base de datos ligera y embebida que almacena la información de libros, usuarios y préstamos.
- **Programación Orientada a Objetos (POO)**: El proyecto sigue un diseño modular basado en clases para mejorar la legibilidad y reutilización del código.

## Clases Principales

1. **`Usuario`**: Representa a los usuarios de la biblioteca y almacena su información.
2. **`Libro`**: Contiene detalles de cada libro disponible en la biblioteca, como el número de copias disponibles.
3. **`Prestamo`**: Gestiona los préstamos, incluyendo información del libro prestado, el usuario que lo toma, y las fechas correspondientes.
4. **`Biblioteca`**: Controlador principal del sistema. Contiene métodos para gestionar libros, usuarios y préstamos, conectando todos los componentes.

## Instalación y Uso

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/biblioteca.git
   cd biblioteca
