[Back to README.md](./../../README.md)

Configuration for ESW3 (just copy and paste):
```
# ssh configuration and user creation
config t

ip domain-name adminredes.escom.ipn.mx

ip ssh rsa keypair-name sshkey
crypto key generate rsa usage-keys label sshkey modulus 1024

ip ssh v 2
ip ssh time-out 30
ip ssh authentication-retries 3
line vty 0 15
password cisco
login local
transport input ssh
exit

username cisco privilege 15 password cisco

# Interfaces

int f 1/4
chann 2 mode on
int f 1/5
chann 2 mode on
int f 1/6
chann 2 mode on
int f 1/7
chann 2 mode on
exit

int p 2
sw mode tru
sw tru all vl all

exit 

int f 1/14
sw mode trunk
sw trunk all vlan all

int vlan 1
ip add 192.168.1.13 255.255.255.0
no shu

exit
exit

# Vlan

vlan data
vtp dom admim-vlan
vtp pass 1234678
vtp v2
vtp pruning v2
vtp client
exit

```