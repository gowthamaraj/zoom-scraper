import os
import sqlite3
import time
import json
import urllib.parse
import datetime

data = {}

def run_script(path):
    # Logged in users
    data_dirs = []
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            data_dirs.append(dir)
    users = [user for user in data_dirs if user.endswith('@xmpp.zoom.us')]
    if users:
        data['users'] = users


    # Chat message sent
    if os.path.exists(os.path.join(path,"zoommeeting.db")):
        connection = sqlite3.connect(os.path.join(path,"zoommeeting.db"))
        cursor = connection.cursor()
        #rows = cursor.execute('SELECT name from sqlite_master where type= "table"').fetchall()
        rows = cursor.execute(f"select time from zoom_conf_chat_gen2_enc").fetchall()
        output = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[0]))
                for row in rows]
        if output:
            data['chat_time'] = output


    # Zoom client config information
    if os.path.exists(os.path.join(path,"zoomus.db")):
        connection = sqlite3.connect(os.path.join(path,"zoomus.db"))
        cursor = connection.cursor()
        data['config'] = {}
        data['Recorded Meetings'] = []
        #rows = cursor.execute('SELECT name from sqlite_master where type= "table"').fetchall()
        zoom_conf_avatar_image_cache = cursor.execute(
            f"select url,path,filesize,timestamp from zoom_conf_avatar_image_cache").fetchall()
        zoom_conf_avatar_image_cache_dict = []
        for item in zoom_conf_avatar_image_cache:
            zoom_conf_avatar_image_cache_dict.append({'url': item[0], 'path': item[1], 'filesize': item[2], 'timestamp': time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(item[3]))})
        if zoom_conf_avatar_image_cache_dict:
            data['config']['zoom_conf_avatar_image_cache'] = zoom_conf_avatar_image_cache_dict

        zoom_conf_video_background_a = cursor.execute(
            f"select name,path from zoom_conf_video_background_a").fetchall()
        zoom_conf_video_background_a_dict = []
        for item in zoom_conf_video_background_a:
            zoom_conf_video_background_a_dict.append(
                {'name': item[0], 'path': item[1]})
        if zoom_conf_video_background_a_dict:
            data['config']['zoom_conf_video_background_a'] = zoom_conf_video_background_a_dict

        zoom_kv_updates = cursor.execute(
            f"select key,value from zoom_kv where section='Update'").fetchall()
        zoom_kv_updates_dict = {}
        for item in zoom_kv_updates:
            zoom_kv_updates_dict[item[0]] = item[1]
        if zoom_kv_updates_dict:
            data['config']['zoom_kv_updates'] = zoom_kv_updates_dict

        zoom_kv = cursor.execute(
            f"select key,value from zoom_kv where section='ZoomChat'").fetchall()
        pick = ['com.zoomus.db.version', 'com.zoom.client.version', 'WorkingDir', 'com.audio.voip.mic.sameassystem', 'com.audio.voip.speaker.sameassystem',
                'updatewnd.donotremindagain', 'com.zoom.client.lastLoginTime', 'schedule.timezone.default', 'schedule.waitingroom.checked', 'com.record.path.root',
                'com.zoom.conf.threshold.to.remind.meeting.time', 'com.conf.callme.telenumber']
        zoom_kv_dict = {}
        for item in zoom_kv:
            if item[0] in pick:
                zoom_kv_dict[item[0]] = item[1]
        if zoom_kv_dict:
            data['config']['zoom_kv'] = zoom_kv_dict

        zoom_meet_history = cursor.execute(
            f"select hostID,meetNo,topic,joinTime,recordPath from zoom_meet_history").fetchall()
        zoom_meet_history_list = []
        for row in zoom_meet_history:
            zoom_meet_history_list.append({'hostID': row[0], 'meetNo': row[1],
                                        'topic': row[2], 'joinTime': time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(row[3])),'recorded path':urllib.parse.unquote(row[4])})
        if zoom_meet_history_list:
            data['Recorded Meetings'] = zoom_meet_history_list

    # Recorded Sessions

    # fcplhujatyyb4n4ihd3asa@xmpp.zoom.us.sync


    def dict_maker(names, data):
        output = {}
        for item in list(zip(names, data)):
            output[item[0]] = item[1]
        return output


    data['user_data'] = {}
    for user in data['users']:
        data['user_data'][user] = {}
        if os.path.exists(os.path.join(path,f"{user}/{user}.asyn.db")):
            connection = sqlite3.connect(os.path.join(path,f"{user}/{user}.asyn.db"))
            cursor = connection.cursor()
            tables = cursor.execute(
                'SELECT name from sqlite_master where type= "table"').fetchall()
            msg_tables = [table[0]
                        for table in tables if table[0].startswith('msg_t_')]
            msgs = []
            for msg in msg_tables:
                rows = cursor.execute(
                    f"select timeStamp,senderName, buddyID, body, messageTimestamp from {msg}").fetchall()
                for row in rows:
                    msgs.append({'timeStamp': time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(row[0])), 'senderName': row[1],
                                'buddyID': row[2], 'body': row[3]})
            if msgs:
                data['user_data'][user]['msgs'] = msgs

            rows = cursor.execute(
                f"select channel, msg_id,emoji,count from emoji_comment_table").fetchall()
            comments = []
            for row in rows:
                comments.append(
                    {'channel': row[0], 'msg_id': row[1], 'emoji': row[2], 'count': row[3]})
            if comments:
                data['user_data'][user]['emoji_comment'] = comments

            rows = cursor.execute(
                f"select insertTime,searchKey from zoom_mm_search").fetchall()
            messages = []
            for row in rows:
                messages.append({'insertTime (Epoch)': row[0], 'searchKey': row[1]})
            if messages:
                data['user_data'][user]['search_messages'] = messages

            rows = cursor.execute(
                f"select sessionID,isGroup,lastUpdateTime from zoom_mm_session").fetchall()
            sessions = []
            for row in rows:
                sessions.append({'Session ID':row[0],'Group':True if row[1] else False,'Update Time': time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(row[2]))})
            if sessions:
                data['user_data'][user]['meeting_sessions'] = sessions

        if os.path.exists(os.path.join(path,f"{user}/{user}.db")):
            connection = sqlite3.connect(os.path.join(path,f"{user}/{user}.db"))
            cursor = connection.cursor()
            rows = cursor.execute(
                f"select jid,email,picPath,avatarUrl,nickName,companyName,jobTitle,location,department,phoneNo from zoom_mm_buddy").fetchall()
            buddies = []
            names = ['jid', 'email', 'picPath', 'avatarUrl', 'nickName',
                    'companyName', 'jobTitle', 'location', 'department', 'phoneNo']
            for row in rows:
                buddies.append(dict_maker(names, row))
            if buddies:
                data['user_data'][user]['buddies_info'] = buddies

            rows = cursor.execute(
                f"select groupID, name, ownerID from zoom_mm_group").fetchall()
            groups = []
            names = ['groupID', 'name', 'ownerID']
            for row in rows:
                groups.append(dict_maker(names, row))
            if groups:
                data['user_data'][user]['group_info'] = groups

            rows = cursor.execute(
                f"select groupID, buddyID from zoom_mm_groupmember").fetchall()
            group_members = []
            names = ['groupID', 'buddyID']
            for row in rows:
                group_members.append(dict_maker(names, row))
            if group_members:
                data['user_data'][user]['group_member_info'] = group_members


    with open("data.json", "w") as write_file:
        json.dump(data, write_file, indent=4)

run_script('C:\\Users\\gowth\\AppData\\Roaming\\Zoom\\data')