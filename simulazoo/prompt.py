import argparse

import cmd2
import names

from .enclosure import Enclosure, fill_default_enclosure


class SimulazooPrompt(cmd2.Cmd):
    prompt = "simulazoo>"
    intro = "Welcome! Type ? to list commands"

    enclosure = None

    def do_exit(self, inp):
        "exit the application."
        print("Bye")
        return True

    def help_exit(self):
        print("exit the application. Shorthand: x q Ctrl-D.")

    def _check_enclosure(self):
        if self.enclosure is None:
            self.perror("You need to create an Enclose before using this command.")
            return False
        return True

    enclosure_parser = cmd2.Cmd2ArgumentParser()
    enclosure_parser.add_argument("name", nargs="?", help="enclosure name")

    @cmd2.with_argparser(enclosure_parser)
    def do_create_enclosure(self, args):
        "Create a new enclosure"
        if self.enclosure:
            self.perror("An enclosure already exists")
        else:
            self.enclosure = Enclosure(name=args.name or names.get_full_name())

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument("file", type=argparse.FileType("r"), help="input file")

    @cmd2.with_argparser(load_parser)
    def do_load_config(self, args):
        "Load configuration file. Usefull for first run."
        if self._check_enclosure():
            self.enclosure.load_from_config_file(args.file)

    @cmd2.with_argparser(load_parser)
    def do_load(self, args):
        "Load file generated with save"
        if self._check_enclosure():
            self.enclosure.load_from_file(args.file)

    save_parser = cmd2.Cmd2ArgumentParser()
    save_parser.add_argument("file", type=argparse.FileType("w"), help="output file")

    @cmd2.with_argparser(save_parser)
    def do_save(self, args):
        "Output file to save current state"
        if self._check_enclosure():
            self.enclosure.save_to_file(args.file)

    def do_process_day(self, args):
        "Simulate a day in the enclosure"
        if self._check_enclosure():
            self.enclosure.process_day(log_report=False)

    def do_report(self, args):
        "Print enclosure report"
        if self._check_enclosure():
            report = self.enclosure.build_report()
            self.poutput(report)

    def do_fill(self, args):
        "Fill the Enclosure with default data"
        if self._check_enclosure():
            fill_default_enclosure(self.enclosure)


if __name__ == "__main__":
    import sys

    app = SimulazooPrompt()
    sys.exit(app.cmdloop())
