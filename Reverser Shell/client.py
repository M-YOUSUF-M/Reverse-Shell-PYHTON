import socket
import subprocess
import os
import platform


server = socket.socket()

host = input("enter server IP: ") 
port = 9999

server.connect((host, port))



def list_files():
    files = os.listdir()
    return "\n".join(files)

def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        return f"Folder '{folder_name}' created successfully."
    except FileExistsError:
        return f"Folder '{folder_name}' already exists."
    except Exception as e:
        return f"Error creating folder '{folder_name}': {e}"

def remove_item(item_name):
    try:
        if os.path.isfile(item_name):
            os.remove(item_name)
            return f"File '{item_name}' removed successfully."
        elif os.path.isdir(item_name):
            os.rmdir(item_name)
            return f"Folder '{item_name}' removed successfully."
        else:
            return f"'{item_name}' is neither a file nor a folder."
    except FileNotFoundError:
        return f"'{item_name}' not found."
    except OSError as e:
        return f"Error removing '{item_name}': {e}"

def create_file(file_name):
    try:
        with open(file_name, "w") as file:
            file.write("")
        return f"File '{file_name}' created successfully."
    except Exception as e:
        return f"Error creating file '{file_name}': {e}"

def change_directory(new_dir):
    try:
        if new_dir == "..":
            os.chdir(os.path.dirname(os.getcwd()))
        else:
            os.chdir(new_dir)
        return f"Current directory changed to: {os.getcwd()}"
    except FileNotFoundError:
        return f"Directory '{new_dir}' not found."
    except Exception as e:
        return f"Error changing directory: {e}"

def system_info():
    return f"System Information:\nCurrent Directory: {os.getcwd()}\nNumber of CPU Cores: {os.cpu_count()}\nPlatform: {platform.system()} {platform.release()}"

def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = str(e.output)
    return output

while True:
    data = server.recv(1024).decode("utf-8")
    if len(data) > 0:
        command = data.split(" ")[0]
        argument = data[len(command)+1:] if len(data.split(" ")) > 1 else ""
        
        if command == "ls":
            output = list_files()
        elif command == "mkdir":
            output = create_folder(argument)
        elif command == "rm":
            output = remove_item(argument)
        elif command == "cat":
            output = create_file(argument)
        elif command == "cd":
            output = change_directory(argument)
        elif command == "sysinfo":
            output = system_info()
        elif command == "pwd":
            output = os.getcwd()
        elif command == "help":
            output = "Available commands:\n" \
                     "  ls - List files in the current directory\n" \
                     "  mkdir <folder_name> - Create a new folder\n" \
                     "  rm <item_name> - Remove a file or folder\n" \
                     "  cat <file_name> - Create a new file\n" \
                     "  cd <directory> - Change the current directory\n" \
                     "  sysinfo - Display system information\n" \
                     "  clear - Clear the screen\n" \
                     "  exit - Exit the command prompt\n"
            server.send(output.encode("utf-8"))
        elif command == "exit":
            server.close() 
            break
        else:
            if command != "clear":
                output = "Unknown command. Type 'help' for available commands.\n"
        if len(output) > 0:
            server.send(output.encode("utf-8"))
