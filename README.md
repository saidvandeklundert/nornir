## Nornir overview

Automation framework with the following characteristics:
- minimal
- pure Python
- total freedom



## installing nornir

Can be installed using pip:
```
pip3 install nornir
```

Nornir has plugins available that make it easier to interface with certain other libraries. Installing some plugins:
```
pip3 install nornir_napalm
pip3 install nornir_utils
pip3 install nornir_jinja2
```


## Mandatory files:

config

hosts
groups
defaults


## logging in Nornir

Log output is directed to `nornir.log`.


## statistics

Statistics writing facts for IOS switches:
500 devices in 2m2
1000 devices in 3m43




## Filtering

### Using platform:

```python
ios_routers = nr.filter(platform='ios')
```

### Using tags:

You can add tags to the hosts:

```yaml
bms_0:
  hostname: 10.0.189.107
  groups:
  - cisco_ios
  data:
    tags:
      - batch_1
bms_1:
  hostname: 10.198.50.170
  groups:
  - cisco_ios
  data:
    tags:
      - batch_3 
```

After doing so, you can filter on these tags like this:
```python
batch_1 = nr.filter(F(tags__contains='batch_1'))
batch_2 = nr.filter(F(tags__contains='batch_2'))
batch_3 = nr.filter(F(tags__contains='batch_3'))
```

>>> nr.inventory.hosts['bms_0'].groups
[Group: cisco]
>>> nr.inventory.hosts['bms_0'].hostname
'10.0.189.107'
>>> nr.inventory.hosts['bms_0'].password
'salty_mcsaltface'
>>> nr.inventory.hosts['bms_0'].username
'salt_nettools'
>>> nr.inventory.groups['cisco'].username
'salt_nettools'


>>> nr.filter(hostname="10.0.189.107").inventory.hosts.keys()
dict_keys(['bms_0'])

nr.inventory.children_of_group("cisco")


## Interesting links:

Official documentation:
https://nornir.readthedocs.io/en/latest/

Discourse group:
https://nornir.discourse.group/


Uses threads to scale:
(old doc) https://nornir.readthedocs.io/en/latest/plugins/execution_model.html?highlight=execution

Debugging:
https://nornir.readthedocs.io/en/latest/howto/ipdb_how_to_use_it_with_nornir.html

configure(template_string = 'set interfaces lo0 unit 0 description yolo', hostname='198.18.60.41', username='admin', password='xx', diff=True,)