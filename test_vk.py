from config_vk import VK_CONFIG
import requests
from db import SQLiteDriver
import time
from tqdm.auto import tqdm

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
start_user_id = 42099955# PUT USER ID HERE
#fields_friends = 'sex'
fields_groups = 'description,members_count'
fields_user = 'bdate,about,activities,city,counters,country,education,home_town,personal,relation,sex'

get_friends_list_api = lambda x: f"{domain}/friends.get?access_token={access_token}&user_id={x}&v={v}" #&fields={fields_friends}
#get_group_list_api = lambda x: f"{domain}/groups.get?access_token={access_token}&user_id={x}&fields={fields_groups}&v={v}&extended=1" #name, description, members_count
get_user_info_api = lambda x: f"{domain}/users.get?access_token={access_token}&user_id={x}&fields={fields_user}&v={v}&extended=1" #name, description, members_count

DEPTH_LIMIT = 1 

FIELDS = ["id", "first_name","last_name","sex", "is_closed", "bdate", "about","activities", "university", "university_name", "faculty", "faculty_name", "graduation", "home_town"]


sqldriver = SQLiteDriver("test.db")

class requestC:
    def __init__(self,):
        self.t1 = 0.0
        self.t2 = 0.0

    def get(self, addr):
        while time.time() - self.t1 < 3:
            continue
        response = requests.get(addr).json()
        self.t1 = time.time()
        return response
    
req = requestC()


def get_user_info(user_id):
    user_info = req.get(get_user_info_api(user_id))["response"][0]
    print("{} {}".format(user_info["first_name"], user_info["last_name"]))
    d = {k:"\"\"" for k in FIELDS}
    for k in FIELDS:
        try:
            d[k] = user_info[k]
        except:
            continue
    quary = "INSERT INTO users(id, first_name, last_name, sex, is_closed, bdate, about, activities, university, university_name, faculty, faculty_name, graduation, home_town ) VALUES({},\"{}\",\"{}\",{},{},\"{}\",\"{}\",\"{}\",{},\"{}\",{},\"{}\",{},\"{}\")".format(d["id"],d["first_name"],d["last_name"],d["sex"],d["is_closed"],d["bdate"],d["about"],d["activities"],d["university"],d["university_name"],d["faculty"],d["faculty_name"], d["graduation"] ,d["home_town"])
    sqldriver.execute_query(quary)
    try:
        return user_info["is_closed"]
    except KeyError:
        return True


def dfs(user_id, counter):
    print(f"DEBUG: user_id: {user_id}")
    counter += 1
    print(counter)
    skip = get_user_info(user_id)
    if skip:
        counter -= 1
        return
    elif counter == DEPTH_LIMIT:
        counter -= 1
        return
    try:
        friends_list = req.get(get_friends_list_api(user_id))["response"]["items"]
    except:
        print(req.get(get_friends_list_api(user_id)))
        exit()
    #insert values into table
    
    
    inserted_values = [(user_id, f) for f in friends_list]
    for f in tqdm(inserted_values):
        q = 'INSERT INTO friends(user_id, friend_id) VALUES({}, {})'.format(f[0],f[1])
        sqldriver.execute_query(q)

    for friend in friends_list:
        dfs(friend, counter)
    counter -= 1
    return

dfs(42099955, -1)
