# module imports
import time
import configparser
import getpass
import hashlib
# ====================================================
config_file = 'config.ini'
data_file = 'data.ini'

# check username availability
def checkAvailability(username):
    config = configparser.ConfigParser()
    config.read(config_file)
    sections = config.sections()
    check_section = username
    available = True
    for s in sections:
        if s == check_section:
            print("Username Already Taken")
            available = False
    return available

# verify username at login
def verifyUsername(username):
    config = configparser.ConfigParser()
    config.read(config_file)
    sections = config.sections()
    check_section = username
    available = False
    for s in sections:
        if s == check_section:
            available = True
    return available

# check patient detail availability
def verifyPatient(patient_name):
    config = configparser.ConfigParser()
    config.read(data_file)
    sections = config.sections()
    check_section = patient_name
    available = False
    for s in sections:
        if s == check_section:
            available = True
    return available

# verfity password at login
def verifyPassword(username, password):
    config = configparser.ConfigParser()
    config.read(config_file)
    en_password = config.get(username, "password")
    if (en_password == encrypt(password)):
        print("***password verified***")
        return True
    else:
        print("***incorrect password***")
        return False

# md5 encryption for passwords
def encrypt(password):
    algorithm = hashlib.md5()
    algorithm.update(password.encode())
    encrypted = algorithm.hexdigest()
    return encrypted

# session
def session(username):
    print("Welcome to your account ")
    config = configparser.ConfigParser()
    config.read(config_file)
    privilege_level = config.get(username, "privilege_level")
    if privilege_level == 'admin_0':
        patientSession(username)
    else:
        staffSession(privilege_level)

# staff session
def staffSession(privilege_level):
    while True:
        print("Options: \n 1.View or Edit Patient Details \n 2.Create New Patient Record \n 3.logout")
        option = input("> ")
        if option == "3":
            print("Logging out...")
            time.sleep(2)
            break
        elif option == "1":
            config = configparser.ConfigParser()
            config.read(data_file)
            patient_name = input("Enter patient name: ")
            patient_name = patient_name + " " + "patient"
            if(verifyPatient(patient_name)):
                print("options: \n 1.view details \n 2.edit details")
                option = input('> ')
                if option == '1':
                    viewSession(patient_name, privilege_level)
                elif option == '2':
                    editSession(patient_name, privilege_level)
            else:
                print("No Records")
        elif option == "2":
            config = configparser.ConfigParser()
            config.read(data_file)
            if (privilege_level=='admin_4'):
                patient_name = input("Enter patient name: ")
                patient_name = patient_name + " " + "patient"
                if not (verifyPatient(patient_name)):
                    personal_details = input("Enter personal details: ")
                    config[patient_name] = {"personal_details": personal_details,
                                            "sickness_details": "",
                                            "drug_prescription": "",
                                            "lab_test_prescription": ""}
                    with open('data.ini', 'w') as configfile:
                        config.write(configfile)
                else:
                    print('Patient details already exist')
            else:
                print('You do not have permission to create new records')
        else:
            print("Not an option!")
            continue

# view only session
def viewSession(patient_name, pl):
    config = configparser.ConfigParser()
    config.read(data_file)
    while True:
        print("View Options: \n 1.personal details \n 2.sickness details \n 3.drug prescriptions \n 4.lab test prespriptions \n 5.back")
        option = input('> ')
        if option == '1':
            print("\n=====================")
            print(config.get(patient_name, "personal_details"))
            print("===================== \n")
            continue
        elif option == '2':
            if (pl=='admin_0' or pl=='admin_1' or pl=='admin_2' or pl=='admin_5'):
                print("\n=====================")
                print(config.get(patient_name, "sickness_details"))
                print("===================== \n")
            else:
                print('You do not have permission to view this section')
            continue
        elif option == '3':
            if (pl=='admin_0' or pl=='admin_1' or pl=='admin_2' or pl=='admin_5'):
                print("\n=====================")
                print(config.get(patient_name, "drug_prescription"))
                print("===================== \n")
            else:
                print('You do not have permission to view this section')
            continue
        elif option == '4':
            if (pl=='admin_0' or pl=='admin_1' or pl=='admin_2' or pl=='admin_3'):
                print("\n=====================")
                print(config.get(patient_name, "lab_test_prescription"))
                print("===================== \n")
            else:
                print('You do not have permission to view this section')
            continue
        elif option == '5':
            break

# edit file session
def editSession(patient_name, pl):
    config = configparser.ConfigParser()
    config.read(data_file)
    while True:
        print("Select a section to Edit: \n 1.personal details \n 2.sickness details \n 3.drug prescriptions \n 4.lab test prespriptions \n 5.back/save")
        option = input('> ')
        if option == '2':
            if (pl == "admin_1" or pl == "admin_2"):
                details_old = config.get(patient_name, 'sickness_details')
                print('Old Record: ', details_old)
                print("Enter New Details:")
                details_new = input('> ').strip()
                mode = input("Do you want to keep old records (Y/N): ")
                while True:
                    if (mode == 'y' or mode == 'Y'):
                        details = details_old + ', ' + details_new
                        break
                    elif (mode == 'n' or mode == 'N'):
                        details = details_new
                        break
                    else:
                        print("(Y/N)??")
                        continue
                config.set(patient_name, 'sickness_details', details)
                print(config.get(patient_name, 'sickness_details'))
                print('Updated Successfully')
            else:
                print('You do not have permission to edit this section')
        elif option == '1':
            if (pl == "admin_4"):
                details_old = config.get(patient_name, 'personal_details')
                print('Old Record: ', details_old)
                print("Enter New Details:")
                details_new = input('> ').strip()
                mode = input("Do you want to keep old records (Y/N): ")
                while True:
                    if (mode == 'y' or mode == 'Y'):
                        details = details_old + ', ' + details_new
                        break
                    elif (mode == 'n' or mode == 'N'):
                        details = details_new
                        break
                    else:
                        print("(Y/N)??")
                        continue
                config.set(patient_name, 'personal_details', details)
                print(config.get(patient_name, 'personal_details'))
                print('Updated Successfully')
            else:
                print('You do not have permission to edit this section')
        elif option == '3':
            if (pl == "admin_1" or pl == "admin_2"):
                details_old = config.get(patient_name, 'drug_prescription')
                print('Old Record: ', details_old)
                print("Enter New Details:")
                details_new = input('> ').strip()
                mode = input("Do you want to keep old records (Y/N): ")
                while True:
                    if (mode == 'y' or mode == 'Y'):
                        details = details_old + ', ' + details_new
                        break
                    elif (mode == 'n' or mode == 'N'):
                        details = details_new
                        break
                    else:
                        print("(Y/N)??")
                        continue
                config.set(patient_name, 'drug_prescription', details)
                print(config.get(patient_name, 'drug_prescription'))
                print('Updated Successfully')
            else:
                print('You do not have permission to edit this section')
        elif option == '4':
            if (pl == "admin_1" or pl == "admin_2" or pl == "admin_3"):
                details_old = config.get(patient_name, 'lab_test_prescription')
                print('Old Record: ', details_old)
                print("Enter New Details:")
                details_new = input('> ').strip()
                mode = input("Do you want to keep old records (Y/N): ")
                while True:
                    if (mode == 'y' or mode == 'Y'):
                        details = details_old + ', ' + details_new
                        break
                    elif (mode == 'n' or mode == 'N'):
                        details = details_new
                        break
                    else:
                        print("(Y/N)??")
                        continue
                config.set(patient_name, 'lab_test_prescription', details)
                print(config.get(patient_name, 'lab_test_prescription'))
                print('Updated Successfully')
            else:
                print('You do not have permission to edit this section')
        elif option == '5':
            break
    config.write(open('data.ini', 'w'))

# patient session
def patientSession(username):
    while True:
        print("Options: \n 1.view history \n 2.logout")
        option = input("> ")
        if option == "2":
            print("Logging out...")
            time.sleep(2)
            break
        elif option == "1":
            if(verifyPatient(username)):
                viewSession(username,'admin_0')
            else:
                print("No Records")
        else:
            print("Not an option")

#staff verification
def staffVerification(v_code):
    config = configparser.ConfigParser()
    config.read(config_file)
    sections = config.sections()
    return (config.get("staff verification", v_code,fallback='1234567'))



# register
def register():
    while True:
        username = input("New username: ").strip()
        print("Enter User Type: ")
        print("Options: staff | patient")
        user_type = input("> ")
        if user_type == "patient":
            privilege_level = "admin_0"
            username = username + " " + "patient"
            if not (checkAvailability(username)):
                continue
            break
        elif user_type == "staff":
            username = username + " " + "staff"
            if not (checkAvailability(username)):
                continue
            while True:
                print("Enter provided verfication code:")
                v_code = input("> ").strip()
                staff_type = staffVerification(v_code)
                ##print(staffVerification(v_code))
                user_type = staff_type
                if staff_type == "doctor":
                    print("Account type:", staff_type)
                    privilege_level = "admin_1"
                    break
                elif staff_type == "nurse":
                    print("Account type:", staff_type)
                    privilege_level = "admin_2"
                    break
                elif staff_type == "lab":
                    print("Account type:", staff_type)
                    privilege_level = "admin_3"
                    break
                elif staff_type == "receptionist":
                    print("Account type:", staff_type)
                    privilege_level = "admin_4"
                    break
                elif staff_type == "pharmacy":
                    print("Account type:", staff_type)
                    privilege_level = "admin_5"
                    break
                else:
                    print("please check the verification code..")
                    continue
            break
        else:
            print(user_type + " is not an option")
            continue
    while True:
        password = getpass.getpass(prompt="New password: ")
        if not len(password) > 0:
            print("Password can't be blank")
            continue
        else:
            confirm_password = getpass.getpass(prompt="Confirm Password: ")
            if (password == confirm_password):
                print("Passwords Matched...")
                break
            else:
                print("Not Matching.Please Re-enter...")
                continue
    print("Creating account...")
    en_password = encrypt(password)

    config = configparser.ConfigParser()
    config.read('config.ini')
    config[username] = {"password": en_password,
                        "user_type": user_type,
                        "privilege_level": privilege_level}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    time.sleep(1)
    print("Account has been created")

# Login
def login():
    while True:
        username = input("Username: ")
        if not len(username) > 0:
            print("Username can't be blank")
            continue
        else:
            print("Enter User Type: ")
            print("Options: staff | patient")
            user_type = input("> ")
            if (user_type == 'staff') or (user_type == 'patient'):
                username = username + " " + user_type
                if(verifyUsername(username)):
                    print("***user verfied***")

                    while True:
                        password = getpass.getpass(prompt="Password: ")
                        if(verifyPassword(username, password)):
                            session(username)
                            break
                        else:
                            continue
                    break
                else:
                    print("invalid username or user type")
                    continue
            else:
                print(user_type + " is not an option")
                continue

# Start
print("Welcome to the Medical Data Processing System. Please Register or Login.")
while True:
    print("Options: register | login | exit")
    option = input("> ")
    if option == "login":
        login()
    elif option == "register":
        register()
    elif option == "exit":
        break
    else:
        print(option + " is not an option")

# Exit
print("Shutting down...")
time.sleep(1)
