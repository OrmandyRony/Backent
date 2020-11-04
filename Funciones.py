import pytz
import datetime

class Funcion():
    def __init__(self, pelicula, horario, sala):
        self.pelicula = pelicula
        self.horario = horario
        self.sala = sala
        self.asistentes = self.sala_vacia()
    
    def sala_vacia(self):
        sala = []
        for i in range(12):
            sala.append({"identificador": i+1, "disponible": True})
            return sala
    
    def asientos(self):
        return self.asistentes
    
    def apartar(self, identificador):
        i = identificador - 1
        self.asistentes[i]["disponible"] = False

    def llena(self):
        for asiento in self.asistentes:
            if asiento ["disponible"]:
                return False
            return True

    def disponible(self):
        if self.llena(): 
            return False
        timezone = pytz.timezone('America/Guatemala')
        fecha_completa = datetime.datetime.now(tz = timezone)
        hora = fecha_completa.strftime("%H")
        minutos = fecha_completa.strftime("%M")
        hora_actual = int(hora)
        min_actual = int(minutos)
        tiempo_funcion = self.horario.split(":")
        hora_funcion = int(tiempo_funcion[0])
        min_funcion = int(tiempo_funcion[1])
        if hora_actual > hora_funcion:
            return False
        elif hora_actual == hora_funcion:
            if min_actual > min_funcion:
                return False
        return True