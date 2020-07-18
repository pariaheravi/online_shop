import json 
from json import JSONEncoder
import sys
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode
from getpass import getpass
key = 'paria'

class person:
    def __init__(self, Name, PhoneNumber, Address, Email, Password):
        self . Name = Name
        self . PhoneNumber = PhoneNumber
        self . Address = Address
        self . Email = Email
        self . Password = Password

# object to JSON
class person_data(JSONEncoder):
    def default(self, o):
        return o.__dict__

def register():
    name = input('Enter your first name :')
    phonenumber = input('Enter your Phone number :')
    address = input('Enter your Address (The province where you live ):')
    mail = input('Enter your Email/Gmail :')
    password = b64encode(encrypt(key, input('Enter your Password :'))).decode("utf-8")
    

    user = person(name, phonenumber, address, mail, password)

    # object to JSON
    person_json = json.dumps(user, cls=person_data)

    # Json parse
    person_dict = json.loads(person_json)

##########
    def write_json(data, filename='users.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('users.json') as json_file:
        data = json.load(json_file)
        temp = data['users']

        # python object to be appended
        y = person_dict
        
        # appending data to emp_details
        temp.append(y)

    write_json(data)
##########

def logIn():
    userName = input('Enter your username :')
    pasS = input('Enter your pass :')

    f = open('users.json', 'r')
    data = json.loads(f.read())

    for i in data["users"]:
        password = decrypt(key, b64decode(i['Password'])).decode("utf-8")
        if userName == i["Name"] and pasS == password:
            print('Your entry was succesful :)')
            displayProducts(i["Name"])
            break
    f.close()

class product:
    def __init__(self,Code,firstName):
        self.Code = Code
        self . firstName = firstName

class product_data(JSONEncoder):
    def default(self, o):
        return o.__dict__

def pay(yourName) :
    f = open('users.json', 'r')
    data = json.loads(f.read())
    for item in data["users"] :
        if yourName == item["Name"] :
            terminus = item["Address"]
            print(f"Your terminus : {terminus} ")
    f.close()

    f2 = open('orders.json' , 'r')
    data = json.loads(f2.read())
    a=[]
    total = 0

    for i in data["orders"] :
        if yourName == i["firstName"] :
            x = i["Code"]
            a.append(x)
    print(f"registered product code : {a}")
    f2.close()

    f3 = open('product.json' ,'r')
    data = json.loads(f3.read())
    products_price = 0
    for i in a:
        for j in data["Products"] :
            if int(i) == int(j["code"]) :
                products_price += int(j["price"])
                break
    print(f"your products price : {products_price}")
    f3.close()

    def write_json(data, filename='product.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('product.json') as json_file:
        data = json.load(json_file)
        temp = data['Products']
        for i in a:
            for j in temp :
                if int(i) == int(j["code"]) :
                    j["numberInstock"] = j["numberInstock"] - 1
                    break
    write_json(data)

    file2 = open('Provinces.json' ,'r')
    data =json.loads(file2.read())
    for i in data["Provinces"] :
        if i["name"] == terminus :
            Price2 = i["cost"]
            print(f"your postage : {Price2}")
    file2.close()

    total = products_price + Price2
    print(f"your total : {total}")
    print(f"Payment was succesfully...!")
    deletOrders(yourName)


def cansel(yourName):
    deletOrders(yourName)

def deletOrders(yourName):
    f = open('orders.json', 'r')
    data = json.loads(f.read())
    a = []
    for i in data["orders"]:
        if  i["firstName"] == yourName:
            continue
        else:
            a.append(i)
    f.close()
    
    product_json = json.dumps(data, cls=product_data)
    product_dict = json.loads(product_json)

    def write_json(data, filename='orders.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('orders.json') as json_file:
        data = json.load(json_file)
        temp = data['orders']
        temp.clear()
    for i in a:
        temp.append(i)
    write_json(data)

def displayProducts(yourName):
    f5 = open('product.json', 'r')
    data2 = json.loads(f5.read())
    for i in data2['Products']:
        print(i)

    exist = False

    code = input("Enter your requset (1.Enter the product code  2.Enter 'cansel'  3. Enter 'payment') :")
    if code == 'payment' :
        pay(yourName)
    elif code == 'cansel' :
        cansel(yourName)
    else :
        for i in data2['Products']:
            if code == str(i["code"]):
                exist = True
                break
        f5.close()
        if (exist == True):
            order = product(code , yourName)
            product_json = json.dumps(order, cls=product_data)

            product_dict = json.loads(product_json)

            def write_json(data, filename='orders.json'):
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)

            with open('orders.json') as json_file:
                data = json.load(json_file)
                temp = data['orders']

                y = product_dict
            
                temp.append(y)

                write_json(data)

class admin:
    def __init__(self , model , numberInstock , price , code) :
        self . model = model
        self . numberInstock = numberInstock
        self . price = price
        self . code = code

class admin_data(JSONEncoder):
    def default(self, o):
        return o.__dict__

def delete():
    yourResponse = input('Which Product do you want to clean ?(Code)')
    f = open('product.json', 'r')
    data = json.loads(f.read())
    a = []
    for i in data["Products"]:
        if  i["code"] == yourResponse :
            continue
        else:
            a.append(i)
    f.close()
    
    admin_json = json.dumps(data, cls=admin_data)
    admin_dict = json.loads(admin_json)

    def write_json(data, filename='product.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('product.json') as json_file:
        data = json.load(json_file)
        temp = data['Products']
        temp.clear()
    for i in a:
        temp.append(i)
    write_json(data)

def edit():
    your_response = input('Which product do you want to edit ? (Code)')
    f = open('product.json', 'r')
    data = json.loads(f.read())
    a = []
    for i in data["Products"]:
        if  i["code"] == your_response :
            continue
        else:
            a.append(i)
    f.close()
    
    admin_json = json.dumps(data, cls=admin_data)
    admin_dict = json.loads(admin_json)

    x = input('Enter Product that includes model , numberInStock , price ,code : ')
    def write_json(data, filename='product.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('product.json') as json_file:
        data = json.load(json_file)
        temp = data['Products']
        temp.clear()
        temp . append(x)
    for i in a:
        temp.append(i)
    write_json(data)
    
def newProcudt():
    Model = input('Enter the product model :')
    NumberInStock = int(input('Enter the number in stock :'))
    Price = int(input('Enter the product price :'))
    Code = input('Enter the product code :')

    products = admin(Model , NumberInStock , Price , Code)

    # object to JSON
    admin_json = json.dumps(products, cls=admin_data)

    # Json parse
    admin_dict = json.loads(admin_json)

    def write_json(data,filename='product.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    with open('product.json') as json_file:
        data = json.load(json_file)
        temp = data['Products']

        # python object to be appended
        y = admin_dict
        
        # appending data to emp_details
        temp.append(y)

    write_json(data)

def order_list():
    f = open('orders.json','r')
    for item in f :
        print(item)
    f.close()

def product_list():
    f = open('product.json' ,'r')
    for i in f :
        print(i)
    f.close()

def AdminLogin():
    myEmail = 'paria.heravi@gmail.com'
    myPassword = 'par#@agh77'
    warehouseAddress = 'tehran'
    email = input('Enter your email :')
    PassWord = input('Enter your password :')
    address = input('Enter the warehouse address :')
    if email == myEmail and PassWord == myPassword and address == warehouseAddress :
        print('You are logged in as an admin :)')
        x = input('Do You want to create a new product , see a list of orders ,see a list of Products, edit the product or clean product ?(newProduct\orderList\productList\edit\delete) ')
        if x == 'newProduct':
            newProcudt()
        elif x == 'orderList' :
            order_list()
        elif x == 'productList' :
            product_list()
        elif x =='edit' :
            edit()
        elif x == 'delete':
            delete()
    else:
        print('Invalid !')

print("------menu------")
print("Enter the Character 'R' for Register :")
print("Enter the character 'L' for log in and Order :")
print("Enter the character 'A' for Admin :")
request = input("Enter your request :")
if request == 'R'or request == 'r':
    register()
elif request == 'L' or request == 'l':
    logIn()
elif request == 'A' or request == 'a':
    AdminLogin()
else: 
    print('Your request is not Valid! try again :')
