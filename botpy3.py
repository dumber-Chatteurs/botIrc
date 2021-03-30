

################################################
# BASE DE BOT IRC PAR DUMBER POUR CHATTEURS.FR #
# Code sans licence, seule demande, de laisser #
# Ce commentaire dans tout bot contenant cette #
# Base, et d'en concerver la version.          #
################################################

import socket
import sys
import re
import string

SERVER = "irc.chatteurs.fr"       
PORT = 6667

OWNERNICK = "dumber"

MAINCHAN = "#python" #salle de debug et de retour pour les test
BACKCHAN = "#python.debug" #salle de debug et de retour pour les test
BOTNICK = "GIZPI"
BOTHOST = "127.0.0.1"
BOTIDENT = "bot-GIZPI"
REALNAME = "DMBER FAIT JOUJOU PYTHON"
OMBNICK =  "Gizmo"
OMBPASS = ""
SETDEBUG = 1 #passer a 1 pour avoir les retour ur BACKCHAN
SETVERSIONBASE = "Python BaseBot By dumber pour le reseau CHATTEURS.FR" #MERCI DE NE PAS CHANGER CETTE LIGNE
SETVERSIONPLUS = "ICI METTEZ QUE VOTRE VERSION DU BOT"


irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print("connecting to:"+SERVER)
irc.connect((SERVER, PORT))                                                         #connects to the server
irc.send(bytes("USER "+ BOTIDENT +" "+ BOTHOST +" "+ SERVER +" :"+ REALNAME +"\n", "UTF-8")) #user authentication
irc.send(bytes("NICK "+ BOTNICK +"\n", "UTF-8"))       



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
    irc.send(bytes("JOIN "+ MAINCHAN +"\n", "UTF-8"))#join the mainchan
    
    if SETDEBUG == 1:
        irc.send(bytes("JOIN "+ BACKCHAN +"\n", "UTF-8"))
    irc.send(bytes("PRIVMSG "+ OMBNICK +" :opmybot "+ OMBPASS +"\r\n", "UTF-8"))


def case_404(): #s'il n'est pas sur la salle
    CHAN = args.split() [3]
    irc.send(bytes("JOIN "+ CHAN +"\n", "UTF-8"))
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : Je ne suis pas sur "+ CHAN +" Je rejoins\r\n", "UTF-8"))

def case_MODE(): #gestion des modes 
    NICK = args.split('!')[0][3:]
    CHAN = args.split() [2]
    MODE = args.split()[3][1:]
    TYPEMODE = "".join(map(str, re.findall(r":",args.split()[3])))
    irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" set mode "+ MODE +" sur "+ CHAN +"\r\n", "UTF-8"))
    if TYPEMODE == ":":
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" set mode "+ MODE +" sur "+ CHAN +"\r\n", "UTF-8"))
    else:
        VICTIME = args.split()[4][1:]
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" set mode +"+ MODE +" "+ CHAN +" sur "+ VICTIME +"\r\n", "UTF-8"))
	
def case_NOTICE(): #gestion des notices encours (OK)
    NICK = args.split('!')[0][3:]
    MSG = " ".join(map(str, args.split()[3:]))[1:]
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +"Me dit en notice : "+ MSG +"\r\n", "UTF-8"))
	
def case_PRIVMSG(): #gestion des MSG 
    CIBLE = "".join(map(str, re.findall(r"#", args.split()[2])))
    CHAN = args.split()[2]
    NICK = args.split('!')[0][3:]
    MSG = " ".join(map(str, args.split()[3:]))[1:]
    
    if CIBLE == "#": ##SI MSG EN SALLE
        CMD = MSG.split()[0]
       
        if CMD == "!test":
            irc.send(bytes("PRIVMSG "+ CHAN +" :4,8BIIIIIP  BIPPPPPP BIPPPPP HOLEEEEEE "+ NICK +"\n", "UTF-8"))

        if CMD == "!op":
            if NICK == OWNERNICK:
                irc.send(bytes("MODE "+ CHAN +" +o "+ NICK +"\n", "UTF-8"))

        if CMD == "!voice":
            if NICK == OWNERNICK:
                if len(MSG.split()) > 1:
                    VICTIME = MSG.split()[1]
                else:
                    VICTIME = NICK                             
                irc.send(bytes("MODE "+ CHAN +" +v "+ VICTIME +"\n", "UTF-8"))
        
        if CMD == "!devoice":
            if NICK == OWNERNICK:
                if len(MSG.split()) > 1:
                    VICTIME = MSG.split()[1]
                else:
                    VICTIME = NICK       
                irc.send(bytes("MODE "+ CHAN +" -v "+ VICTIME +"\n", "UTF-8"))        
                       
       
        if SETDEBUG == 1:
            irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" dit sur " + CHAN +" : "+ MSG +" \n", "UTF-8"))
   
    else:  ##SI MSG EN PRIVE
        CMD = MSG.split()[0]
        #MERCI DE LAISSER CE CODE
        if CMD == "VERSION": #NE PAS TOUCHER
            irc.send(bytes("NOTICE "+ NICK +" :VERSION "+ SETVERSIONBASE +" . "+ SETVERSIONPLUS +"  \n", "UTF-8"))#NE PAS TOUCHER
        if SETDEBUG == 1:
            irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" me dit en prive " + CMD +" : "+ MSG +" \n", "UTF-8"))
	
def case_NICK(): #gestion des changements de pseudo
    NICK = args.split('!')[0][3:]
    NEWNICK = args.split() [2][1:]
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" change de pseudo en " + NEWNICK +" \n", "UTF-8"))
	
def case_JOIN(): #gestion des joins
    NICK = args.split('!')[0][3:]
    CHAN = args.split() [2][1:]
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" JOIN "+ CHAN +" \n", "UTF-8"))
	
def case_PART(): #gestion des part
    NICK = args.split('!')[0][3:]
    CHAN = args.split() [2][1:]
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" PART "+ CHAN +" \n", "UTF-8"))
	
def case_TOPIC(): #gestion des topic
    NICK = args.split('!')[0][3:]
    CHAN = args.split()[2]
    TOPIC = " ".join(map(str, args.split()[3:]))[1:]
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" TOPIC "+ CHAN +" : "+ TOPIC +" \n", "UTF-8"))

def case_KICK(): #gestion des kick
    NICK = args.split('!')[0][3:]
    CHAN = args.split()[2]
    VICTIME = args.split()[3]
    RAISON = " ".join(map(str, args.split()[4:]))[1:]
    if VICTIME == BOTNICK:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : Un sale aux trou ("+ NICK +") m'a éxclu de "+ CHAN +" pour "+ RAISON +". J'y retourne de ce pas \n", "UTF-8"))
        irc.send(bytes("JOIN "+ CHAN +" \n", "UTF-8"))
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ VICTIME +" Exclus de "+ CHAN +" par "+ NICK +" pour "+ RAISON +" \n", "UTF-8"))
	
def case_QUIT(): #gestion des quitsafaire
    NICK = args.split('!')[0][3:]
    RAISON = " ".join(map(str, args.split()[2:]))[1:]
    if SETDEBUG == 1:
        irc.send(bytes("PRIVMSG "+ BACKCHAN +" : "+ NICK +" Quit pour : "+ RAISON +" \n", "UTF-8"))
    
def default():
    print(args)

while 1:    
    args = irc.recv(2040)
    args = str(args).replace('\\r\\n\'', '')
    #premier nettoyage du code couleur a vous de perfectionner (PS merci de me le partager si vous avez mieu)
    args = str(args).replace('\\x1f', '').replace('\\x02','').replace('\\x03','').replace('\\x1D','').replace('\\x1F','').replace('\\x16','').replace('\\x0F','')
    

    print(args)
    #print(args)   #ECHO EN CONSOLE
    
    #Gestion du ping
    if args.find('PING') != -1:
        PONG = "".join(map(str, args.split()[1]))                    
        irc.send(bytes('PONG ' + PONG + '\r\n', "UTF-8")) 
   
    RAW = args.split()[1]

    print(args.split()[1])
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

