import nbtlib
from subprocess import run
import configparser
import json

def delete_player_structure(folder_path):
    try:
        file_path = folder_path + "\\level.dat"
        print("Loading the Data.")
        nbt_file = nbtlib.load(file_path)
        level_data = nbt_file["Data"]
        
        print("Verifying the Data.")
        # Delete player structure
        if "Player" in level_data:
            del level_data["Player"]
            print("Server Player deleted.")

            # Save modified level.dat file
            nbt_file.save(file_path)
            print("Saved successfully.")

        else:
            print("Server Player has already deleted.")

        
    except Exception as e:
        print("Failed to delete Server Player.")
        print(e)


def move_quests_to_host(host_uuid, folder_path):
    
    # Opening JSON file
    path_json = folder_path + "\\betterquesting\\QuestProgress.json"
    with open(path_json) as file_json:
        # Convert to dictionary
        dic_json = json.load(file_json)  
        old_uuid = dic_json['questProgress:9']['0:10']['completed:9']['0:10']['uuid:8']

        # Clear first quest\
        complete_users = {"0:8": host_uuid}
        user_progress = {"0:10": {"data:9": {"0:3": 64,"1:3": 64},"uuid:8": host_uuid}}

        dic_json['questProgress:9']['0:10']['tasks:9']['0:10']['completeUsers:9'] = complete_users
        dic_json['questProgress:9']['0:10']['tasks:9']['0:10']['userProgress:9'] = user_progress

        print(f"Old UUID: {old_uuid}")
        print(f"New UUID: {host_uuid}")
    #Convert to string and replace uuid
    string_json = json.dumps(dic_json).replace(old_uuid, host_uuid)
    dic_json = json.loads(string_json)

    with open(path_json,"w") as file_json:
        json.dump(dic_json, file_json)
    
    return
        

def get_config (path):
    config = configparser.ConfigParser()
    if config.read(path):
        return config
    
    else:
        raise FileNotFoundError("Could not read Path", path)

# Usage example
config = get_config('./path.ini')
app_path = config['PATH']['Minecraft_exe']
run_exe = config['PATH']['Execute_Minecraft']
folder_path = config['PATH']['Map_Folder_path']
host_UUID = config['PATH']['UUID']

delete_player_structure(folder_path)

if (run_exe == '1'):
   run([app_path])

input()#BREAK BEFORE FINISH