import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
import http.cookiejar as cookielib
from requests.cookies import RequestsCookieJar
import tkinter
import rsa
from binascii import b2a_hex, a2b_hex
import time
import gc
with open('public.pem') as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)

with open('private.pem') as privatefile:
    p = privatefile.read()
    prikey = rsa.PrivateKey.load_pkcs1(p)

class rsacrypt():
    def __init__(self, pubkey, prikey):
        self.pubkey = pubkey
        self.prikey = prikey
    def encrypt(self, text):
        self.ciphertext = rsa.encrypt(text.encode(), self.pubkey)
        return b2a_hex(self.ciphertext)
    def decrypt(self, text):
        decrypt_text = rsa.decrypt(a2b_hex(text), prikey)
        return decrypt_text

def save():
    f = open('加密密码文件，请勿删除.txt', 'w')
    studyNum = text1.get().replace('\n', '')
    password = text2.get().replace('\n', '')
    f.write(studyNum + '\n')
    # 密码加密写入文件
    rs_obj = rsacrypt(pubkey, prikey)
    encry_password = rs_obj.encrypt(password)
    del rs_obj
    f.write(encry_password.decode())
    f.close()
def on_click():
    rs_obj = rsacrypt(pubkey, prikey)
    f = open('加密密码文件，请勿删除.txt', 'r')
    a = f.readlines()
    f.close()
    cookies=login(a[0],rs_obj.decrypt(a[1]).decode()).cookies.get_dict()
    from selenium import webdriver
    global driver
    driver=webdriver.Chrome()
    driver.get('http://jwc.swjtu.edu.cn/vatuu/UserFramework')
    driver.maximize_window()
    for name,value in cookies.items():
        driver.add_cookie({'name':name,'value':value})
    driver.get('http://jwc.swjtu.edu.cn/vatuu/UserFramework')


def admin_not_exist():
    global root1
    root1=tkinter.Tk()
    root1.geometry("+650+245")
    root1.wm_attributes('-topmost', True)
    label=tkinter.Label(root1)
    label['text'] = '登录错误，用户不存在。'
    label.grid(row=1,column=0)
    b1=tkinter.Button(root1, text='返回', width=3, height=1, command=root1.destroy)
    b1.grid(row=2,column=0)
def password_worng():
    global root2
    root2=tkinter.Tk()
    root2.geometry("+650+245")
    root2.wm_attributes('-topmost', True)
    label=tkinter.Label(root2)
    label['text'] = '密码错误！'
    label.grid(row=1,column=0)
    b1=tkinter.Button(root2, text='返回', width=3, height=1, command=root2.destroy)
    b1.grid(row=2,column=0)
def gui():
    global text1,text2,text3,top
    f = open('加密密码文件，请勿删除.txt', 'r')
    a = f.readlines()
    f.close()
    studyNum=a[0]
    top=tkinter.Tk(className='教务辅助登录')
    top.geometry('480x150')
    top.wm_attributes('-topmost', True)
    top.geometry("+650+245")
    label1 = tkinter.Label(top)
    label1['text'] = '教务辅助登录系统：'
    label1.grid(row=0, column=0)
    label2 = tkinter.Label(top)
    label2['text'] = '首次使用输完账号'
    label2.grid(row=0, column=1)
    label2 = tkinter.Label(top)
    label2['text'] = '密码后请务必先点保存后再点登陆！'
    label2.grid(row=0, column=2)
    label3 = tkinter.Label(top)
    label3['text'] = '学号：'
    label3.grid(row=2, column=0)
    text1 = tkinter.StringVar()
    text1.set(studyNum)
    entry = tkinter.Entry(top,width=13)
    entry['textvariable'] = text1
    entry.grid(row=2, column=1)

    label4 = tkinter.Label(top)
    label4['text'] = '密码：'
    label4.grid(row=3, column=0)
    text2 = tkinter.StringVar()
    text2.set('**********')
    entry = tkinter.Entry(top,width=13,show='*')
    entry['textvariable'] = text2
    entry.grid(row=3, column=1)

    button = tkinter.Button(top, width=13, height=1)
    button['text'] = '保存初始账号密码'
    button['command'] = save
    button.grid(row=3, column=2)

    button = tkinter.Button(top,width=13, height=1)
    button['text'] = '登录'
    button['command'] = on_click
    button.grid(row=5, column=1)

    top.mainloop()

def bdapi_get_code(name):
    from aip import AipOcr
    APP_ID = '16920343' #填你自己的ID
    API_KEY = 'qQhlU0e1GHfjnIgGygTduhk6'#填你自己的APIKEY
    SECRET_KEY = '7qxUVgLYd16wRX0MgscsaLnQfrhXFk37'#填你自己的SECRETKEY
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    image = get_file_content(name)
    client.basicAccurate(image)
    options = {}
    options["language_type"] = "ENG"
    global a
    a=client.basicAccurate(image,options)
    if a['words_result']!=[]:
        return a['words_result'][0]['words'].replace(' ','')
    else:
        return []

def login(username,password):
    s=requests.session()
    s.get('http://jwc.swjtu.edu.cn/service/login.html')
    headers={
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'jwc.swjtu.edu.cn',
    'Origin': 'http://jwc.swjtu.edu.cn',
    'Referer': 'http://jwc.swjtu.edu.cn/service/login.html',
    'X-Requested-With': 'XMLHttpRequest'
    }
    postData={
    'username': username,
    'password': password,
    'url': 'http://jwc.swjtu.edu.cn/index.html',
    'returnUrl': '',
    'area': ''
    }
    while True:
        res=s.get('http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG?test=1564811998471')
        image=Image.open(BytesIO(res.content))
        image.save('temp.png')
        #image.show()
        code=bdapi_get_code('temp.png')
        print(code)
        if code:
            postData['ranstring']=code
        else:
            continue
        postUrl='http://jwc.swjtu.edu.cn/vatuu/UserLoginAction'
        responseRes = s.post(postUrl, data = postData, headers = headers)
        print(responseRes.text)
        s.post('http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction')
        if "验证码输入不正确" in responseRes.text:
            continue
        if "登录失败，密码输入不正确" in responseRes.text:
            password_worng()
            raise Exception
        if "登录错误，用户不存在" in responseRes.text:
            admin_not_exist()
            raise Exception
        if "登录成功" in responseRes.text:
            print('Suceess')
            top.destroy()
            return s

gui()
# on_click()

