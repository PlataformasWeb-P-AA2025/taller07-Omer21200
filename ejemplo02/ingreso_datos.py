import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# se importa la clase(s) del 
# archivo genera_tablas
from genera_tablas import Club, Jugador

# se importa información del archivo configuracion
from configuracion import cadena_base_datos
# se genera enlace al gestor de base de
# datos
# para el ejemplo se usa la base de datos
# sqlite
engine = create_engine(cadena_base_datos)

Session = sessionmaker(bind=engine)
session = Session()

# Se crea la sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()

# 1. Cargar datos de clubes desde el archivo de texto
ruta_clubs = os.path.join("data", "datos_clubs.txt")  # Ruta del archivo
with open(ruta_clubs, encoding='utf-8') as archivo:
    for linea in archivo:
        datos = linea.strip().split(";")  # Separar por ";"
        if len(datos) == 3:
            nombre, deporte, fundacion = datos
            # Crear objeto Club
            club = Club(nombre=nombre, deporte=deporte, fundacion=int(fundacion))
            session.add(club)  # Agregar a la sesión (no guarda aún)

# Guardar todos los clubes en la base de datos
session.commit()

# 2. Crear un diccionario {nombre_club: objeto Club}
#    para facilitar la asociación de jugadores
clubes_dict = {c.nombre: c for c in session.query(Club).all()}

# 3. Cargar datos de jugadores desde el archivo de texto
ruta_jugadores = os.path.join("data", "datos_jugadores.txt")
with open(ruta_jugadores, encoding='utf-8') as archivo:
    for linea in archivo:
        datos = linea.strip().split(";")  # Separar por ";"
        if len(datos) == 4:
            nombre_club, posicion, dorsal, nombre_jugador = datos
            club = clubes_dict.get(nombre_club)  # Buscar el club correspondiente
            if club:  # Solo si el club existe
                try:
                    dorsal = int(dorsal)  # Convertir dorsal a entero
                except ValueError:
                    continue  # Omitir si el dorsal no es un número

                # Crear objeto Jugador con relación al Club
                jugador = Jugador(
                    nombre=nombre_jugador,
                    posicion=posicion,
                    dorsal=dorsal,
                    club=club  # Esto asigna automáticamente club_id
                )
                session.add(jugador)  # Agregar a la sesión

# Guardar todos los jugadores en la base de datos
session.commit()