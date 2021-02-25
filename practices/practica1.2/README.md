# Configuración automática de SSH por Telnet | Práctica 1.2
## Descripción

Se creó la siguiente topología de red:

![topology](./docs/images/topology.jpg)

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

Usando Python 3:
```bash
python configure_ssh.py
```

Salida:

![output](./docs/images/output.jpg)