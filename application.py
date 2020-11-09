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
resenas = []
registro_funcion = []

usuario_maestro= Usuario("Usuario", "Maestro", "admin", "admin", "Administrador" )
usuarios.append(usuario_maestro)

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
    previous_usuario = dato['previous_usuario']
    nombre = dato['nombre']
    apellido = dato['apellido']
    usuario = dato['usuario']
    contrasena = dato['contrasena']
    global usuarios
    for usuario in usuarios:
        if usuario.usuario == previous_usuario:
            usuario.usuario = previous_usuario
            usuario.nombre = nombre
            usuario.apellido = apellido
            usuario.usuario = contrasena
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

def actualizar_funcion(pelicula, new_pelicula):
    """
    Actualiza una funcion.
    """
    global funciones 
    for funcion in funciones:
        if funcion.pelicula == pelicula:
            funcion.pelicula = new_pelicula
            
@app.route('/eliminarFuncion', methods=['POST'])
def eliminar_funcion():
    """
    Elimina una funcion
    """
    dato = request.get_json()
    identificador = dato['identificador']
    global funciones
    funciones.pop(identificador)
    return jsonify({'mensaje': 'Funcion eliminada'})
    
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
    pelicula = request.args.get('pelicula')
    global funciones
    print(pelicula)
    for funcion in funciones:
        if funcion.pelicula == pelicula:
            return jsonify(funcion.asientos())
    return jsonify({"mensaje": "No existe esta función"})

@app.route('/apartarAsientos', methods=['POST'])
def apartarAsientos():
    cuerpo = request.get_json()
    pelicula = cuerpo['pelicula']
    identificador = cuerpo['identificador']
    global funciones
    for funcion in funciones:
        if funcion.pelicula == pelicula:
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
            actualizar_funcion(pelicula, new_pelicula)
            peliculas[i]['pelicula'] = new_pelicula
            peliculas[i]['url_imagen'] = new_url_imagen
            peliculas[i]['puntuacion'] = new_puntuacion
            peliculas[i]['duracion'] = new_duracion
            peliculas[i]['sinopsis'] = new_sinopsis
            break
    return jsonify({"mensaje": "Pelicula editada correctamente"})

@app.route('/editarFuncion', methods=['POST'])
def editar_funcion():
    """
    Esto hacerlo con sala
    """
    dato = request.get_json()
    pelicula = dato['pelicula']
    new_pelicula = dato['new_pelicula']
    new_sala = dato['new_sala']
    new_horario = dato['new_horario']
    global funciones
    for funcion in funciones:
        if funcion.pelicula == pelicula:
            funcion.pelicula = new_pelicula
            funcion.sala =new_sala
            funcion.horario = new_horario
    return jsonify({'mensaje': 'Funcion editada con exito'})

@app.route('/eliminarPelicula', methods=['POST'])
def eliminar_pelicula():
    dato = request.get_json()
    identificador = dato['identificador']
    global peliculas
    peliculas.pop(identificador)
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


@app.route('/ingresarResena', methods=['POST'])
def resena():
    dato = request.get_json()
    nombre = dato['nombre']
    comentario = dato['comentario']
    pelicula = dato['pelicula']
    global resenas
    resenas.append({'nombre': nombre, 'comentario': comentario, 'pelicula': pelicula})
    return jsonify({'mensaje': "Reseña agregada"})

@app.route('/obtenerResena', methods=['GET'])
def obtener_resena():
    return jsonify(resenas)

@app.route('/registroAsistente', methods=['POST'])
def registro_asistentes():
    dato = request.get_json()
    usuario = dato['usuario']
    pelicula = dato['pelicula']
    global registro_funcion
    registro_funcion.append({'usuario': usuario, 'pelicula': pelicula})
    return jsonify({'mensaje': 'Usuario asignado a una funcion'})

@app.route('/obtenerRegistro', methods=['GET'])
def obtener_registro():
    return jsonify(registro_funcion)

if __name__ == '__main__':
    puerto = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=puerto)