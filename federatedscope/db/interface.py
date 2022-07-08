import logging


class Interface(object):
    def __init__(self):
        pass

    def get_input(self):
        tmp = ""
        # Main loop in the interface
        print('get input')
        while True:
            cmds = input(">").strip().split(";")
            cmds[0] = " ".join([tmp, cmds[0]]).strip()
            tmp = cmds[-1]
            # Process the commands
            for cmd in cmds:
                if len(cmd) == 0:
                    continue
                yield cmd

    def print(self, feedback):
        print(feedback)

    def end(self):
        print("Bye")