import os

productsData = []

def leer_archivo(nombre_archivo):
  try:
    with open(nombre_archivo, 'r') as archivo:
      lineas = archivo.readlines()
      return lineas
  except FileNotFoundError:
    raise FileNotFoundError(f"El archivo '{nombre_archivo}' no fue encontrado")
  
def obtener_tabla_datos() -> str:
    texto_para_tabla = ""

    encabezados = ["Producto", "Cantidad", "Precio Unitario", "Valor Total", "Ubicación"]
    encabezados_formatados = " | ".join(encabezados)
    separador = "-" * len(encabezados_formatados)
    
    texto_para_tabla += encabezados_formatados + "\n"
    texto_para_tabla += separador + "\n"
    
    for producto in productsData:
        nombre = producto['nombre']
        cantidad = producto['cantidad']
        precio_unitario = producto['precio_unitario']
        valor_total = cantidad * precio_unitario
        ubicacion = producto['ubicacion']
        
        # Formatear y alinear los datos
        fila_formatada = "{:<8} | {:<8} | {:<15.2f} | {:<11.2f} | {:<10}".format(
            nombre, cantidad, precio_unitario, valor_total, ubicacion
        )
        
        texto_para_tabla += fila_formatada + '\n'
    return texto_para_tabla
  
def obtener_datos_por_linea(linea: str):
  datos = []
  datos.append(linea.strip().split(";")[0].split(" ")[0]) # el comando
  datos.append(linea.strip().split(";")[0].split(" ")[1])
  datos.extend(linea.strip().split(";")[1:])
  return datos

def buscar_producto(nombre, ubicacion):
    for producto in productsData:
        if producto["nombre"] == nombre and producto["ubicacion"] == ubicacion:
            return producto
    return None

# INICIO PROGRAMA
while True:
  print("USAC - Segundo Semestre 2023")
  print("Práctica 1 - Lenguajes Formales")
  print("Luis Morales - 202208521")
  print("----------------------------")
  print("MENU")
  print("1. Cargar Inventario inicial")
  print("2. Cargar Instrucciones de movimientos")
  print("3. Crear Informe de inventario")
  print("4. Salir")
  option = input("Ingrese el número de opción:")

  if option == "1":
    print("\n")
    print("Ha elegido la opción '1. Cargar Inventario inicial'")
    print("\n")
    
    try:
        nombre_archivo = input("Ingresa el nombre del archivo: ")
        
        if not nombre_archivo.endswith('.inv'):
          print("\n")
          raise ValueError("ERROR: El archivo debe tener extensión .inv")
        else:
          lineas = leer_archivo(nombre_archivo)
          #crear_producto <nombre>;<cantidad>;<precio_unitario>;<ubicacion>
          for linea in lineas:
            dato = obtener_datos_por_linea(linea)
            nombre, cantidad, precio_unitario, ubicacion = dato[1:]
            productsData.append({
              "nombre": nombre,
              "cantidad": int(cantidad),
              "precio_unitario": float(precio_unitario),
              "ubicacion": ubicacion
            })

          print("\n")
          print(f"ÉXITO: El archivo {nombre_archivo} ha sido agregado correctamente")

    except ValueError as ve:
        print(ve)
    except FileNotFoundError as fnfe:
        print(fnfe)
    finally:
       print("\n")
  elif option == "2":
    print("\n")
    print("Ha elegido la opción '2. Cargar Instrucciones de movimientos'")
    print("\n")
    
    try:
        nombre_archivo = input("Ingresa el nombre del archivo: ")
        
        if not nombre_archivo.endswith('.mov'):
          print("\n")
          raise ValueError("El archivo debe tener extensión .mov")
        else:
          lineas = leer_archivo(nombre_archivo)
          
          for linea in lineas:
            dato = obtener_datos_por_linea(linea)
            nombre, cantidad, ubicacion = dato[1:]

            producto_encontrado = buscar_producto(nombre=nombre, ubicacion=ubicacion)

            if producto_encontrado:
              #agregar_stock <nombre>;<cantidad>;<ubicacion>
              if dato[0] == "agregar_stock":
                producto_encontrado["cantidad"] += int(cantidad)
                print("\n")
                print("ÉXITO: Cantidad actualizada exitosamente.")
                print("\n")

              #vender_producto <nombre>;<cantidad>;<ubicacion>
              elif dato[0] == "vender_producto":
                if producto_encontrado["cantidad"] >= int(cantidad):
                  producto_encontrado["cantidad"] -= int(cantidad)
                  print("\n")
                  print("ÉXITO: Productos vendidos exitosamente.")
                else:
                  print("\n")
                  print("Error: La cantidad que quiere vender es mayor que la cantidad de productos existentes")
            else:
              print("\n")
              print("Error: Producto no encontrado.")
              
    except ValueError as ve:
        print(ve)
    except FileNotFoundError as fnfe:
        print(fnfe)
    finally:
       print("\n")

  elif option == "3":
    print("\n")
    print("Ha elegido la opción '3. Crear Informe de inventario'")
    print("\n")

    ruta = r'C:\Users\DELL\Desktop\archivo.txt'

    try:
        if os.path.exists(os.path.dirname(ruta)):
            with open(ruta, 'w') as archivo:
                archivo.write(obtener_tabla_datos())
                
            print("\n")
            print("TERMINADO: Archivo creado exitosamente en el escritorio.")
            print("\n")
        else:
            print("La ruta del escritorio no existe.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

  elif option == "4":
   print("\n")
   print("HAS SALIDO DE LA APLICACIÓN")
   print("\n")
   break