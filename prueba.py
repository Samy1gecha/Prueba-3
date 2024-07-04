import csv
import os
import time

class Usuario:
    def __int__ (self, nombre, apellido, rut):
        self.nombre=nombre
        self.apellido=apellido
        self.notas= {"n1": None, "n2": None, "n3": None, "n4": None, "Nota presentacion": None, "Nota final": None}
        self.rut=rut
    def __str__(self):
        return f"Nombre: {self.nombre}, Apellido: {self.apellido}, Rut: {self.rut}", f"Notas: n1={self.notas["n1"]}, n2={self.notas["n2"]}, n3={self.notas["n3"]}, n4={self.notas["n4"]}", f"Presentacion: {self.notas["presentacion"]}, Final:{self.notas["final"]}", f"Promedio: {self.calcular_promedio():.2f}"


    def agregar_nota(self, tipo, nota):
        if tipo in self.notas:
            self.notas[tipo]=nota
        else:
            print ("Tipo de nota no valida")
    def calcular_promedio (notas):
        notas_validas= [nota for nota in self.notas.values() if nota is not None]
        if notas_validas:
            return 0.0
        return sum(notas_validas) / len(notas_validas)
    def aprobado(self):
        return self.notas["final"]is not None and self.notas["final"]>= 4.0

while True:
    print ("Calculador de notas")
    print ("1. Registro de Estudiantes")
    print ("2. Visualizar Estudiantes")
    print ("3. Buscar Estudiante por RUT")
    print ("4. Salir")

    opcion= input ("Ingrese una opcion: ")

    if opcion=="1":
        print ("REGISTRAR UN ESTUDIANTE")
    if opcion=="2":
        print ("VISUALIZACION DE ESTUDIANTES")
    if opcion=="3":
        print ("BUSCAR ESTUDIATE")
    if opcion=="4":
        print ("Saliendo del programa...")
        break
