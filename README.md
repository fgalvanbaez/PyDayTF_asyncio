# PyDay TF 2017 asyncio, Ejercicios y Presentación

## Ejercicio: Implementar un servidor de publish/subscribe (broker)

Para implementar el broker se ha de usar dos sockets que escuchen `asyncio.start_server()`
uno en `127.0.0.1` y puerto `8888` para los clientes que sean subscriptores
y otro en `127.0.0.1` y puerto `9999` para los clientes que sean publicadores.

### Protocolo

El protocolo usado para transmitir los datos sera el siguiente.

1. Se asume que existen unos datos que se quieren enviar que son bytes.
2. Se calcula el tamaño en bytes de los datos
3. Se envia un entero de 32 bits con el tamaño de los datos
4. Se envian los datos

El protocolo usado para recivir los datos sera el siguiente.

1. Se lee el entero de 4 bytes para saber el tamaño de los datos
2. Se leen los datos enviados usando el tamaño de los datos del paso anterior

### Comportamiento

Cuando un publicador envie datos han de llegar a todos los subscriptores que esten connectados.

### Tests

Para validar la implementación existen 5 test.

Para correr los test ejecutar en la raiz del proyecto
```
py.test
```

### Recomendación para Setup

Para hacer esta tarea es necesario python 3.5 o mayor

* Instalar virtualenv:
```
apt-get install python-virtualenv
```
 
 
 * Crear el virtualenv estando dentro del directorio del proyecto
```
virtualenv -p $(which python3)
```

* Activamos el virtualenv
```
source ./virtualenv/bin/activate
```

* Instalamos las dependencias
```
pip install -r requirements.txt
```

* Lanzamos los test
```
py.test
```