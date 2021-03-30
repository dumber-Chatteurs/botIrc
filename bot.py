# -*- coding: utf-8 -*-

################################################
# BASE DE BOT IRC PAR DUMBER POUR CHATTEURS.FR #
# Code sans licence, seule demande, de laisser #
# Ce commentaire dans tout bot contenant cette #
# Base, et d'en concerver la version.          #
################################################

import socket
import sys
import re

SERVER = "irc.chatteurs.fr"       
PORT = 6667

MAINCHAN = "#python" #salle de debug et de retour pour les test
BACKCHAN = "#python.debug" #salle de debug et de retour pour les test
BOTNICK = "GIZPI"
BOTHOST = "127.0.0.1"
BOTIDENT = "bot-GIZPI"
REALNAME = "DMBER FAIT JOUJOU PYTHON"
OMBNICK =  "Gizmo"
OMBPASS = ""
SETDEBUG = 0 #passer a 1 pour avoir les retour ur BACKCHAN
SETVERSIONBASE = "Python BaseBot By dumber pour le reseau CHATTEURS.FR" #MERCI DE NE PAS CHANGER CETTE LIGNE
SETVERSIONPLUS = "ICI METTEZ QUE VOTRE VERSION DU BOT"


irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print("connecting to:"+SERVER)
irc.connect((SERVER, PORT))                                                         #connects to the server
irc.send("USER "+ BOTIDENT +" "+ BOTHOST +" "+ SERVER +" :"+ REALNAME +"\n") #user authentication
irc.send("NICK "+ BOTNICK +"\n")        



def switch(case):
    def cases(dict_):
        try:
            return dict_[case]()
        except KeyError:
            if 'else' in dict_:
                return dict_['else']()
            raise Exception('CAS INCONNU.')
    return cases


def case_001():
    irc.send("JOIN "+ MAINCHAN +"\n")        #join the mainchan
    
    if SETDEBUG == 1:
        irc.send("JOIN "+ BACKCHAN +"\n")
    irc.send("PRIVMSG "+ OMBNICK +" :opmybot "+ OMBPASS +"\r\n")


def case_404(): #s'il n'est pas sur la salle
    CHAN = args.split() [3]
    irc.send("JOIN "+ CHAN +"\n")
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : Je ne suis pas sur "+ CHAN +" Je rejoins\r\n")

def case_MODE(): #gestion des modes 
    NICK = args.split('!')[0][1:]
    CHAN = args.split() [2]
    MODE = args.split()[3][1:]
    TYPEMODE = "".join(map(str, re.findall(r":",args.split()[3])))
    irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" set mode "+ MODE +" sur "+ CHAN +"\r\n")
    if TYPEMODE == ":":
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" set mode "+ MODE +" sur "+ CHAN +"\r\n")
    else:
        VICTIME = args.split()[4][1:]
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" set mode +"+ MODE +" "+ CHAN +" sur "+ VICTIME +"\r\n")
	
def case_NOTICE(): #gestion des notices encours (OK)
    NICK = args.split('!')[0][1:]
    MSG = " ".join(map(str, args.split()[3:]))[1:]
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +"Me dit en notice : "+ MSG +"\r\n")
	
def case_PRIVMSG(): #gestion des MSG 
    CIBLE = "".join(map(str, re.findall(r"#", args.split()[2])))
    CHAN = args.split()[2]
    NICK = args.split('!')[0][1:]
    MSG = " ".join(map(str, args.split()[3:]))[1:]
    
    if CIBLE == "#": ##SI MSG EN SALLE
        CMD = MSG.split()[0]
       
        if CMD == "!test":
			irc.send("PRIVMSG "+ CHAN +" :4,8BIIIIIP  BIPPPPPP BIPPPPP HOLEEEEEE "+ NICK +"\n")

        if CMD == "!op":
            if NICK == "dumber":
                irc.send("MODE "+ CHAN +" +o "+ NICK +"\n")

        if CMD == "!voice":
            if NICK == "dumber":
                if "MSG.split()[1]" in locals():
                    VICTIME = NICK
                else:
                    VICTIME = MSG.split()[1]
                irc.send("MODE "+ CHAN +" +v "+ VICTIME +"\n")
        
        if CMD == "!devoice":
            if NICK == "dumber":
                if "MSG.split()[1]" in locals():
                    VICTIME = NICK
                else:
                    VICTIME = MSG.split()[1]
                irc.send("MODE "+ CHAN +" -v "+ VICTIME +"\n")        
       
        if SETDEBUG == 1:
            irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" dit sur " + CHAN +" : "+ MSG +" \n")
   
    else:  ##SI MSG EN PRIVE
        CMD = MSG.split()[0]
        #MERCI DE LAISSER CE CODE
        if CMD == "VERSION": #NE PAS TOUCHER
            irc.send("NOTICE "+ NICK +" :VERSION "+ SETVERSIONBASE +" . "+ SETVERSIONPLUS +"  \n")#NE PAS TOUCHER
        if SETDEBUG == 1:
            irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" me dit en prive " + CMD +" : "+ MSG +" \n")
	
def case_NICK(): #gestion des changements de pseudo
    NICK = args.split('!')[0][1:]
    NEWNICK = args.split() [2][1:]
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" change de pseudo en " + NEWNICK +" \n")
	
def case_JOIN(): #gestion des joins
    NICK = args.split('!')[0][1:]
    CHAN = args.split() [2][1:]
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" JOIN "+ CHAN +" \n")
	
def case_PART(): #gestion des part
    NICK = args.split('!')[0][1:]
    CHAN = args.split() [2][1:]
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" PART "+ CHAN +" \n")
	
def case_TOPIC(): #gestion des topic
    NICK = args.split('!')[0][1:]
    CHAN = args.split()[2]
    TOPIC = " ".join(map(str, args.split()[3:]))[1:]
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" TOPIC "+ CHAN +" : "+ TOPIC +" \n")

def case_KICK(): #gestion des kick
    NICK = args.split('!')[0][1:]
    CHAN = args.split()[2]
    VICTIME = args.split()[3]
    RAISON = " ".join(map(str, args.split()[4:]))[1:]
    if VICTIME == BOTNICK:
        irc.send("PRIVMSG "+ BACKCHAN +" : Un sale aux trou ("+ NICK +") m'a éxclu de "+ CHAN +" pour "+ RAISON +". J'y retourne de ce pas \n")
        irc.send("JOIN "+ CHAN +" \n")
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ VICTIME +" Exclus de "+ CHAN +" par "+ NICK +" pour "+ RAISON +" \n")
	
def case_QUIT(): #gestion des quitsafaire
    NICK = args.split('!')[0][1:]
    RAISON = " ".join(map(str, args.split()[2:]))[1:]
    if SETDEBUG == 1:
        irc.send("PRIVMSG "+ BACKCHAN +" : "+ NICK +" Quit pour : "+ RAISON +" \n")
    
def default():
    print(args)

while 1:
    
    args = irc.recv(2040) 
    print(args)   #ECHO EN CONSOLE
    
    #Gestion du ping
    if args.find('PING') != -1:                         
        irc.send('PONG ' + args.split() [1] + '\r\n') 
   
    RAW = args.split()[1]
  
    switch(RAW) ({
        '001': case_001,
        '404': case_404,
        'MODE': case_MODE,
        'NOTICE': case_NOTICE,
        'PRIVMSG': case_PRIVMSG,
        'NICK': case_NICK,      
        'JOIN': case_JOIN,
        'PART': case_PART,
        'TOPIC': case_TOPIC,
        'KICK': case_KICK,
        'QUIT': case_QUIT,
        'else': default
    })