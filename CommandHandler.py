import subprocess
import ExtFunctions
from Store import ConfigStore


class format_dict(dict):
    def __missing__(self, key):
        return "{{{key}}}".format(key=key)

class CommandHandler:

    def __init__(self) -> None:
        pass

    def extFunctions(self):
        return ExtFunctions.ExtFunctions()

    def getInput(self, name):
        if not name:
            return [None, None]
        name, flag, *_ = [*name.split(':'), *[None]*2]
        if flag == "var":
            return [subprocess.PIPE, ConfigStore.config['variables'].get(name, '').encode()]
        return [open(name, flag or 'r'), None]

    def getIO(self, name):
        if not name:
            return [open(ConfigStore.config['default']['log_file'], 'a'), None]
        name, flag, *_ = [*name.split(':'), *[None]*2]
        if flag == "var":
            return [subprocess.PIPE, name]
        return [open(name, flag or 'w+'), None]


    def exec_command(self, command, out, err, inp=None):
        print(" ".join(command))
        outIO, outName = self.getIO(out)
        errIO, errName = self.getIO(err)

        stdInput, inValueOrName = self.getInput(inp)
        process = subprocess.Popen(command, stdin=stdInput, stdout=outIO, stderr=errIO)

        try:
            out, err = process.communicate(input=inValueOrName)
        except Exception as e:
            print(inValueOrName, e)
        if out or outIO == subprocess.PIPE:
            if outName:
                ConfigStore.updateConfig(outName, out)
            else:
                print(out)
        if err or outIO == subprocess.PIPE:
            if errName:
                ConfigStore.updateConfig(errName, err)
            else:
                print(err, file=errIO)

        if outIO != subprocess.PIPE:
            outIO.close()
        if errIO != subprocess.PIPE:
            errIO.close()
        return process


    def handle_commands(self, command, out, err, inp, *args):
        if command[0].startswith('func:'):
            func = command[0][5:]
            command = command[1:]
            if func == "foreach_exec":
                process = self.extFunctions().foreach_exec(command, out, err, inp,  *args)
            else:
                raise Exception(f'{command} not exist')
        elif command[0].startswith('dyn_func:'):
            func = command[0][9:]
            outIO, outName = self.getIO(out)
            errIO, errName = self.getIO(err)
            stdInput, inName = self.getInput(inp)
            outFileOrVar = outIO if outIO != subprocess.PIPE else outName
            errFileOrVar = errIO if errIO != subprocess.PIPE else errName
            inFileOrVar = stdInput if stdInput != subprocess.PIPE else inName
            process = getattr(self.extFunctions(), func)(outFileOrVar, errFileOrVar, inFileOrVar, *args)
            if outIO != subprocess.PIPE:
                outIO.close()
            if errIO != subprocess.PIPE:
                errIO.close()
        else:
            process = self.exec_command(command, out, err, inp)
        
            
        return process