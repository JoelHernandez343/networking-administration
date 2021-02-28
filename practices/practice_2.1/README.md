# Enrutamiento múltiple | Práctica 2.1
## Descripción

Desarrollar un programa en Python que sea capaz de levantar el enrutamiento estático y dinámico de la columna vertebral de una topología con múltiples métodos de enrutamiento.

Implementar en GNS3 la siguiente topología, donde únicamente se van a configurar las interfaces indicadas en enrutadores, MV y VPCS y un usuario `admin` con contraseña `admin` en ssh de los enrutadores.

Desarrollar un programa en Python que correrá en la máquina virtual host1 y que sea capaz
levantar los distintos métodos de enrutamiento indicados en la topología y permitir que exista conectividad en toda la red.

Se creó la siguiente topología de red:

![topology](./docs/images/topology.jpg)

El programa no contendrá ninguna dirección IP y deberá de ser capaza de ir localizando los diferentes router (por su nombre), así como levantar los tipos de enrutamiento según la siguiente tabla:

Enrutador | Estático | RIP | OSPF
--- | --- | --- | ---
R1 | Sí | |
R2 | | Sí | 
R3 | | | Sí 
R4 | Sí | Sí | Sí 


**NOTAS**
- Se utilizó el router **c7200**

## Configuración

### Tabla de configuración de direcciones

(Las interfaces pueden variar)

<table>
<thead>
  <tr>
    <th>Dispositivos</th>
    <th>Interfaz</th>
    <th>IP</th>
    <th>Prefijo</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">R1</td>
    <td>Fa0/0</td>
    <td>192.168.122.65</td>
    <td>26</td>
  </tr>
  <tr>
    <td>Fa0/1</td>
    <td>192.168.122.137</td>
    <td>30</td>
  </tr>
  <tr>
    <td>Fa1/0</td>
    <td>192.168.122.129</td>
    <td>30</td>
  </tr>
  <tr>
    <td>Fa1/1</td>
    <td>192.168.122.133</td>
    <td>30</td>
  </tr>
  <tr>
    <td rowspan="1">R2</td>
    <td>Fa0/0</td>
    <td>192.168.122.130</td>
    <td>30</td>
  </tr>
  <tr>
    <td rowspan="2">R3</td>
    <td>Fa0/0</td>
    <td>192.168.122.1</td>
    <td>26</td>
  </tr>
  <tr>
    <td>Fa0/1</td>
    <td>192.168.122.138</td>
    <td>30</td>
  </tr>
  <tr>
    <td rowspan="1">R4</td>
    <td>Fa0/0</td>
    <td>192.168.122.134</td>
    <td>30</td>
  </tr>
  <tr>
    <td rowspan="1">Python</td>
    <td>Et0</td>
    <td>192.168.122.100</td>
    <td>26</td>
  </tr>
  <tr>
    <td rowspan="1">PC2</td>
    <td>Et0</td>
    <td>192.168.122.50</td>
    <td>26</td>
  </tr>
</tbody>
</table>

### Configuración individual de cada dispositivo

- [R1](./docs/configuration/r1.md)
- [R2](./docs/configuration/r2.md)
- [R3](./docs/configuration/r3.md)
- [R4](./docs/configuration/r4.md)

## Uso

Se crea un ambiente virtual de python y se activa:

```bash
python3 -m venv env
source env/bin/activate
```

Se instalan los paquetes via pip (**require conexión a internet**):

```bash
pip install -r requirements.txt
```

Se instalan los paquetes via npm (**require conexión a internet**):

```bash
npm install
```

Se compilan las fuentes de letra y el framework de utilidades Tailwindcss:

```bash
npm run gulp
```

Finalmente, corremos el servidor Flask:

```bash
npm start
```

Abrimos el navegador en localhost en el puerto 5000:

[http://localhost:5000/](http://localhost:5000/)

**Para desactivar el ambiente virtual**
```bash
deactivate
```