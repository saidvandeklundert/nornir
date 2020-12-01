"""
Nornir example script sending a command using netmiko
"""
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.plugins.inventory.simple import SimpleInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_netmiko.tasks import netmiko_send_command

def get_nornir_cfg():
    """
    Returns the Nornir object.
    """
    InventoryPluginRegister.register("SimpleInventory", SimpleInventory)
    nr = InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                    "host_file": "/inventory/hosts.yaml",
                    "group_file": "/inventory/groups.yaml",
                    "defaults_file": "/inventory/defaults.yaml"
            },
        }
    )
    return nr
    

if __name__ == "__main__":

    
    nr = get_nornir_cfg()

    result = nr.run(netmiko_send_command, command_string="show version")

    print_result(result)

    
