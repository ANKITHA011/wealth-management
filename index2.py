import random
import sqlite3


def check_luhn_algo(checkme):
    converting_to_int_list = []
    for item in list(checkme):
        converting_to_int_list.append(int(item))
    luhn_card_no = converting_to_int_list[:-1]
    tmp_list = luhn_card_no.copy()
    for i in range(0, len(tmp_list), 2):
        tmp_list[i] *= 2
        if tmp_list[i] > 9:
            tmp_list[i] -= 9
    checksum = list(str(10 - sum(tmp_list) % 10))
    if len(checksum) != 1:
        checksum = [0]
    luhn_card_no.extend(checksum)
    del tmp_list
    card_no_for_db = ''.join(map(str, luhn_card_no))
    if card_no_for_db == checkme:
        return True
    else:
        return False


def create_account():
    def get_code():
        code = ""
        for each in random.sample(range(9), k=4):
            code += str(each)
        return code

    conn = sqlite3.connect("PAM.s3db")
    curr = conn.cursor()
    iin = [4, 0, 0, 0, 0, 0]
    random_acc_no = random.sample(range(9), 9)
    luhn_card_no = []
    luhn_card_no.extend(iin)
    luhn_card_no.extend(random_acc_no)
    tmp_list = luhn_card_no.copy()
    for i in range(0, len(tmp_list), 2):
        tmp_list[i] *= 2
        if tmp_list[i] > 9:
            tmp_list[i] -= 9
    checksum = list(str(10 - sum(tmp_list) % 10))
    if len(checksum) != 1:
        checksum = [0]
    luhn_card_no.extend(checksum)
    del tmp_list
    ACC_no_for_db = ''.join(map(str, luhn_card_no))
    code_for_db = get_code()
    print("\nYour Account has been created")
    print("Your Account number:\n{}\nYour sceurity code:\n{}\n".format(ACC_no_for_db, code_for_db))
    curr.execute('SELECT id from PAM2;')
    db_return = curr.fetchall()
    try:
        listofrows = (lambda l: [item for sublist in l for item in sublist])(db_return)
        myid = max(listofrows)
    except ValueError:
        myid = 0
    dontsqlinjectme = (myid, ACC_no_for_db, code_for_db)
    curr.execute('INSERT INTO PAM2 (id, number, pin) VALUES (?, ?, ?);', dontsqlinjectme)
    conn.commit()


def retrieve_from_db(user_enters_card_no, user_enters_pin):
    conn = sqlite3.connect("PAM.s3db")
    curr = conn.cursor()
    Acc_number = user_enters_card_no
    code = user_enters_pin
    dontsqlinjectme = (Acc_number, code)
    curr.execute('SELECT number, pin FROM PAM2 WHERE number = ? and pin = ?;', dontsqlinjectme)
    db_return = curr.fetchone()
    match = False
    try:
        if Acc_number in db_return and code in db_return:
            match = True
            print("You have successfully logged in!")
    except sqlite3.OperationalError:
        print("\nWrong Account number or PIN!\n")
    except TypeError:
        print("\nWrong Security code or PIN!\n")
    while match:
        print("Personal Asset Management System\n1. Balance\n2. Add Asset\n3. Transfer asset\n4. Close account\n5.Log out\n0.Exit")
        second_menu_choice = int(input())
        if second_menu_choice == 1:
            curr.execute('SELECT balance FROM PAM2 WHERE number = ? and pin = ?;', (Acc_number, code))
            db_return = curr.fetchone()
            print("\nBalance: {}\n".format(db_return[0]))
        elif second_menu_choice == 2:
            print("\nEnter Asset Type:")
            print("Please Select the Asset Type\n1. ~GOLD\n2.Stock\n3.Liquid Cash~")
            a = input()
            if a == "1":
                #asset_type = "Gold"
                #print("Enter Asset type")
                print("Enter the Asset Value")
                dontsqlinjectme = (int(input()), Acc_number, code)
                curr.execute('UPDATE PAM2 SET asset_value = asset_value + ? WHERE number = ? and pin = ?;', dontsqlinjectme)
                curr.execute('UPDATE PAM2 SET balance = balance + ? WHERE number = ? and pin = ?;', dontsqlinjectme)
                conn.commit()
                curr.execute('SELECT asset_value FROM PAM2 WHERE number = ? and pin = ?;', (Acc_number,code))
                db_return = curr.fetchone()
                print("\nAsset Value: {}\n".format(db_return[0]))
                print("Gold of value is added!")
            if a == "2":
                #asset_type = ""
                #print("Enter Asset type")
                print("Enter the Asset Value")
                dontsqlinjectme = (int(input()), Acc_number, code)
                curr.execute('UPDATE PAM2 SET asset_value = asset_value + ? WHERE number = ? and pin = ?;', dontsqlinjectme)
                curr.execute('UPDATE PAM2 SET balance = balance + ? WHERE number = ? and pin = ?;', dontsqlinjectme)
                conn.commit()
                curr.execute('SELECT asset_value FROM PAM2 WHERE number = ? and pin = ?;', (Acc_number,code))
                db_return = curr.fetchone()
                print("\nAsset Value: {}\n".format(db_return[0]))
                print("stock of value is added!")
            if a == "3":
                #asset_type = "Gold"
                #print("Enter Asset type")
                print("Enter the Asset Value")
                dontsqlinjectme = (int(input()), Acc_number, code)
                curr.execute('UPDATE PAM2 SET asset_value = asset_value + ? WHERE number = ? and pin = ?;', dontsqlinjectme)
                curr.execute('UPDATE PAM2 SET balance = balance + ? WHERE number = ? and pin = ?;', dontsqlinjectme)
                conn.commit()
                curr.execute('SELECT asset_value FROM PAM2 WHERE number = ? and pin = ?;', (Acc_number,code))
                db_return = curr.fetchone()
                print("\nAsset Value: {}\n".format(db_return[0]))
                print("Liquid cash of value is added!")
           
            
        elif second_menu_choice == 3:
            global transfer_destination
            transfer_destination = []
            print("Enter Account number:")
            user_enters_transferdest = input()
            if len(user_enters_transferdest) != 16:
                print("\nProbably you made a mistake in the card number.\nPlease try again!\n")
                continue
            elif len(user_enters_transferdest) == 16:
                if user_enters_transferdest == Acc_number:
                    print("\nYou can't transfer money to the same account!\n")
                    continue
                elif not check_luhn_algo(user_enters_transferdest):
                    '# IF CHECK LUHN ALGO RETURNS FALSE. NOT FALSE = TRUE AND THEN WE CONTINUE'
                    print("\nLUHN CHECK:Probably you made a mistake in the card number.\nPlease try again!\n")
                    continue
                else:
                    transfer_destination = (int(user_enters_transferdest),)
            curr.execute('SELECT number FROM PAM2 WHERE number = ?;', transfer_destination)
            db_return = curr.fetchone()
            try:
                len(db_return)
                print("Please Select the Asset Type you want to transfer\n1. ~GOLD\n2.Stock\n3.Liquid Cash~")
                a = input()
                if a == "1":
                    print("Enter the Asset Value you want to transfer\n")
                    user_enters_transfermoney = int(input())
                    curr.execute('SELECT balance FROM PAM2 WHERE number = ? and pin = ?', (Acc_number, code))
                    db_return = curr.fetchone()
                if a == "2":
                    print("Enter the Asset Value you want to transfer\n")
                    user_enters_transfermoney = int(input())
                    curr.execute('SELECT balance FROM PAM2 WHERE number = ? and pin = ?', (Acc_number, code))    
                    db_return = curr.fetchone()
                if a == "3":
                    print("Enter the Asset Value you want to transfer\n")
                    user_enters_transfermoney = int(input())
                    curr.execute('SELECT balance FROM PAM2 WHERE number = ? and pin = ?', (Acc_number, code))    
                    db_return = curr.fetchone()
                if user_enters_transfermoney > db_return[0]:
                    print("\nNot enough money!\n")
                    continue
                else:
                    curr.execute('UPDATE PAM2 SET balance = balance + ? WHERE number = ?;', (
                        user_enters_transfermoney, int(user_enters_transferdest)))
                    curr.execute('UPDATE PAM2 SET balance = balance - ? WHERE number = ?;', (
                        user_enters_transfermoney, Acc_number))
                    conn.commit()
                    print("\nSuccess!\n")
                    continue
            except TypeError:
                print("\nSuch a card does not exist.\n")
                continue

        elif second_menu_choice == 4:
            dontsqlinjectme = (Acc_number, code)
            curr.execute('DELETE FROM PAM2 WHERE number = ? and pin = ?;', dontsqlinjectme)
            conn.commit()
            print("\nThe account has been closed!\n")
            break
        elif second_menu_choice == 5:
            print("You have successfully logged out!")
            match = False
        elif second_menu_choice == 0:
            print("Bye!")
            conn.close()
            exit()


def create_db():
    conn = sqlite3.connect("PAM.s3db")
    curr = conn.cursor()
    id = 1
    curr.execute('create table PAM2 (id INTEGER , number TEXT, pin TEXT, balance INTEGER default 0, asset_value INTEGER default 0);')
    conn.commit()
    id = id + 1


program_is_running = True
create_db()
while program_is_running:
    print("#######  Personal Money Management System #######\n1. Create New Account(Auto Generated)\n2. Log Account\n0. Exit")
    first_menu_choice = int(input())
    if first_menu_choice == 1:
        create_account()
    elif first_menu_choice == 2:
        print("Enter your card number:")
        user_enters_card_no = input()
        print("Enter your PIN:")
        user_enters_pin = input()
        retrieve_from_db(user_enters_card_no, user_enters_pin)
    elif first_menu_choice == 0:
        print("Thank you! Bye!")
        program_is_running = False