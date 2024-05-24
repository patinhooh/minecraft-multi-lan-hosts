
from subprocess import run
import configparser
from nbtlib import load


def delete_player(map_folder_path):
    """
        Opens the level.dat file and deletes the player info
    """
    try:
        file_path = map_folder_path + "\\level.dat"
        print("Loading the Data.")
        nbt_file = load(file_path)
        level_data = nbt_file["Data"]

        print("Verifying the Data.")
        # Delete player structure
        if "Player" in level_data:
            del level_data["Player"]
            print("Server Player deleted.")
            print("Saving... ")
            # Save modified level.dat file
            nbt_file.save(file_path)
            print("Saved successfully.")

        else:
            print("Server Player is already deleted.")

    except Exception as e:
        print("Failed during Server Player!")
        print(e)
        input()
        exit()
        

def get_config (path='./path.ini'):
    """
        Returning: [Map_Folder_Path, Execute_App, App_Path]
    """
    config = configparser.ConfigParser()
    if config.read(path):
        map_folder_path = config['PATH']['Map_Folder_Path']
        execute_exe = config['PATH']['Execute_App']
        app_path = config['PATH']['App_Path']
        return map_folder_path, execute_exe, app_path

    else:
        print("Could not read path.ini!") 
        print("Make sure 'path.ini' is in the same folder as the exe.")
        print("Path used:", path)
        input()
        exit()


def main():
    map_folder_path, execute_exe, app_path = get_config()
    delete_player(map_folder_path)
    try:
        if (execute_exe == '1'):
            run([app_path])
        else:
            input()

    except Exception as e:
        print("Failed to run App\n")
        print(e)
        input()
        exit()


main()