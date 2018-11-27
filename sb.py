# -*- coding: utf-8 -*-
from linepy import *
import json, time, random, os, num

with open("auth.txt","r") as token:
    auth=token.read().replace("\n","")
    if not auth:
        client = LineClient()
        with open("auth.txt","w") as token:
            token.write(client.authToken)
    else:
        client = LineClient(authToken=auth)
channel = LineChannel(client)
client.log("Auth Token : "+str(client.authToken))
client.log("Channel Access Token : "+str(channel.channelAccessToken))
poll = LinePoll(client)

ids=["u2b69d9f6ba4479b2a83f715648ab9748"]
cctv={"cyduk":{},"point":{},"sidermem":{}}
stand={}
run_time,run_max = 0,1
shut_flag=False

while True:
    if shut_flag == True:
        break
    try:
        ops=poll.singleTrace(count=50)
        for op in ops:
            if op.type == 26:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                try:
                    if msg.contentType == 0:
                        if msg.toType == 2:
                            if text.lower() == "shut down" and sender in ids:
                                client.sendText(receiver,"關...關機")
                                shut_flag=True
                            elif text.lower() == 'speed' and sender in ids:
                                start = time.time()
                                client.sendText(receiver, "測試測試")
                                client.sendText(receiver, "%s sec" % (time.time() - start))
                            elif text.lower() == '@-@':
                                client.sendText(receiver, "@-@")
                            elif text.lower() == '@-@!':
                                if msg.to in cctv['point']:
                                    #cctv['cyduk'][msg.to]=False
                                    name_list=cctv['sidermem'][msg.to].split("\n")
                                    del name_list[len(name_list)-1]
                                    name_text,name_num="",len(name_list)
                                    for i in name_list:
                                        name_text +=i
                                        if i!=name_list[len(name_list)-1]:
                                            name_text +="\n"
                                    client.sendText(receiver,name_text)
                                    client.sendText(receiver,"抓到"+str(name_num)+"個已讀仔@@")
                                else:
                                    client.sendText(receiver, "NoReadPoint")
                        else:
                               pass
                    else:
                        pass
                except Exception as e:
                    client.log("[SEND_MESSAGE] ERROR : " + str(e))
            else:
                pass
            if op.type == 25:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                try:
                    if msg.contentType == 0:
                        if msg.toType == 2:
                            client.sendChatChecked(receiver, msg_id)
                            contact = client.getContact(sender)
                            if text.lower() == '@-@':
                                try:
                                    del cctv['point'][msg.to]
                                    del cctv['sidermem'][msg.to]
                                    del cctv['cyduk'][msg.to]
                                except:
                                    pass
                                cctv['point'][msg.to] = msg.id
                                cctv['sidermem'][msg.to] = ""
                                cctv['cyduk'][msg.to]=True
                except Exception as e:
                    client.log("[SEND_MESSAGE] ERROR : " + str(e))
            elif op.type == OpType.NOTIFIED_READ_MESSAGE:
                try:
                    if cctv['cyduk'][op.param1]==True:
                        if op.param1 in cctv['point']:
                            Name = client.getContact(op.param2).displayName
                            if Name in cctv['sidermem'][op.param1]:
                                pass
                            else:
                                cctv['sidermem'][op.param1] +="-> "+Name +"\n"
                        else:
                            pass
                    else:
                        pass
                except:
                    pass
            else:
                pass
            # Don't remove this line, if you wan't get error soon!
            poll.setRevision(op.revision)
    except Exception as e:
        client.log("[SINGLE_TRACE] ERROR : " + str(e))