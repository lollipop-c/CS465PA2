import sys

currentUser = {}
userlist = []
grouplist = []
filelist  = []


def converTORWX(permi):
    permission = []
    i = 0
    for p in permi:
        if i == 0 or i == 3 or i ==6:
            if permi[i] == 0:
                permission .append('-');
            else :
                permission.append("r")
        elif i== 1 or i==4 or i==7:
            if permi[i] == 0:
                permission .append('-');
            else :
                permission.append("w")
        else :
            if permi[i] == 0:
                permission .append('-');
            else :
                permission.append("x")
        i = i + 1
    p1 = ''.join(permission[:3])
    p2 = ''.join(permission[3:6])
    p3 = ''.join(permission[6:9])

    return p1+" "+p2+" "+p3
def isUserInList(username):
    for user in userlist :
        if user['username'] == username:
            return True
    return False
def isGrpInList(groupname):
    for group in grouplist:
        if group['groupname'] == groupname:
            return True
    return False
def isFileInList(filename):
    for file in filelist:
        if file['filename'] == filename:
            return True
    return False

def useradd(username, password):


    f_audit = open("audit.txt","a")
    f = open("account.txt","a")

    if currentUser:

        if currentUser['username'] != "root":
            print("ERROR:only root user can add group ")
            f_audit.write("ERROR:only root user can  add group\n")
            return


    if isUserInList(username):
        print("The username exist, create user failed, please use other name")
        f_audit.write("The username exist, create user failed, please use other name\n")
        return
    else:
        new_user = {"username": username,
                "password": password,
                "group": []
                }
        userlist.append(new_user)
    if new_user!= None:
        print("User "+ new_user['username'] +" created")
        f_audit.write("User "+ new_user['username'] +" created\n")
        f.write(username+" "+password+"\n")
    f.close()
    f_audit.close()



def login(username, password):
    f_audit = open("audit.txt","a")
    global currentUser

    up_list = []
    for line in open("account.txt"):
        users, pwd = line.split(" ")
        user_pwd = {"name":users,
                    "pwd":pwd}
        up_list.append(user_pwd)

    if currentUser:
        print("The System can only login one user at a time")
        f_audit.write("The System can only login one user at a time\n")
        return
    for user in userlist :
        if user['username'] == username:
            if user['password'] == password:
                currentUser = user
                print("User " + user['username'] +" logged in")
                f_audit.write("User " + user['username'] +" logged in\n")
                return
    print("ERROR:Password or Username is incorrect ")
    f_audit.write("ERROR:Password or Username is incorrect \n")
    f_audit.close()




def logout():

    global currentUser
    f_audit = open("audit.txt", "a")
    if currentUser:

        print("User " + currentUser['username'] + " logged out")
        f_audit.write("User " + currentUser['username'] + " logged out\n")
        currentUser= {}

    else:
        print("ERROR:user must be logged in first!")
        f_audit.write("ERROR:user must be logged in first!\n")
    f_audit.close()



def groupadd(groupname):
    f_audit = open("audit.txt", "a")

    if currentUser['username'] != "root":
        print("ERROR:only root user can add group ")
        f_audit.write("ERROR:only root user can  add group\n")
        return


    if isGrpInList(groupname):
        print("ERROR:The group name is existed, create group failed, please use other name")
        f_audit.write("ERROR:The group name is existed, create group failed, please use other name\n")
        return
    if groupname == "nil":
        print("ERROR:Group can not have the name 'nil'")
        f_audit.write("ERROR:Group can not have the name 'nil'\n")
        return
    new_group={'groupname':groupname,
           'user_contained':[]}
    grouplist.append(new_group)
    if new_group!=None:
        print("Group "+ new_group['groupname'] +" created")
        f_audit.write("Group "+ new_group['groupname'] +" created\n")
    f_audit.close()


def usergrp(username,groupname):
    f_audit = open("audit.txt", "a")
    if not isGrpInList(groupname):
        print("ERROR: The group does not exist")
        f_audit.write("ERROR: The group does not exist\n")
    if not isUserInList(username):
        print("ERROR: The user does not exist")
        f_audit.write("ERROR: The user does not exist\n")

    for user in userlist:
        if user['username'] == username:
            user["group"].append(groupname)
            for group in grouplist:
                if group['groupname'] == groupname:
                    group["user_contained"].append(user['username'])
            print("User "+user['username']+" added to group "+groupname)
    f_audit.write("User "+user['username']+" added to group "+groupname+"\n")
    f_audit.close()



def mkfile(filename):
    f_audit = open("audit.txt", "a")

    global currentUser
    if isFileInList(filename):
        print("ERROR:The file name is existed, create file failed, please use other name")
        f_audit.write("ERROR:The file name is existed, create file failed, please use other name\n")

    f = open(filename, "w")
    new_file = {"filename":filename,
                "permissions":[1,1,0,0,0,0,0,0,0],
                "owner": currentUser,
                "group":"nil"}
    filelist.append(new_file)
    if new_file :
        print("File" + new_file['filename'] + " with owner " + new_file['owner']['username'] + "and default "
                                                                                               "permissions created")
        f_audit.write("File" + new_file['filename'] + " with owner " + new_file['owner']['username'] + "and default "
                                                                                               "permissions created\n")
    f_audit.close()


def chmod(filename,rwx1,rwx2,rwx3):
    f_audit = open("audit.txt", "a")


    permissions =[]

    permissions.append(rwx1)
    permissions.append(rwx2)
    permissions.append(rwx3)
    permission = ''.join(permissions)
    permi = []
    for p in permission:
        if p == 'r' or p == 'w' or p == 'x':
            permi.append(1)
        else: permi.append(0)


    if not isFileInList(filename):
        print("ERROR:File does not exist")
        f_audit.write("ERROR:File does not exist\n")
    for file in filelist:
        if file['filename'] == filename:
            file['permissions'] = permi
            print("Permissions for "+file['filename']+"set to "+converTORWX(permi)+" by " +currentUser['username'])
            f_audit.write("Permissions for "+file['filename']+"set to "+converTORWX(permi)+" by " +currentUser['username']+"\n")
    f_audit.close()


def chown(filename,username):
    f_audit = open("audit.txt", "a")

    if currentUser['username'] != "root":
        print("ERROR:only root user can change the owner of a file")
        f_audit.write("ERROR:only root user can change the owner of a file\n")
        return
    if not isFileInList(filename):
        print("ERROR:File does not exist")
        f_audit.write("ERROR:File does not exist\n")
    elif not isUserInList(username):
        print("ERROR:User does not exist")
        f_audit.write("ERROR:User does not exist\n")
    else:
        for file in filelist:
           if file['filename'] == filename:
               preowner = file['owner']
               for user in userlist:
                   if username == user['username']:
                        file['owner'] =  user
                        print( "Owner of "+preowner['username']+" changed to "+file['owner']['username'])
                        f_audit.write("Owner of "+preowner['username']+" changed to "+file['owner']['username']+"\n")

    f_audit.close()




def chgrp(filename,groupname):
    f_audit = open("audit.txt", "a")


    if not isFileInList(filename):
        print("ERROR:File does not exist")
        f_audit.write("ERROR:File does not exist\n")
    elif not isGrpInList(groupname):
        print("ERROR:Group does not exist")
        f_audit.write("ERROR:Group does not exist\n")
    else:
        for file in filelist:
            if file['filename'] == filename:
                owner = file['owner']
        if currentUser['username'] != "root" and  currentUser['username'] != owner:
            print("ERROR current user is not the owner and not root")
            f_audit.write("ERROR current user is not the owner and not root\n")
            return
        for group in owner['group']:
            if group == groupname or groupname == "nil" or currentUser == "root":
                file['group'] = groupname
                print("Group for "+file['filename']+ "set to "+group+" by "+owner['username'])
                f_audit.write("Group for "+file['filename']+ "set to "+group+" by "+owner['username']+"\n")
                f_audit.close()



def read(filename):
    f_audit = open("audit.txt", "a")

    f = open(filename,"r")
    if not isFileInList(filename):
        print("ERROR:File does not exist")
        f_audit.write("ERROR:File does not exist\n")
    for file in filelist:
        if file['filename'] == filename:
            if currentUser['username'] == "root":
                print("User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read())
                f_audit.write("User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read()+"\n")
            elif currentUser == file['owner'] and file['permissions'][0] == 1:
                print("User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read())
                f_audit.write( "User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read()+ "\n")
            elif  file['group'] in currentUser['group']   and file['permissions'][3] == 1:
                print("User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read())
                f_audit.write(
                    "User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read() + "\n")
            elif file['permissions'][6] == 1:
                print("User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read())
                f_audit.write(
                    "User " + currentUser['username'] + " read " + file['filename'] + " as:" + f.read() + "\n")
            else:
                print("Error, Access Denied")
                f_audit.write("Error, Access Denied\n")
    f.close()
    f_audit .close()


def write(filename, *text):
    f_audit = open("audit.txt", "a")
    text = ' '.join(text[0])
    f = open(filename,"a")
    if not isFileInList(filename):
        print("ERROR:File does not exist")
        f_audit.write("ERROR:File does not exist\n")
    for file in filelist:
        if file['filename'] == filename:
            if currentUser == "root":
                f.write(text+"\n")
                print("User " + currentUser['username']+" wrote to "+file['filename'] + ":" + text)
                f_audit.write("User " + currentUser['username']+" wrote to "+file['filename'] + ":" + text+"\n")
            elif currentUser == file['owner'] and file['permissions'][1] == 1:
                f.write(text+"\n")
                print("User " + currentUser['username'] + " wrote to " + file['filename'] + ":" + text)
                f_audit.write("User " + currentUser['username'] + " wrote to " + file['filename'] + ":" + text + "\n")
            elif file['group'] in currentUser['group'] and file['permissions'][4] == 1:
                f.write(text+"\n")
                print("User " + currentUser['username'] + " wrote to " + file['filename'] + ":" + text)
                f_audit.write("User " + currentUser['username'] + " wrote to " + file['filename'] + ":" + text + "\n")
            elif file['permissions'][7] == 1:
                f.write(text+"\n")
                print("User " + currentUser['username'] + " wrote to " + file['filename'] + ":" + text)
                f_audit.write("User " + currentUser['username'] + " wrote to " + file['filename'] + ":" + text + "\n")
            else:
                print("Error, Access Denied")
                f_audit.write("Error, Access Denied\n")
    f.close()
    f_audit.close()

def execute(filename):
    f_audit = open("audit.txt", "a")
    f = open(filename)
    if not isFileInList(filename):
        print("ERROR:File does not exist")
        f_audit.write("ERROR:File does not exist\n")
        return
    for file in filelist:
        if file['filename'] == filename:
            if currentUser == "root":
                print("FIle "+file['filename']+"  execute by"+currentUser['username'])
                f_audit.write("FIle "+file['filename']+"  execute by"+currentUser['username']+"\n")
            elif currentUser == file['owner'] and file['permissions'][2] == 1:
                print("FIle " + file['filename'] + "  execute by" + currentUser['username'])
                f_audit.write("FIle " + file['filename'] + "  execute by" + currentUser['username']+"\n")
            elif file['group'] in currentUser['group']  and file['permissions'][5] == 1:
                print("FIle " + file['filename'] + "  execute by" + currentUser['username'])
                f_audit.write("FIle " + file['filename'] + "  execute by" + currentUser['username']+"\n")
            elif file['permissions'][8] == 1:
                print("FIle " + file['filename'] + "  execute by" + currentUser['username'])
                f_audit.write("FIle " + file['filename'] + "  execute by" + currentUser['username']+"\n")
            else:
                print("ERROR:User " + currentUser['username']+ " denied execute access to" + file['filename'])
                f_audit.write("FIle " + file['filename'] + "  execute by" + currentUser['username']+"\n")
    f.close()
    f_audit.close()


def ls(filename):
    f_audit = open("audit.txt", "a")
    if currentUser:
        if not isFileInList(filename):
            print("ERROR:File does not exist")
            f_audit.write("ERROR:File does not exist\n")
        for file in filelist:
            if filename == file['filename']:
                print(file['filename']+": "+ file['owner']['username'] +"  "+ file['group']+"  "+converTORWX(file['permissions']))
                f_audit.write(file['filename']+": "+ file['owner']['username'] +"  "+ file['group']+"  "+converTORWX(file['permissions'])+"\n")
    else:
        print("ERROR:user must be logged in first!")
        f_audit.write("ERROR:user must be logged in first!\n")
    f_audit.close()

def end():

    file_f = open("file.txt","w")
    group_f = open("group","w")

    for group in grouplist:
        group_f.write(group['groupname']+": ")
        for user in group['user_contained']:
            group_f.write(user + "  ")

    for file  in filelist:
        file_f.write(file['filename'] + ": " + file['owner']['username']+" " + file['group']+" ")
        file_f.write(converTORWX(file['permissions'])+" \n")

    file_f.close()
    group_f.close()


def main(argv):
    f_audit   = open("audit.txt","w")
    f_audit.close()
    f_account = open("account.txt","w")
    f_account.close()
    f = open(argv[1], "r")
    commands = f.read()
    commands = str(commands).split('\n')
    f.close()

    for command in commands :
        command = str(command).split(' ')
        print(command)
        commandline(command)

def commandline(*parameters):

    global currentUser
    parameters = parameters[0]

    if not userlist:
        if parameters[0] ==  "useradd":
            if parameters[1] == "root":
                useradd(parameters[1], parameters[2])
            else:
                print("ERROR:The first user can only be root")
        else:
            print("ERROR:There is no root user,the first common can only be 'useradd root password'to add a root user")

    else:
        if parameters[0] == "useradd":
            useradd(parameters[1], parameters[2])

        if parameters[0] == "login":
            login(parameters[1], parameters[2])

        if parameters[0] == "logout":
            logout()

        if parameters[0] == "groupadd":
            groupadd(parameters[1])

        if parameters[0] == "usergrp":
            usergrp(parameters[1], parameters[2])

        if parameters[0] == "mkfile":
            mkfile(parameters[1])


        if parameters[0] == "chmod":
            chmod(parameters[1], parameters[2], parameters[3], parameters[4])

        if parameters[0] == "chown":
            chown(parameters[1], parameters[2])

        if parameters[0] == "chgrp":
            chgrp(parameters[1], parameters[2])

        if parameters[0] == "read":
            read(parameters[1])

        elif parameters[0] == "write":
            write(parameters[1], parameters[2:])

        if parameters[0] == "execute":
            execute(parameters[1])

        if parameters[0] == "ls":
            ls(parameters[1])

        if parameters[0] == "end":
            end()


if __name__ == "__main__":
        main(sys.argv)
