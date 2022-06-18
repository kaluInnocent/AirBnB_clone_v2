#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from shlex import split
from datetime import datetime
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
               }

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class with given parameters
        Usage: create <Class name> <param 1> <param 2> <param 3>...
        args: list of commands passed
        """
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            if arg_list:
                class_name = arg_list[0]
            else:
                raise SyntaxError()

            kwargs = {}
            for arg in arg_list[1:]:
                key, value = tuple(arg.split("="))
                if self.is_int(value):
                    kwargs[key] = int(value)
                elif self.is_float(value):
                    kwargs[key] = float(value)
                else:
                    kwargs[key] = value.strip('"\'').replace("_", " ")
            if kwargs == {}:
                obj = eval(arg_list[0])()
            else:
                obj = eval(arg_list[0])(**kwargs)
                storage.new(obj)
                obj.save()
                print("{}".format(obj.id))

        except SyntaxError:
            print("** class name missing **")
        except KeyError:
            print("** class doesn't exist **")

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Prints the string representation of an instance"""
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            if arg_list[0] not in self.classes:
                raise NameError()
            if len(arg_list) < 2:
                raise IndexError()
            obj = storage.all()
            key = "{}.{}".format(arg_list[0], arg_list[1])
            if key in obj:
                print(obj[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object that has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            if arg_list[0] not in self.classes:
                raise NameError()
            if len(arg_list) < 2:
                raise IndexError()
            obj = storage.all()
            key = "{}.{}".format(arg_list[0], arg_list[1])
            if key in obj:
                storage.delete(obj[key])
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects
        Usage: all or all <class> or <class>.all()
        """
        if not args:
            obj = storage.all()
            print([obj[key].__str__() for key in obj])
            return
        try:
            arg_list = args.split(" ")
            if arg_list[0] not in self.classes:
                raise NameError()
            obj = storage.all(args)
            print(
                    [
                        obj[key].__str__()
                        for key in obj
                        if key.split(".")[0] == arg_list[0]])
        except NameError:
            print("** class doesn't exist **")

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Counts the number of instances of a class"""
        count = 0
        try:
            arg_list = split(args, " ")
            if arg_list[0] not in self.classes:
                raise NameError()
            obj = storage.all()
            for key in obj:
                if key.split(".")[0] == arg_list[0]:
                    count += 1
            print(count)
        except NameError:
            print("** class doesn't exist **")

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        """
        try:
            if not args:
                raise SyntaxError()
            arg_list = split(args, " ")
            if arg_list[0] not in self.classes:
                raise NameError()
            if len(arg_list) < 2:
                raise IndexError()
            obj = storage.all()
            key = "{}.{}".format(arg_list[0], arg_list[1])
            if key not in obj:
                raise KeyError()
            if len(arg_list) < 3:
                raise AttributeError()
            if len(arg_list) < 4:
                raise ValueError()
            val = obj[key]
            try:
                val.__dict__[arg_list[2]] = eval(arg_list[3])
            except Exception:
                val.__dict__[arg_list[2]] = arg_list[3]
                val.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    def strip_clean(self, args):
        """Method strips the arguments passed to it
        and returns strings of commands
        Arguments:
            args (list): list of arguments
        Return: String of arguments
        """
        arg_list = []
        arg_list.append(args[0])
        try:
            arg_dict = eval(
                    args[1][args[1].find("{"):args[1].find("}") + 1])
        except Exception:
            arg_dict = None
        if type(arg_dict) is dict:
            str_arg = args[1][args[1].find("(") + 1:args[1].find(")")]
            arg_list.append(str_arg.split(", ")[0].strip('"'))
            arg_list.append(arg_dict)
            return arg_list
        str_arg = args[1][args[1].find("(") + 1:args[1].find(")")]
        arg_list.append(" ".join(str_arg.split(", ")))
        for cmd in arg_list:
            return " ".join(cmd)

    def default(self, args):
        """ retrieve all instances of a class and
        retrieve the number of instances
        """
        arg_list = args.split(".")
        if len(arg_list) >= 2:
            if arg_list[1] == "all()":
                self.do_all(arg_list[0])
            elif arg_list[1] == "count()":
                self.count(arg_list[0])
            elif arg_list[1][:4] == "show":
                self.do_show(self.strip_clean(arg_list))
            elif arg_list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(arg_list))
            elif arg_list[1][:6] == "update":
                arg = self.strip_clean(arg_list)
                if type(arg) is list:
                    obj = storage.all()
                    key = "{} {}".format(arg[0], arg[1])
                    for k, v in arg[2].items():
                        self.update('{} "{}" "{}"'.format(key, k, v))
                else:
                    self.update(arg)
            else:
                cmd.Cmd.default(self, args)

    @staticmethod
    def is_int(ele):
        """checks if a string is convertible to integer
        Argument:
            ele (str): element to be checked
        """
        try:
            int(ele)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(ele):
        """checks if a string is convertibke to float
        Argument:
            ele (str): item to be checked
        """
        try:
            float(ele)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
