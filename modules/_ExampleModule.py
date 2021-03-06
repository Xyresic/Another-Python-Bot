from modules import _BaseModule

class Module(_BaseModule.BaseModule):

    # Defines the command that triggers the module
    cmd = ".example_command"

    def __init__(self, msg, share):
        super(Module, self).__init__(msg, share)

    def main(self):
        
        # Send "Hello World!" to the user/channel that triggered the command
        self.sendmsg("Hello World!")
        return
