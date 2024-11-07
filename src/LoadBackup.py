
from subprocess import run
from datetime import datetime as dt
import os
import configparser
import zipfile
import stat


def get_config (path='./path.ini'):
    """
        Returning: [Map_Folder_Path, Execute_App, App_Path]
    """
    config = configparser.ConfigParser()
    if config.read(path):
        map_dir_path = config['PATH']['Map_Folder_Path']
        execute_exe = config['PATH']['Execute_App']
        app_path = config['PATH']['App_Path']
        return map_dir_path, execute_exe, app_path

    else:
        print("Could not read path.ini!") 
        print("Make sure 'path.ini' is in the same folder as the exe.")
        print("Path used:", path)
        input()
        exit()


def load_backup(map_dir_path):
    # parse paths for readability
    map_list = map_dir_path.split('\\')
    instance_path = "\\".join(map_list[:-2])
    backups_dir = instance_path + "\\backups"
    saves_path = "\\".join(map_list[:-1])
    
    # Get zip Files in dir
    dir_list = os.listdir(backups_dir)
    zip_files = [file for file in dir_list if file.endswith('.zip')]

    # Unzipping the most recent backup in saves
    most_recent_file = max(zip_files)
    backup_zip = backups_dir+"\\"+most_recent_file
    backup_name = most_recent_file.split(".")[0]
    print("The Most Recent Backup:", backup_name)
    print("Unzipping to saves")

    with zipfile.ZipFile(backup_zip, 'r') as zip_ref:
        zip_ref.extractall(saves_path)

    try:
        print("Moving SyncTrayzor Folder", end='')
        os.rename(map_dir_path+"\\.stfolder", saves_path+"\\"+backup_name+"\\.stfolder")
    except:
        print("... Wasn't Found. Continuing", end='')
    
    # no time to make it work
    # zip = zipfile.ZipFile(map_dir_path+ dt.today().strftime("-%Y-%m-%d-%H-%M-%S")+".zip", "w", zipfile.ZIP_DEFLATED)
    # zip.write(map_dir_path)
    # zip.close()
    # os.remove(map_dir_path)
    
    print("\nRenaming Old Map")
    os.rename(map_dir_path, map_dir_path+ dt.today().strftime("-%Y-%m-%d-%H-%M-%S"))

    print("Renaming Backup")
    os.rename(saves_path+"\\"+backup_name, map_dir_path)
    print("Backup Moved Successfully")


def main():
    map_dir_path, _, _ = get_config()
    load_backup(map_dir_path)
    try:
        pass

    except Exception as e:
        print("Failed Move\n")
        print(e)

    finally:
        input("Press ENTER to exit")
        exit()


main()