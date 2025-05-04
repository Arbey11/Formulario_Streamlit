'''
este formulario permite loguearse si esta registrado en una BBDD
en caso contrario, permite realizar el registro
'''

import streamlit as st
import sqlite3

# Crear la base de datos y la tabla si no existen
conexion = sqlite3.connect('usuarios.db')
cursor = conexion.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        nombre TEXT NOT NULL,
        contrasena TEXT NOT NULL
    )
''')
conexion.commit()
conexion.close()

# Formulario
st.write('### Acceso de Usuarios')

with st.form(key='formulario_usuario'):
    nombre = st.text_input('Nombre')
    contrasena = st.text_input('Contraseña', type='password')

    col1, col2 = st.columns(2)
    with col1:
        iniciar_sesion = st.form_submit_button('Iniciar sesión')
    with col2:
        registrarse = st.form_submit_button('Registrarse')

# Lógica
if iniciar_sesion:
    if nombre.strip() == "" or contrasena.strip() == "":
        st.warning("Por favor, completa todos los campos.")
    else:
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre=? AND contrasena=?", (nombre, contrasena))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            st.success(f"Bienvenido, {nombre}!")
        else:
            st.error("Usuario o contraseña incorrectos.")

elif registrarse:
    if nombre.strip() == "" or contrasena.strip() == "":
        st.warning("Por favor, completa todos los campos.")
    else:
        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        # Verificar si ya existe un usuario con ese nombre
        cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (nombre,))
        existente = cursor.fetchone()

        if existente:
            st.error("Este nombre de usuario ya está registrado.")
        else:
            cursor.execute("INSERT INTO usuarios (nombre, contrasena) VALUES (?, ?)", (nombre, contrasena))
            conexion.commit()
            st.success(f"¡Usuario {nombre} registrado exitosamente!")

        conexion.close()

