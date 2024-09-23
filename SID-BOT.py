import io
import os, json
import codecs
import chardet
import logging
import datetime
import requests
import traceback
import time
from time import sleep
from functools import wraps
import telebot
from telebot import types
import base64,random
from coinbase_commerce.client import Client
import urllib ,json, sys
from requests.exceptions import ConnectionError, ReadTimeout
client = Client(api_key="bb0eb7b6-9e4b-469d-8786-4bd3139b7da3")
token = "7391946524:AAH_HEKkUP38SZOunORtRR41ezWwB9oa1rY"
admin_id = 6971781535
urls2=['20.168.234.93','20.231.23.132']
keys = []
choice = 0
for i in open("keys.txt"):
    if "AKIA" in i:
        i= i.strip()
        keys.append([i.split("|")[0],i.split("|")[1],i.split("|")[2]])

bot = telebot.TeleBot(token, parse_mode=None)
print("Bot Starting")
all_users=[]
for i in open("clients.txt","r").readlines():
    all_users.append(i.split(":")[0].strip())
def bb64(ins):
    return base64.b64encode(ins.encode()).decode("ascii")

def changeaws():
    global choice
    if choice<len(keys)-1:
        choice+=1
    else:
        choice=0
    return str(choice+1)

def discordweb(cont):
    req = urllib.request.Request(url="https://discord.com/api/webhooks/1085627355738943539/AFCWUJO5gvFdmBfDLcfSWvXHooG_DfOs9ma-kB3sFlgM2I1a-lTlIAaECSl8FJmnS-ky",data=json.dumps({"content": f"{cont}"}).encode("latin-1"),headers={"Content-Type": "application/json","user-agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"},method="POST",)
    try:
        response = urllib.request.urlopen(req)
    except Exception as e:
        print(e)

blackll = []
def loadblack():
    global blackll
    blackll = []
    for i in open("blacklist.txt").readlines():
        blackll.append(i.strip().lower())

loadblack()
blackll2=["gov","gouv","bank","banque","police","snap","netf"]

def blacklist(sid):
    if sid.lower() in blackll:
        return True
    if sid.lower().replace("l","i") in blackll:
        return True
    if sid.lower().replace("i","l") in blackll:
        return True
    if sid.lower().replace("-","") in blackll:
        return True
    if sid.lower() in blackll:
        return True
    for i in blackll2:
        if i in sid.lower():
            return True
    return False


with open("dic1.txt", "r") as f:
    sidblack = json.load(f)
with open("dic2.txt", "r") as f:
    msgblack = json.load(f)

def issuspect(msg,sid):
    global sidblack
    global msgblack
    while "\n\n" in msg:
        msg=msg.replace("\n\n","\n")
    msg=msg.replace("\n"," ")
    if sid in sidblack and sidblack[sid]>10:
        return True,sid
    for i in msg.split(" "):
        if i in msgblack and msgblack[i]>10:
            return True,i
    return False,""

def black(msg,sid):
    global sidblack
    global msgblack
    while "\n\n" in msg:
        msg=msg.replace("\n\n","\n")
    msg=msg.replace("\n"," ")
    if sid in sidblack:
        sidblack[sid]+=1
    elif sid not in sidblack:
        sidblack[sid]=1
    for i in msg.split(" "):
        if i in msgblack and len(i)>=4:
            msgblack[i]+=1
        elif len(i)>=4:
            msgblack[i]=1
    with open("dic1.txt", "w") as f:
        json.dump(sidblack, f)
    with open("dic2.txt", "w") as f:
        json.dump(msgblack, f)

def unblack(msg,sid):
    global sidblack
    global msgblack
    while "\n\n" in msg:
        msg=msg.replace("\n\n","\n")
    msg=msg.replace("\n"," ")
    if sid in sidblack:
        sidblack[sid]+=-1
    elif sid not in sidblack:
        sidblack[sid]=-1
    for i in msg.split(" "):
        if i in msgblack and len(i)>=4:
            msgblack[i]+=-1
        elif len(i)>=4:
            msgblack[i]=-1
    with open("dic1.txt", "w") as f:
        json.dump(sidblack, f)
    with open("dic2.txt", "w") as f:
        json.dump(msgblack, f)

def sendsms(msg , senderid, num):
    global choice
    global urls2
    tmp = f"{keys[choice][0]}::::{keys[choice][1]}::::{keys[choice][2]}::::{senderid}::::{num}::::{msg}::::{str(round(time.time()))}"
    tmp = bb64(tmp)
    tmp = tmp.replace("a","ylod5psa6sfms1")
    url = f"http://{random.choice(urls2)}/out?tmp={tmp}"
    try:
        r = requests.get(url,timeout=3)
        if "ok-az2q" in r.text:
            changeaws()
            return True
        else:
            discordweb("Une erreur c'est produite avec la passerelle, le sms est partie directement de la machine")
            changeaws()
            sendsms(msg , senderid, num)
            return True
    except Exception as e:
        print(e)
        discordweb("Une erreur c'est produite avec la passerelle, le sms est partie directement de la machine")
        changeaws()
        return False
def checksender(senderid):
    allow = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    allow2 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if len(senderid)>11:
        return True
    if senderid[0] not in allow2:
        return True
    if senderid[len(senderid)-1] not in allow2:
        return True
    for i in senderid:
        if i not in allow:
            return True
    return False

def checknum(num):
    allow = "0123456789+"
    if len(num)>12:
        return True
    for i in num:
        if i not in allow:
            return True
    return False

def getcredit(userid):
    for i in open("clients.txt","r").readlines():
        if str(userid)==i.split(":")[0].strip():
            return i.split(":")[1].strip()
def changecredit(userid,nbr):
    old = open("clients.txt","r").read()
    for i in open("clients.txt","r").readlines():
        if str(userid)==i.split(":")[0].strip():
            newi = i.split(":")[0] +":"+ str(int(i.split(":")[1])+nbr)
            old = old.replace(i.strip(),newi)
            break
    with open("clients.txt","w") as file:
        file.write(old)
    return
@bot.message_handler(commands=["start"])
def start(message):
    if not str(message.from_user.id) in all_users:
        all_users.append(str(message.from_user.id))
        with open("clients.txt","a") as file:
            file.write(str(message.from_user.id)+":0\n")
    keyboard = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="ðŸ’³ Recharger mon solde", callback_data="recharger")
    but_2 = types.InlineKeyboardButton(text="âš™ï¸ Aide/Guide", callback_data="aide")
    keyboard.row(but_1,but_2)
    bot.send_message(chat_id=message.from_user.id,text='ðŸŒ  Greyz SENDER SMS  ID:'+str(message.from_user.id)+'\n\nðŸ“¡Ici vous pourrrez envoyer des sms avec le SENDER ID que vous souhaitez\nVouch : @vouchgreyzsid\n\nVotre solde actuel est de '+getcredit(message.from_user.id)+' crÃ©dits.\n\nA noter le prix d\'un crÃ©dit/sms est de 0.50â‚¬\nNous ne sommes en aucun cas responsable d\'une utilisation illÃ©gale de cet outil\n\nAttention beaucoup de fake seul support : support@greyz.online',reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data=="recharger":
        charge_info = {"name": "Greyz SID","description": "Rechargement du Sender SMS\nClient ID:"+str(call.from_user.id),"pricing_type": "no_price",}
        charge = client.charge.create(**charge_info)
        entity_id=charge.id
        url = client.charge.retrieve(entity_id)["hosted_url"]
        with open("paiement.txt","a") as file:
            file.write(str(entity_id)+":"+str(round(time.time()))+":"+str(call.from_user.id)+"\n")
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="âœ”ï¸ C'est fais", callback_data="start2")
        but_2 = types.InlineKeyboardButton(text="âŒ Annuler", callback_data="start2")
        keyboard.row(but_1,but_2)
        bot.edit_message_text(chat_id=call.from_user.id,text="<a href='"+url+"'>ðŸ’³ Clique IcI pour recharger</a>\n\nPour recharger :clique sur le lien et envoie le montant que tu souhaites\n\nVos crÃ©dits seront automiquement ajoutÃ©s une fois l'argent rÃ©Ã§u",parse_mode="HTML", message_id=call.message.id,reply_markup=keyboard)
    elif call.data=="start2":
        print(call.message.text)
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="ðŸ’³ Recharger mon solde", callback_data="recharger")
        but_2 = types.InlineKeyboardButton(text="âš™ï¸ Aide/Guide", callback_data="aide")
        keyboard.row(but_1,but_2)
        bot.edit_message_text(chat_id=call.from_user.id,text='ðŸŒ  Greyz SENDER SMS\nID : '+str(call.from_user.id)+'\n\nðŸ“¡Ici vous pourrrez envoyer des sms avec le SENDER ID que vous souhaitez\nVouch : @vouchgreyzsid\n\nVotre solde actuel est de '+getcredit(call.from_user.id)+' crÃ©dits.\n\nA noter le prix d\'un crÃ©dit/sms est de 0.50â‚¬\nNous ne sommes en aucun cas responsable d\'une utilisation illÃ©gale de cet outil\n\nAttention beaucoup de fake seul support : support@greyz.online', message_id=call.message.id,reply_markup=keyboard)
    elif call.data=="aide":
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="ðŸ’¡ IdÃ©e SID", callback_data="sidaide")
        but_2 = types.InlineKeyboardButton(text="âœï¸ Commande", callback_data="cmd")
        but_3 = types.InlineKeyboardButton(text="ðŸ“Ž Retour", callback_data="start2")
        keyboard.row(but_1,but_2,but_3)
        bot.edit_message_text(chat_id=call.from_user.id,text='ðŸŒ  Greyz SENDER SMS\n\nðŸ“Œ Choisissez l\'aide que vous souhaitez:\nAllez dans commande pour savoir comment envoyer des sms\n\nVotre problÃ¨me n\'est pas ici ? contactez moi support@greyz.online\n\nSid= SenderID', message_id=call.message.id,reply_markup=keyboard)
    elif call.data=="sidaide":
        if int(getcredit(call.from_user.id))>0:
            keyboard = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(text="ðŸ“Ž Retour", callback_data="aide")
            keyboard.row(but_1)
            bot.edit_message_text(chat_id=call.from_user.id,text='ðŸŒ  Greyz SENDER SMS\n\nðŸ“Œ Voici quelque idÃ©e de SenderID a utilisÃ©, bien sur vous pouvez en utiliser d\'autre\n\nCrÃ©dit Agricole --> CRAGRICOLE\nCrÃ©dit lyonnais --> CR-LYONNAIS\nCIC --> CIC\nCrÃ©dit Mutuel --> CRMUTUEL\nSociÃ©tÃ© GÃ©nÃ©rale --> SGENERALE\nCaisse d\'Ã©pargne --> CAISSEDEP\nBanque Postale --> BPost\nBanque Populaire --> B-POPULAIRE\nBNP Paribas --> BNPPARIBAS\nBoursorama --> BOURSO-BANK\nHSBC --> HSBCFR\nBPCE --> BPCE', message_id=call.message.id,reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(text="ðŸ“Ž Retour", callback_data="aide")
            keyboard.row(but_1)
            bot.edit_message_text(chat_id=call.from_user.id,text="âŒ Vous devez possÃ©der des crÃ©dits pour accÃ©der Ã  cette section",message_id=call.message.id,reply_markup=keyboard)
    elif call.data=="cmd":
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="ðŸ“Ž Retour", callback_data="aide")
        keyboard.row(but_1)
        bot.edit_message_text(chat_id=call.from_user.id,text='ðŸŒ  Greyz SENDER SMS\n\nðŸ“Œ Voici comment utilisÃ© le sender\n\n/sms +33********* SenderID Message\n/ported +33*********\nLa commande ported sert Ã  voir si un numÃ©ro de tÃ©lÃ©phone est bien connectÃ© sur le rÃ©seau ( Checker HLR )\n\nVoici un exemple de commande:\n/sms +33658749541 Greyz Salut il s\'agit de Greyz\n/ported +33658749541', message_id=call.message.id,reply_markup=keyboard)
    elif call.data=="noaverti":
        ok = 0
        msg=""
        for i in call.message.text.split("\n"):
            if ok==1:
                msg+="\n"+i
            elif i[0:3]=="SID":
                sid = i[5:]
            elif i[0:6]=="NumÃ©ro":
                num = i[8:]
            elif i[0:7]=="Message":
                msg += i[9:]
                ok=1

        if sendsms(msg , sid, num):
            changecredit(str(call.from_user.id),-1)
            keyboard = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(text="âœ”ï¸ Ce message est arrivÃ©", callback_data="recu")
            but_2 = types.InlineKeyboardButton(text="âŒ Rien reÃ§u", callback_data="norecu")
            keyboard.row(but_1,but_2)
            bot.edit_message_text(chat_id=call.from_user.id,text="âœ”ï¸ Le message a bien Ã©tÃ© envoyÃ©\n\nSID: "+sid+"\nNumÃ©ro: "+num+"\n\nMessage: "+msg+"\n\nMerci de rÃ©pondre sÃ©rieusement Ã  la question ci-dessous, si tu ne sais pas, rÃ©ponds pas",reply_markup=keyboard,message_id=call.message.id)
            bot.send_message(-1001779157701,text=f"Message envoyÃ© par {call.from_user.id} \n\nSID: "+sid+"\nNumÃ©ro: "+num+"\n\nMessage: "+msg)
        else:
            bot.edit_message_text(chat_id=call.from_user.id,text="âŒ Une erreur est survenu, Merci de rÃ©essayer\n\nPensez Ã  vÃ©rifier le numÃ©ro, senderID et message.\nSi le problÃ¨me persiste contacte support@greyz.online", message_id=call.message.id)
    elif call.data=="recu":
        ok = 0
        msg=""
        for i in call.message.text.replace("\n\nMerci de rÃ©pondre sÃ©rieusement Ã  la question ci-dessous, si tu ne sais pas, rÃ©ponds pas","").split("\n"):
            if ok==1:
                msg+="\n"+i
            elif i[0:3]=="SID":
                sid = i[5:]
            elif i[0:6]=="NumÃ©ro":
                num = i[8:]
            elif i[0:7]=="Message":
                msg += i[9:]
                ok=1
        unblack(msg,sid)
        bot.edit_message_text(chat_id=call.from_user.id,text="Commentaire prit en compte\n\nMerci beaucoup pour ta rÃ©ponse", message_id=call.message.id)
    elif call.data=="norecu":
        ok = 0
        msg=""
        for i in call.message.text.replace("\n\nMerci de rÃ©pondre sÃ©rieusement Ã  la question ci-dessous, si tu ne sais pas, rÃ©ponds pas","").split("\n"):
            if ok==1:
                msg+="\n"+i
            elif i[0:3]=="SID":
                sid = i[5:]
            elif i[0:6]=="NumÃ©ro":
                num = i[8:]
            elif i[0:7]=="Message":
                msg += i[9:]
                ok=1
        black(msg,sid)
        bot.edit_message_text(chat_id=call.from_user.id,text="Commentaire prit en compte\n\nMerci beaucoup pour ta rÃ©ponse", message_id=call.message.id)





def extract_arg(arg):
    return arg.split(" ")[1:]

def rport(num):
    url = "https://api.numberportabilitylookup.com/npl?user=verifltd&pass=Eragon27%40&msisdn="+num.replace("+","")+"&msc=1&format=json"
    req = requests.get(url)
    if req.status_code==200:
        return req


@bot.message_handler(commands=['ported'])
def ported(message):
    if str(message.from_user.id) not in all_users:
        bot.send_message(message.from_user.id,text="âŒ Vous n'Ãªtes pas inscrit merci de faire la commande /start")
        return
    if int(getcredit(message.from_user.id))<=9:
        bot.send_message(message.from_user.id,text="âŒ Vous n'avez pas assez de crÃ©dit.\nLa commande ported est gratuite cependant vous devez avoir au moins 10 crÃ©dits pour l'utilisÃ©")
        return
    status = extract_arg(message.text)
    if len(status)!=1:
        bot.send_message(message.from_user.id,text="âŒ Des arguments sont manquantes ou incorrect")
        return
    num = status[0]
    if checknum(num) and "33" in num:
        bot.send_message(message.from_user.id,text="âŒ Le numÃ©ro que tu as utilisÃ© est incorrects\n\nExemple de numÃ©ro a utilisÃ©: +33666666666\nNumÃ©ro: "+num)
        return
    try:
        req = rport(num)
        js = json.loads(req.text.replace("[","").replace("]",""))
        if req.text.find('"reachable":"true"')!=-1 or req.text.find('"reachable":"undetermined"')!=-1:
            bot.send_message(message.from_user.id,text=f"âœ”ï¸ Le numero {num} est bien connectÃ© et prÃªt Ã  Ãªtre appelÃ©\n\nOpÃ©rateur :{js['operatorname']}")
            return
        else:
            bot.send_message(message.from_user.id,text=f"âŒ Le numero {num} n'est pas connectÃ© / invalide")
            return
    except Exception as e:
        print(e)
        bot.send_message(message.from_user.id,text="âŒ Nous arrivons pas avoir des informations sur ce numÃ©ro, dÃ©solÃ©\nNumÃ©ro: "+num)







@bot.message_handler(commands=['sms'])
def sms(message):
    if str(message.from_user.id) not in all_users:
        bot.send_message(message.from_user.id,text="âŒ Vous n'Ãªtes pas inscrit merci de faire la commande /start")
        return
    if int(getcredit(message.from_user.id))<=0:
        bot.send_message(message.from_user.id,text="âŒ Vous n'avez pas assez de crÃ©dit, merci de recharger votre compte.\n\nSi vous pensez qu'il s'agit d'une erreur contact support@greyz.online")
        return
    status = extract_arg(message.text)
    if len(status)<3:
        bot.send_message(message.from_user.id,text="âŒ Des arguments sont manquantes ou incorrect")
        return
    count=0
    msg=""
    for i in status:
        if count==0:
            num=i
        elif count==1:
            sid=i
        else:
            msg+=i+" "
        count+=1
    if blacklist(sid):
        bot.send_message(message.from_user.id,text="âŒ Le SenderID que tu as utilisÃ© est blacklist")
        return
    if checknum(num):
        bot.send_message(message.from_user.id,text="âŒ Le numÃ©ro que tu as utilisÃ© est incorrects\n\nExemple de numÃ©ro a utilisÃ©: +33666666666\nNumÃ©ro: "+num)
        return
    if checksender(sid):
        bot.send_message(message.from_user.id,text="âŒ Le SenderID est incorrect pour rappel seul les caractÃ¨res alphanumÃ©rique sont autorisÃ©\nLes espaces ne sont pas autorisÃ© utilisÃ© des -\n\nVoici un exemple de senderID: CR-AGRICOLE\nSenderID: "+sid)
        return
    bool,susp=issuspect(msg,sid)
    if bool:
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="â˜¢ï¸ Envoyer quand mÃªme", callback_data="noaverti")
        keyboard.row(but_1)
        bot.send_message(message.from_user.id,text="â˜¢ï¸ Attention: Le message qui tu vas send est suceptible de ne pas inbox\n\nCet avertissement est basÃ© sur l'expÃ©rience d'autre utlisateur et peut Ãªtre biasÃ©\n\nLe terme suspect est : "+susp+"\n\nSID: "+sid+"\nNumÃ©ro: "+num+"\n\nMessage: "+msg,reply_markup=keyboard)
        return
    if sendsms(msg , sid, num):
        changecredit(str(message.from_user.id),-1)
        bot.send_message(-1001779157701,text=f"Message envoyÃ© par {message.from_user.id} \n\nSID: "+sid+"\nNumÃ©ro: "+num+"\n\nMessage: "+msg)
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(text="âœ”ï¸ Ce message est arrivÃ©", callback_data="recu")
        but_2 = types.InlineKeyboardButton(text="âŒ Rien reÃ§u", callback_data="norecu")
        keyboard.row(but_1,but_2)
        bot.send_message(message.from_user.id,text="âœ”ï¸ Le message a bien Ã©tÃ© envoyÃ©\n\nSID: "+sid+"\nNumÃ©ro: "+num+"\n\nMessage: "+msg+"\n\nMerci de rÃ©pondre sÃ©rieusement Ã  la question ci-dessous, si tu ne sais pas, rÃ©ponds pas",reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id,text="âŒ Une erreur est survenu, Merci de rÃ©essayer\n\nPensez Ã  vÃ©rifier le numÃ©ro, senderID et message.\nSi le problÃ¨me persiste contacte support@greyz.online")
try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)