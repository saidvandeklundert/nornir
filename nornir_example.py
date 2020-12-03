"""
Nornir example script.

The intention of this script is to:
- explain what is going on when using Nornir
- give an example to help get started quickly

The following is the content of the configuration files used:
--- # hosts file:
veos01:
  hostname: 10.254.169.50
  groups:
    - arista_eapi
veos02:
  hostname: 10.254.169.51
  groups:
    - arista_eapi


--- # groups:
juniper: { platform: junos, port: 830 }
arista: { platform: eos, port: 22 }
arista_eapi: { platform: eos, port: 443}
cisco_ios: { platform: ios, port: 22 }
cisco_nxos: { platform: nxos, port: 22 }


--- # defaults:
username: admin
password: password


"""
import logging
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_utils.plugins.functions import print_result
from nornir.plugins.inventory.simple import SimpleInventory
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_napalm.plugins.tasks import napalm_configure, napalm_cli, napalm_get
from nornir_netmiko.tasks import netmiko_send_command

logger = logging.getLogger('nornir')

template_string = """
interface loopback 0
description Nornir
"""
    
def main_task(task: Task, example_arg_1, example_arg_2, template_string, dry_run=True) -> Result:
    """
    This is the main task or function of the program. 
    
    We will call several sub tasks from this task.
    """
    
    task.run(
        name="Logging example.",
        task=log_something,
    )
    
    task.run(
        name="example_task",
        task=example_task,
        example_arg_1=example_arg_1,
        example_arg_2=example_arg_2,
    )
    
    result_to_examine = task.run(
        name="examine task",
        task=examine_task,
    )

    task.run(
        name="examine result",
        task=examine_result,
        result = result_to_examine        
    )    
    
    task.run(
        name="example command using NAPALM",
        task=example_command_using_napalm,
    )
    
    task.run(
        name="example using NAPALM getters",
        task=example_napalm_getters,
    )

    task.run(
        name="example configuration using NAPALM",
        task=example_napalm_configure,        
        template_string=template_string,        
        dry_run=dry_run,
    )

    return Result(
        host=task.host,
        result="Example task finished!",
    )


def log_something(task: Task,) -> Result:
    """
    Nornir will log to 'nornir.log' by default.
    """    
    logger.info(f"{task.host.name} says hi!")
    logger.warning("Warning %r is running task %r", task.host.name, task.name)    
    return Result(
        host=task.host,
        result=f"Task {task.name} made some log updates"
    )


def example_task(task: Task, example_arg_1, example_arg_2) -> Result:
    """
    This is an example sub-task that can be used in a Nornir main task.

    Purpose of this task it to return the example arguments.
    """
    task_result = f"Got the following:\nexample_arg_1: {example_arg_1}\nexample_arg_2: {example_arg_2}"
    return Result(
        host=task.host,
        result=task_result
    )


def examine_task(task: Task,) -> Result:
    """
    This task will return information that describes the task object.
    """
    ret_dict ={
        "task" : task,
        "task name" : task.name,
        "host dict" : task.host.dict(),
        "groups content" : task.host.groups[0].dict(),
        "default content" : task.host.defaults.dict(),
        "task methods" : dir(task),
        "host methods" : dir(task.host),
        "task type" : type(task),        
    }
    # to have a detailed look around, consider setting a trace by removing next line's comment:
    #import pdb; pdb.set_trace()
    return Result(
        host=task.host,
        result=ret_dict
    )


def examine_result(task: Task, result) -> Result:
    """
    This task will return information describing the result object.
    """
    ret_dict ={
        "result" : result,
        "result methods" : dir(result),
        "task type" : type(result),        
    }
    # to have a detailed look around, consider setting a trace by removing next line's comment:
    #import pdb; pdb.set_trace()
    return Result(
        host=task.host,
        result=ret_dict
    )


def example_command_using_napalm(task: Task,) -> Result:
    """
    Send commands using napalm_cli
    """
    
    cmd_ret = task.run(
        task=napalm_cli, commands=[
            'show version',
            'show hostname',
            ],
    )
    # In case you want to work with the returns for the individual commands, uncomment the following lines:
    #show_version_output = cmd_ret[0].result['show version']
    #config = cmd_ret[0].result['show hostname']

    return Result(
        host=task.host,
        result=cmd_ret
    )

def example_command_using_netmiko(task: Task,) -> Result:
    """
    Send command using Netmiko.

    (not used in the main task in this example, included as FYI)
    """
    cmd_ret = task.run(
        task=netmiko_send_command,
        command_string='show version',
        )
    
    return Result(
        host=task.host,
        result=cmd_ret
    )
    

def example_napalm_getters(task: Task,) -> Result:
    """
    Example on how to use the NAPALM getters.

    There are a lot more getters, find them here:
        https://napalm.readthedocs.io/en/latest/support/
    """
    napalm_getters = task.run(
        task = napalm_get, getters=["get_facts"],
        )
    
    return Result(
        host=task.host,
        result=napalm_getters
    )


def example_napalm_configure(task: Task, template_string, dry_run=True) -> Result:
    """
    Example on how to use the NAPALM to configure devices.
        
    If dry_run is set to True, this task will only retrieve a diff.
    """
    
    napalm_ret = task.run(
        task=napalm_configure,
        dry_run=dry_run,
        configuration=template_string,
    )
    return Result(
        host=task.host,
        result=napalm_ret
    )


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

    result = nr.run(
        name="Task example and explanation function.",
        task=main_task,
        example_arg_1="arg_1",
        example_arg_2="arg_2",
        template_string=template_string,
        dry_run=True
    )

    print_result(result)