from time import *
import threading
import getpass
import socket
import os
import re
import time
import argparse

def upis_u_dat(var, ime_dat): #upis naredbi u dat
    dat = open(ime_dat, 'a')
    dat.write(var)
    dat.write('\n')
    dat.close()

trenutno_vrijeme = strftime("%d.%m.%Y. %H:%M:%S", localtime()) #Vrijeme

print('Pozdrav, dobro dosao...')
print('Datum i vrijeme vaseg pristupa: {}'.format(trenutno_vrijeme))

kucni_dir = os.getenv("HOME")

povijest = kucni_dir + '/.povijest'
while True: #Petlja koja vrti prompt
    korisnik, host, adresa = getpass.getuser(), socket.gethostname(), os.path.abspath(os.getcwd())
    naredba = input('[{0}@{1}:{2}]$ '.format(korisnik, host, adresa)) #Prompt/odzivni znak
    if naredba == 'exit' or naredba == 'logout':
        break;
    lista_sa_naredbom = naredba.split()
    if naredba != "":
        print(lista_sa_naredbom)
        
    if re.match(r"(pwd\s+.*)|(pwd$)", naredba): #pwd naredba
        if re.match(r"pwd\s*$", naredba):
            print(os.path.abspath(os.getcwd()))
            upis_u_dat(naredba, povijest)
        else:
            print('Naredba ne prima parametre ni argumente')
            
    elif re.match(r"(ps\s+.*)|(ps$)", naredba): #ps naredba
        if re.match(r"ps\s*$", naredba):
            print(os.getpid())
            upis_u_dat(naredba, povijest)
        else:
            print('Nepostojeci parametar ili argument')
            
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
            
        
        
    elif naredba == "kill":
        print(naredba)
    elif re.match(r"(cd\s+.*)|(cd$)", naredba): #cd naredba
        def korak_nazad(put, do_kud):
            trenutna = put.split('/')
            print(trenutna)
            nova_adresa = ""
            if do_kud != 0:
                for ele in trenutna[1:do_kud]:
                    nova_adresa += "/"
                    nova_adresa += ele
            else:
                for ele in trenutna[1:]:
                    nova_adresa += "/"
                    nova_adresa += ele
                    
            return nova_adresa
            
        if re.match(r"^cd\s*$", naredba):
            os.chdir(kucni_dir)
        elif re.match(r"cd\s\.{1}\s*$", naredba):
            continue
        elif re.match(r"cd\s\.{2}\s*", naredba):
            os.environ['prethodna'] = korak_nazad(adresa, -1)
            try:
                os.chdir(os.environ['prethodna'])
            except OSError:
                print('Nemate pristup / direktoriju')
        elif re.match(r"cd\s\.{0,1}(\/[^\.\.]+)+", naredba):
            try:
                os.chdir(korak_nazad(naredba, 0))
            except OSError:
                print('Upisana adresa ne postoji')
        else:
            print('Kriva naredba')
            
        
    elif re.match(r"(date\s.*)|(date\s*$)", naredba): #date naredba
        if re.match(r"date\s*$", naredba):
            print (strftime("%H::%M::%S  %A  %d/%m/%Y"))
            upis_u_dat(naredba, povijest)
        elif re.match(r"date -r\s*$", naredba):
            print (strftime("%d/%m/%Y  %A  %H::%M::%S"))
            upis_u_dat(naredba, povijest)
        elif re.match(r"date -[^r]\s*$", naredba):
            print('Nepostojeci parametar')
        else:
            
            print('Nepostojeci argument')
    
    elif re.match(r"(ls\s+.*)|(ls$)", naredba): #ls naredba
        if re.match(r"ls\s*$", naredba):
            def lsnohidden(path):
                for f in os.listdir(path):
                    if not f.startswith('.'):
                        print (f)
            lsnohidden((os.getcwd()))
            upis_u_dat(naredba, povijest)
        elif re.match(r"ls -l\s*$", naredba):
            def parse_args():
                parser=argparse.ArgumentParser(description='Izlistaj sve fajlove u direktoriju')
                parser.add_argument('directory', type=str, nargs='?', default='.')
                parser.add_argument('--long','-l', action='store_true')
                return parser.parse_args()
            def ls(args):
                
                    from pwd import getpwuid
                    from grp import getgrgid
                    import pprint
                    for f in listdir(args):
                        filestats=os.lstat(os.path.join(args.directory,f))
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
            def listdir(args):
               dirs=os.listdir(args.directory)
               dirs=[dir for dir in dirs if dir[0]!='.']
               return dirs
            args=parse_args()
            ls(args)
            upis_u_dat(naredba, povijest)
        elif re.match(r"ls -[^l]*\s*$", naredba):
            print('Nepostojeci parametar')
        
    elif naredba == "mkdir":
        print(naredba)
    elif naredba == "rmdir":
        print(naredba)
    elif naredba == "kub":
        print(naredba)
    elif re.match(r"\s*$", naredba):
        continue
    else:
        print('pogresna naredba')
