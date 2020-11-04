from flask import Flask, request, jsonify
import json 
import os
from flask_cors import CORS, cross_origin
from Usuario import Usuario
from Funciones import Funcion

app = Flask(__name__)
CORS(app)
usuarios = []
funciones = []
peliculas = []
datos = {}


@app.route('/', methods=['GET'])
def inicio():
    return "Cinella"

@app.route('/signup', methods=['POST'])
def signup():
    """
    Ingresa los datos del usuario y los almacena la lista de usuarios.
    :return: un mensaje de confimacion que se a agregado el usuario.
    """
    cuerpo = request.get_json()
    nombre = cuerpo['nombre']
    apellido = cuerpo['apellido']
    usuario = cuerpo['usuario']
    contrasena = cuerpo['contrasena']
    tipo = cuerpo['tipo']
    nuevo_usuario = Usuario(nombre, apellido, usuario, contrasena, tipo)
    global usuarios
    usuarios.append(nuevo_usuario)
    return jsonify({'mensaje': 'Registrado correctamente'})

@app.route('/obtenerUsuarios', methods=['GET'])
def obtener_usuarios():
    """
    Obtiene todos los usuarios que an sido registrados en la lista de usuarios.
    :return: un json con los datos de los usuarios.
    """
    json_usuarios = []
    global usuarios
    for usuario in usuarios:
        json_usuarios.append({"nombre": usuario.nombre, "apellido": usuario.apellido, "usuario": usuario.usuario, "contrasena": usuario.contrasena, "tipo": usuario.tipo})
    return jsonify(json_usuarios)

@app.route('/editar', methods=['POST', 'GET'])
def editar_usuario():
    dato = request.get_json()
    nombre = dato['nombre']
    apellido = dato['apellido']
    usuario = dato['usuario']
    contrasena = dato['contrasena']
    global datos

    for i in range(len(usuarios)):
        if usuarios[i]['usuario'] == datos[i]['usuario']:
            usuarios[i]['nombre'] = nombre
            usuarios[i]['apellido'] = apellido
            usuarios[i]['usuario'] = usuario
            usuarios[i]['contrasena'] = contrasena
            break
    return jsonify({"mensaje": "El usuario se edito"})

@app.route('/agregarFuncion', methods=['POST'])
def agregarFuncion():
    """
    Agrega los datos de la funcion a la lista de funciones como un objeto Funcion.
    :return: una mensaje indicando que a funcion a sido agregada
    """
    dato = request.get_json()
    pelicula = dato['pelicula']
    sala = dato['sala']
    horario = dato['horario']
    nueva_funcion = Funcion(pelicula, horario, sala)
    global funciones
    funciones.append(nueva_funcion)
    return jsonify({'mensaje': 'La funcion a sido agregada correctamente'})

@app.route('/obtenerFunciones', methods=['GET'])
def obtenerFunciones():
    """
    Obtiene todas las funciones que an sido ingresadas.
    :return: un json con los datos de cada funcion.
    """
    json_funciones = []
    global funciones
    for funcion in funciones:
        if (funcion.disponible()):
            disponible = "Si"
        if not(funcion.disponible()):
            disponible = "No"
        json_funciones.append({'pelicula': funcion.pelicula, 'horario': funcion.horario, 'sala': funcion.sala, 'disponible': disponible })
    return jsonify(json_funciones)

@app.route('/obtenerSala', methods=['GET'])
def obtenerSala():
    nombre = request.args.get('nombre')
    global funciones
    for funcion in funciones:
        if funcion.nombre == nombre:
            return jsonify(funcion.asientos())
    return jsonify({"mensaje": "No existe esta función"})

@app.route('/apartar', methods=['POST'])
def apartarAsientos():
    cuerpo = request.get_json()
    nombre = cuerpo['nombre']
    identificador = cuerpo['identificador']
    global funciones
    for funcion in funciones:
        if funcion.nombre == nombre:
            funcion.apartar(identificador)
    return jsonify({"mensaje": "apartado correctamente"})

@app.route('/editarPelicula', methods=['POST'])
def editar_pelicula():
    dato = request.get_json()
    pelicula = dato['pelicula']
    new_pelicula = dato['new_pelicula']
    new_url_imagen = dato['new_url_imagen']
    new_puntuacion = dato['new_puntuacion']
    new_duracion = dato['new_duracion']
    new_sinopsis = dato['new_sinopsis']
    global peliculas
    for i in range(len(peliculas)):
        if peliculas[i]['pelicula'] == pelicula:
            peliculas[i]['titulo'] = new_pelicula
            peliculas[i]['url_imagen'] = new_url_imagen
            peliculas[i]['puntuacion'] = new_puntuacion
            peliculas[i]['duracion'] = new_duracion
            peliculas[i]['sinopsis'] = new_sinopsis
            break
    
    return jsonify({"mensaje": "Pelicula editada correctamente"})

@app.route('eliminarPelicula', methods=['POST'])
def eliminar_pelicula():
    dato = request.get_json()
    nombre_pelicula = dato['pelicula']
    global peliculas
    for pelicula in peliculas:
        if pelicula.pelicula == nombre_pelicula:
            pelicula.pop
    return jsonify({'mensaje': "La pelicula a sido eliminada"})

@app.route('/obtenerPeliculas', methods=['GET'])
def obtener_peliculas():
    return jsonify(peliculas)

@app.route('/leerArchivo', methods=['POST'])
def leer_archivo():
    dato = request.get_json()
    contenido = dato['contenido']
    filas = contenido.split("\r\n")
    global peliculas
    for fila in filas:
        columna = fila.split(",")
        peliculas.append({'pelicula': columna[0], 'url_imagen': columna[1], 'puntuacion': columna[2], 'duracion': columna[3], 'sinopsis': columna[4]})
    return jsonify(peliculas)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)