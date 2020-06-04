from time import *
import threading as th
import getpass
import socket
import os
import re
import time
import signal
import sys
from pathlib import Path #za windows compatibility

def upis_u_dat(var, ime_dat): #upis naredbi u dat
    dat = open(ime_dat, 'a')
    dat.write(var)
    dat.write('\n')
    dat.close()

def korak_nazad(put):
    nova_adresa = ""
    if len(put) == 2 and put[1] == '/':
        nova_adresa = "/"
    else:
        trenutna = ""
        trenutna = trenutna.join(put[1])
        trenutna = trenutna.split('/')
        absolutna = os.path.abspath(os.getcwd())
        absolutna = absolutna.split('/')
        iste = False
        if len(trenutna) > 1:
            if absolutna[1] == trenutna[1]:
                iste = True
        if iste == False:
            for x in absolutna:
                if x == "." or x == '':
                    continue
                nova_adresa += "/"
                nova_adresa += x
        for ele in trenutna:
            if ele == "." or ele == '':
                continue
            nova_adresa += "/"
            nova_adresa += ele
    return nova_adresa

trenutno_vrijeme = strftime("%d.%m.%Y. %H:%M:%S", localtime()) #Vrijeme

print('Pozdrav, dobro dosao...')
print('Datum i vrijeme vaseg pristupa: {}'.format(trenutno_vrijeme))

#kucni_dir = os.getenv("HOME")  #radi samo s unixom, na windowsu ne
kucni_dir = str(Path.home())    

povijest = kucni_dir + '/.povijest'
while True: #Petlja koja vrti prompt
    korisnik, host, adresa = getpass.getuser(), socket.gethostname(), os.path.abspath(os.getcwd())
    naredba = input('[{0}@{1}:{2}]$ '.format(korisnik, host, adresa)) #Prompt/odzivni znak
    if naredba == 'exit' or naredba == 'logout':
        break;
    lista_sa_naredbom = naredba.split()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~pwd naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    if re.match(r"(pwd\s+.*)|(pwd$)", naredba): #pwd naredba
        if re.match(r"pwd\s*$", naredba):
            print(os.path.abspath(os.getcwd()))
            upis_u_dat(naredba, povijest)
        else:
            print('Naredba ne prima parametre ni argumente')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~ps naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~           
    elif re.match(r"(ps\s+.*)|(ps$)", naredba): #ps naredba
        if re.match(r"ps\s*$", naredba):
            print(os.getpid())
            upis_u_dat(naredba, povijest)
        else:
            print('Nepostojeci parametar ili argument')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~echo naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    elif re.match(r"(echo\s+.*)|(echo$)", naredba): #echo naredba
        if re.match(r"echo\s*$", naredba):
            print('Naredba prima barem jedan argument')
        else:
            upis_u_dat(naredba, povijest)
            for word in lista_sa_naredbom[1:]:
                if re.match(r'^\"(.*\".*)*\"$', word):
                    word = word[1:-1]
                    print(word, end=" ")
                elif re.match(r'(^\"[^"]+)|([^"]+\"$)|(^\"[^"]+\"$)|(^\"$)', word):
                    izmjena = word.replace('"', '')
                    print(izmjena, end=" ")
                else:
                    print(word, end=" ")
            print()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~kill naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    elif re.match(r"(kill\s+.*)|(kill$)", naredba): #kill naredba
        if re.match(r"kill\s*$", naredba):          #regex za samo kill
            print('Naredba prima tocno jedan parametar: naziv signala ili njegov redni broj')
        elif re.match(r"(kill -2\s*$)|(kill -SIGINT\s*$)|(kill -INT\s*$)", naredba):        #regex za signal broj 2
            def upravljac(broj_signala, stog):
                print('Pristiago je signal broj 2: Program se zavrsava.'.format(broj_signala))
                sys.exit()
                return
            signal.signal(signal.SIGINT,upravljac)   #ceka sigint salje ga upravljacu i on nas obavjestava da je signal dosao
            os.kill(os.getpid(), signal.SIGINT)      #interrupta i zavrsava program
            upis_u_dat(naredba, povijest)
        elif re.match(r"(kill -3\s*$)|(kill -SIGQUIT\s*$)|(kill -QUIT\s*$)", naredba):       #regex za signal broj 3
            signal.signal(signal.SIGQUIT,signal.SIG_IGN)        #ceka da se desi signal broj 3 sig ign znaci da se signal ignorira
            os.kill(os.getpid(), signal.SIGQUIT)                #saljemo signal 3 koji je ignoriran 
            print('Signal broj 3 je ignoriran')
            upis_u_dat(naredba, povijest)
        elif re.match(r"(kill -15\s*$)|(kill -SIGTERM\s*$)|(kill -TERM\s*$)", naredba):      #regex za signal broj 15
            signal.signal(signal.SIGTERM,signal.SIG_DFL)        #ceka da se desi signal broj 3 sig dfl odraduje default funkciju signala
            os.kill(os.getpid(), signal.SIGTERM)                #saljemo signal broj 15 koji terminatea program
            upis_u_dat(naredba, povijest)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~cd naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
    

    elif re.match(r"(cd\s+.*)|(cd$)", naredba): #cd naredba    
        if re.match(r"^cd\s*$", naredba):
            os.chdir(kucni_dir)
        elif re.match(r"cd\s+(\.{0,2}(\/.*)+)|([^\/]+\/{1})+|([^\/]+)", naredba):
            try:
                os.chdir(korak_nazad(naredba.split()))
            except OSError:
                print('Upisana adresa ne postoji')
        else:
            print('Kriva naredba')
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~date naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       
    elif re.match(r"(date\s.*)|(date\s*$)", naredba): #date naredba
        if re.match(r"date\s*$", naredba):            #regex za samo date
            print (strftime("%H::%M::%S  %A  %d/%m/%Y"))       #printa sati::minute::sekunde dan u tjednu dan/mjesec/godina
            upis_u_dat(naredba, povijest)
        elif re.match(r"date -r\s*$", naredba):       #regex za date -r
            print (strftime("%d/%m/%Y  %A  %H::%M::%S"))       #printa dan/mjesec/godina dan u tjednu sati::minute::sekunde
            upis_u_dat(naredba, povijest)
        elif re.match(r"date -[^r]\s*$", naredba):
            print('Nepostojeci parametar')
        else:
            
            print('Nepostojeci argument')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~ls naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
    elif re.match(r"(ls\s+.*)|(ls$)", naredba): #ls naredba
        if re.match(r"(ls\s+[^\-]+.*)|(ls\s*$)", naredba):
            def lsnohidden(path):
                for f in os.listdir(path):
                    if not f.startswith('.'):
                        print (f)
            if re.match(r"ls\s*$", naredba):
                lsnohidden(os.getcwd())
            elif re.match(r"ls\s+[^\-]", naredba):
                try:
                    lsnohidden(korak_nazad(naredba.split()))
                except OSError:
                    print('Upisali ste krivu adresu')
            upis_u_dat(naredba, povijest)
        elif re.match(r"ls -l\s*$", naredba):
            def ls():
                from pwd import getpwuid
                from grp import getgrgid
                import pprint
                for f in listdir():
                    filestats=os.lstat(os.path.join(os.getcwd(),f))
                    mode_chars=['r','w','x']
                    st_perms=bin(filestats.st_mode)[-9:]
                    mode=filetype_char(filestats.st_mode)
                    for i, perm in enumerate(st_perms):
                        if perm=='0':
                            mode+='-'
                        else:
                            mode+=mode_chars[i%3] 
                    entry=[mode,str(filestats.st_nlink),getpwuid(filestats.st_uid).pw_name,getgrgid(filestats.st_gid).gr_name,str(filestats.st_size),f]                          
                    pprint.pprint(entry) 
              
            def filetype_char(mode):
                import stat
                if stat.S_ISDIR(mode):
                    return 'd'
                if stat.S_ISLNK(mode):
                    return 'l'
                return '-'
            
            def listdir():
                dirs=os.listdir(os.getcwd())
                dirs=[dir for dir in dirs if dir[0]!='.']
                return dirs
                
            ls()
            upis_u_dat(naredba, povijest)
        elif re.match(r"ls\s+-l+[^\-]", naredba):
            def ls():
                    from pwd import getpwuid
                    from grp import getgrgid
                    import pprint
                    for f in listdir():
                        var=naredba.split()
                        var=var[1:]
                        filestats=os.lstat(os.path.join(korak_nazad(var),f))
                        mode_chars=['r','w','x']
                        st_perms=bin(filestats.st_mode)[-9:]
                        mode=filetype_char(filestats.st_mode)
                        for i, perm in enumerate(st_perms):
                            if perm=='0':
                                mode+='-'
                            else:
                                mode+=mode_chars[i%3] 
                        entry=[mode,str(filestats.st_nlink),getpwuid(filestats.st_uid).pw_name,getgrgid(filestats.st_gid).gr_name,str(filestats.st_size),f]                          
                        pprint.pprint(entry) 
              
            def filetype_char(mode):
                import stat
                if stat.S_ISDIR(mode):
                    return 'd'
                if stat.S_ISLNK(mode):
                    return 'l'
                return '-'
            
            def listdir():
               var=naredba.split()
               var=var[1:]
               dirs=os.listdir(korak_nazad(var))
               dirs=[dir for dir in dirs if dir[0]!='.']
               return dirs
            try:   
                ls()
            except FileNotFoundError:
                print('Upisali ste krivu adresu')
            upis_u_dat(naredba, povijest)
        elif re.match(r"ls -l.*$", naredba):
            print('Nepostojeci parametar')
        elif re.match(r"ls -[^l]*\s*$", naredba):
            print('Nepostojeci parametar')
            
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~mkdir naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~            
    elif re.match(r"(mkdir\s+.*)|(mkdir$)", naredba):  
        if re.match(r"mkdir\s*$", naredba):             #regex za ako korisnik upise samo mkdir bez argumenata
            print("Naredba mora primiti argument")     
        elif (len(lista_sa_naredbom)>=3):       #ako naredba ima vise od jednog argumenta javi gresku
            print ("Naredba ne smije imati vise od jednog argumenta")       
        else:                                           #izvedi ovo ako je dobro upisana naredba
            for word in lista_sa_naredbom[1:2]:         
                argument=word                           
            try:
                os.makedirs(argument)                   #stvaranje direktorija
            except FileExistsError:                     #ako direktorij postoji, javi ovu gresku
                print("Ovaj direktorij vec postoji!")
            except OSError:                             #pri javljanju neke druge greske (npr ako nema mjesta na disku) javi ovu gresku
                print("Stvaranje direktorija nije uspjelo!")
            upis_u_dat(naredba, povijest)               #upis u povjest
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~rmdir naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif re.match(r"(rmdir\s+.*)|(rmdir$)", naredba):   
        if re.match(r"rmdir\s*$", naredba):             #regex za ako korisnik upise samo rmdir bez ikakvih argumenata
            print("Naredba mora primiti argument")      
        elif (len(lista_sa_naredbom)>=3):               #ako naredba ima vise od jednog argumenta javi gresku
            print ("Naredba ne smije imati vise od jednog argumenta")
        else:                                           #izvedi ovo kad je naredba dobro upisana
            for word in lista_sa_naredbom[1:2]:         
                argument=word
            try:
                os.rmdir(argument)                      #brisanje direktorija
            except FileNotFoundError:
                print("Direktorij nije pronadena!")       #greska koja se ispisuje ako je argument direktorij koji ne postoji
            except OSError:
                print("Brisanje direktorija nije uspjelo, direktorij nije prazan")     #greska koja se ispisuje kad direktorij koji se brise nije prazan
            upis_u_dat(naredba, povijest)               #upis u povjest
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~kub naredba~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif re.match(r"kub\s*$", naredba):
        broj_za_oduzimanje = 29290290290290290290
        adresa_rez = kucni_dir + '/rezultat.txt'

        barijera = th.Barrier(3)
        lock = th.Lock()
        
        rez = open(adresa_rez, 'r+')
        rez.truncate(0)
        rez.close
        
        def thread_kub(n):
            lock.acquire()
            rez = open(adresa_rez, 'a')
            global broj_za_oduzimanje
            for i in range(n):
                print(i, end=" ")
                print(broj_za_oduzimanje)
                broj_za_oduzimanje -= i**3
                rez.write('N = {}'.format(broj_za_oduzimanje))
                rez.write('\n')
                
            rez.write('Kraj threada')
            rez.write('\n')
            rez.close()
            lock.release()
            id_threada = barijera.wait()
            if id_threada == 1:
                print('Dretve se prosle barijeru i izvrsile su program')
            

        nit1 = th.Thread(target = thread_kub, args=(100000,))        
        nit2 = th.Timer(2, thread_kub, args=(100000, ))
        nit3 = th.Thread(target = thread_kub, args=(100000,))
        
        nit1.start()
        nit2.start()
        nit3.start()

        nit1.join()
        nit3.join()
        nit2.join()

        upis_u_dat(naredba, povijest)
    elif re.match(r"kub\s+\-+.*\s*", naredba):   # ako korisnik upise
        print('Naredba ne prima parametre')      # parametre ili
    elif re.match(r"kub\s+[^\-]+\s*", naredba):  # argumente
        print('Naredba ne prima argumente')      # ispisuje gresku
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~        
    elif re.match(r"\s*$", naredba):
        continue
    else:
        print('pogresna naredba')
