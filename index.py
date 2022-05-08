import os
from CommandHandler import CommandHandler as CH
from CommandHandler import format_dict

from Store import ConfigStore


commands_out_err_args_before_process = ConfigStore.config.get('commands_out_err_args')

commands_out_err_args = []

for i in commands_out_err_args_before_process:
    if isinstance(i, str):
        commands = ConfigStore.config.get('chains',{}).get(i, None)
        if commands:
            commands_out_err_args = [*commands_out_err_args, *commands]
    else:
        commands_out_err_args = [*commands_out_err_args, i]



project_domain_list = ConfigStore.config.get('project_domain_list')
path = os.path.dirname(os.path.realpath(__file__))

def getFromArray(arr, index, default = None):
    try:
        return arr[index]
    except IndexError:
        return default

def CommandHandler():
    return CH()


current_vars = format_dict({
    'path': path,
    'line': '{line}',
    **ConfigStore.config.get('variables')
})

for project, domain_list_file, inScope in project_domain_list:
    if not inScope:
        continue
    current_vars['project'] = project
    current_vars['domain_list_file'] = domain_list_file
    for command, *args in commands_out_err_args:
        current_vars = format_dict({**current_vars, **ConfigStore.config['variables']})
        out = getFromArray(args, 0)
        err = getFromArray(args, 1)
        inp = getFromArray(args, 2)
        args = args[3:]
        command = list(map(lambda x:x.format_map(current_vars), command))
        if out:
            out = out.format_map(current_vars)
        if err:
            err = err.format_map(current_vars)
        if inp:
            inp = inp.format_map(current_vars)
        try:
            args = list(map(lambda x:x.format_map(current_vars) if isinstance(x,str) else x, args))
        except Exception:
            print(args)
        process = CommandHandler().handle_commands(command, out, err, inp, *args )

exit()
