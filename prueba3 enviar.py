import csv
import os
import time

# Definición de códigos ANSI para colores en la consola
COLOR_VERDE = '\033[92m'
COLOR_ROJO = '\033[91m'
RESET_COLOR = '\033[0m'

class Usuario:
    def __init__(self, nombre, apellido, rut):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.notas = {"n1": None, "n2": None, "n3": None, "n4": None, "examen": None, "final": None}

    def __str__(self):
        nota_presentacion = self.calcular_nota_presentacion()
        nota_examen = self.notas["examen"]
        
        notas_str = f"Nota de Presentación={self.formatear_nota(nota_presentacion)}" if nota_presentacion is not None else "Nota de Presentación=N/A"
        notas_str += f", Examen={self.formatear_nota(nota_examen)}" if nota_examen is not None else ", Examen=N/A"
        
        estado = "Aprobado" if self.esta_aprobado() else "Reprobado"
        if self.esta_aprobado():
            estado_coloreado = f"{COLOR_VERDE}{estado}{RESET_COLOR}"
        else:
            estado_coloreado = f"{COLOR_ROJO}{estado}{RESET_COLOR}"

        return (f"Nombre: {self.nombre}, Apellido: {self.apellido}, RUT: {self.rut}, "
                f"Notas: {notas_str}, Estado: {estado_coloreado}")

    def agregar_nota(self, tipo, nota):
        if tipo in self.notas:
            self.notas[tipo] = nota
        else:
            print("Tipo de nota no válido.")

    def calcular_nota_presentacion(self):
        notas_validas = [nota for key, nota in self.notas.items() if key.startswith("n") and nota is not None]
        if not notas_validas:
            return None
        return sum(notas_validas) / len(notas_validas)

    def calcular_nota_final(self):
        nota_presentacion = self.calcular_nota_presentacion()
        nota_examen = self.notas["examen"]
        if nota_presentacion is None or nota_examen is None:
            return None
        nota_final = 0.6 * nota_presentacion + 0.4 * nota_examen
        return nota_final

    def esta_aprobado(self):
        nota_final = self.calcular_nota_final()
        return nota_final is not None and nota_final >= 4.0

    def formatear_nota(self, nota):
        return int(nota) if nota.is_integer() else f"{nota:.1f}".replace('.', ',')

class SistemaUsuarios:
    def __init__(self, archivo_csv):
        self.usuarios = {}
        self.archivo_csv = archivo_csv
        self.cargar_usuarios()

    def cargar_usuarios(self):
        try:
            with open(self.archivo_csv, mode='r', newline='') as archivo:
                lector = csv.reader(archivo)
                for fila in lector:
                    if len(fila) >= 9:  # Ahora se espera final como última nota
                        nombre, apellido, rut, n1, n2, n3, n4, examen, final = fila[:9]
                        usuario = Usuario(nombre, apellido, rut)
                        usuario.notas["n1"] = float(n1.replace(',', '.')) if n1 else None
                        usuario.notas["n2"] = float(n2.replace(',', '.')) if n2 else None
                        usuario.notas["n3"] = float(n3.replace(',', '.')) if n3 else None
                        usuario.notas["n4"] = float(n4.replace(',', '.')) if n4 else None
                        usuario.notas["examen"] = float(examen.replace(',', '.')) if examen else None
                        usuario.notas["final"] = float(final.replace(',', '.')) if final else None
                        self.usuarios[self.normalizar_rut(rut)] = usuario
        except FileNotFoundError:
            print("El archivo no existe. Se creará uno nuevo al guardar usuarios.")

    def guardar_usuarios(self):
        with open(self.archivo_csv, mode='w', newline='') as archivo:
            escritor = csv.writer(archivo)
            for usuario in self.usuarios.values():
                escritor.writerow([usuario.nombre, usuario.apellido, usuario.rut,
                                   self.formatear_nota(usuario.notas["n1"]), self.formatear_nota(usuario.notas["n2"]),
                                   self.formatear_nota(usuario.notas["n3"]), self.formatear_nota(usuario.notas["n4"]),
                                   self.formatear_nota(usuario.notas["examen"]), self.formatear_nota(usuario.notas["final"])])

    def crear_usuario(self):
        nombre = input("Ingrese el nombre: ").strip()
        apellido = input("Ingrese el apellido: ").strip()
        rut = input("Ingrese el RUT: ").strip()

        if nombre == "" or apellido == "" or rut == "":
            print("Error: No se permiten campos vacíos. Intente de nuevo.")
            time.sleep(3)
            limpiar_pantalla()
            return

        # Convertir 'k' minúscula a mayúscula si es el dígito verificador
        if rut[-1].lower() == 'k':
            rut = rut[:-1] + 'K'

        # Validar que el RUT contenga solo números y opcionalmente la letra 'K' al final
        rut_valido = rut[:-1].isdigit() and (rut[-1].upper() == 'K' or rut[-1].isdigit())
        if not rut_valido:
            print("Error: El RUT debe contener solo números y la letra 'K' opcional al final.")
            time.sleep(3)
            limpiar_pantalla()
            return

        rut_normalizado = self.normalizar_rut(rut)
        if rut_normalizado in self.usuarios:
            print("El usuario ya existe. Intente con otro RUT.")
            time.sleep(3)
            limpiar_pantalla()
            return

        self.usuarios[rut_normalizado] = Usuario(nombre, apellido, rut)
        self.guardar_usuarios()
        print("Usuario creado exitosamente.")
        time.sleep(3)
        limpiar_pantalla()

    def mostrar_usuarios(self):
        if not self.usuarios:
            print("No hay usuarios registrados.")
            time.sleep(3)
            limpiar_pantalla()
            return

        print("\nRegistros guardados:")
        for usuario in self.usuarios.values():
            print(usuario)
            print("")

        time.sleep(3)
        limpiar_pantalla()

    def agregar_nota_usuario(self):
        rut = input("Ingrese el RUT del usuario: ").strip()
        rut_normalizado = self.normalizar_rut(rut)
        
        if rut_normalizado not in self.usuarios:
            print("El usuario no existe. Intente con otro RUT.")
            time.sleep(3)
            limpiar_pantalla()
            return

        tipo = input("Ingrese el tipo de nota (n1, n2, n3, n4, examen): ").strip().lower()
        if tipo not in self.usuarios[rut_normalizado].notas:
            print("Tipo de nota no válido.")
            time.sleep(3)
            limpiar_pantalla()
            return

        try:
            nota_input = input("Ingrese la nota (puede usar ',' o '.'): ").strip()
            nota = float(nota_input.replace(',', '.'))  # Convertir nota a float
            if nota > 7.0:
                print("Error: La nota no puede ser mayor a 7,0.")
                time.sleep(3)
                limpiar_pantalla()
                return
            self.usuarios[rut_normalizado].agregar_nota(tipo, nota)
            self.guardar_usuarios()
            print("Nota agregada exitosamente.")
        except ValueError:
            print("Error: La nota debe ser un número.")
        
        time.sleep(3)
        limpiar_pantalla()

    def mostrar_usuario_por_rut(self):
        rut = input("Ingrese el RUT del usuario: ").strip()
        rut_normalizado = self.normalizar_rut(rut)
        
        if rut_normalizado not in self.usuarios:
            print("El usuario no existe. Intente con otro RUT.")
            time.sleep(3)
            limpiar_pantalla()
            return

        usuario = self.usuarios[rut_normalizado]
        print("\nInformación del usuario:")
        print(usuario)
        if usuario.esta_aprobado():
            print(f"Estado: {COLOR_VERDE}Aprobado{RESET_COLOR}")
        else:
            print(f"Estado: {COLOR_ROJO}Reprobado{RESET_COLOR}")

        time.sleep(3)
        limpiar_pantalla()

    def normalizar_rut(self, rut):
        return rut.replace("-", "").replace(".", "")

    def formatear_nota(self, nota):
        if nota is None:
            return ""
        return str(int(nota)) if nota.is_integer() else f"{nota:.1f}".replace('.', ',')

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    sistema = SistemaUsuarios("usuarios.csv")
    while True:
        print("-- MENÚ DE NOTAS --")
        print("1. Crear usuario")
        print("2. Mostrar todos los registros")
        print("3. Agregar nota a un usuario")
        print("4. Buscar y mostrar usuario por RUT")
        print("5. Salir")
        opcion = input("Ingrese el número de la opción deseada: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            sistema.crear_usuario()
        elif opcion == "2":
            limpiar_pantalla()
            sistema.mostrar_usuarios()
        elif opcion == "3":
            limpiar_pantalla()
            sistema.agregar_nota_usuario()
        elif opcion == "4":
            limpiar_pantalla()
            sistema.mostrar_usuario_por_rut()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()