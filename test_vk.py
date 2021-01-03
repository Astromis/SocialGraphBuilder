from config_vk import VK_CONFIG
import requests
from db import SQLiteDriver

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
user_id = 42099955# PUT USER ID HERE
#fields_friends = 'sex'
fields_groups = 'description,members_count'
fields_user = 'bdate,about,activities,city,counters,country,education,home_town,personal,relation,sex'

get_friends_list_api = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&v={v}" #&fields={fields_friends}
get_group_list_api = f"{domain}/groups.get?access_token={access_token}&user_id={user_id}&fields={fields_groups}&v={v}&extended=1" #name, description, members_count
get_user_info_api = f"{domain}/users.get?access_token={access_token}&user_id={user_id}&fields={fields_user}&v={v}&extended=1" #name, description, members_count

DEPTH_LIMIT = 5 

sqldriver = SQLiteDriver("test.db")

def sql_insert_friends(con, entities):

    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO friends(user_id, friend_id) VALUES(?, ?)', entities)
    con.commit()

def get_user_info(user_id):
    user_info = requests.get(get_user_info_api).json()["response"][0]
    quary = "INSERT INTO users(id, first_name, last_name, sex, is_closed, bdate, about, activities, university, university_name, faculty, faculty_name, graduation, home_town, friends ) VALUES({},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(user_info["id"],user_info["first_name"],user_info["last_name"],user_info["sex"],user_info["is_closed"],user_info["bdate"],user_info["about"],user_info["activities"],user_info["university"],user_info["university_name"],user_info["faculty"],user_info["faculty_name"], user_info["graduation"] ,user_info["home_town"])
    sqldriver.execute_query(quary)
    group_list = requests.get(get_group_list_api).json()["response"]["items"]
    for group in group_list:
        quary = "INSERT INTO groups(id, name, description, members_count) VALUES({},\"{}\",\"{}\",{})".format(group["id"],group["name"],group["description"],group["members_count"])
        sqldriver.execute_query(quary)
        quary = "INSERT INTO user_groups(user_id, group_id) VALUES({},{})".format(user_id, group["id"])
        sqldriver.execute_query(quary)

def dfs(user_id, counter):
    counter += 1
    get_user_info(user_id)
    friends_list = requests.get(get_friends_list_api).json()["response"]["items"]
    #insert values into table
    inserted_values = [(user_id, f) for f in friends_list]
    for f in inserted_values:
        q = 'INSERT INTO friends(user_id, friend_id) VALUES({}, {})'.format(f[0],f[1])
        sqldriver.execute_query(q)
    if counter == DEPTH_LIMIT:
        return 
    for friend in friends_list:
        dfs(friend, counter)
        counter -= 1
    return

dfs(42099955, 2)
#print(requests.get(get_group_list_api).json()["response"]["items"][0])