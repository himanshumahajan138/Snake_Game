###########################################################################################################################################
# This Snake Game Is Made By Himanshu Mahajan
# Made using Pyhton With Tkinter Support
# In This Game as Snake Eat Food it Gets Larger 
###########################################################################################################################################

from tkinter import *
from tkinter.messagebox import showerror
from random import choice
from winsound import Beep
import sys
from os import path
from PIL import Image,ImageTk
###########################################################################################################################################
class Snake:
	def __init__ (self):
		self.snake_pos = [(100,100),(80,100),(60,100)]
		self.direction = "Right"
		self.speed = 100
		self.win = Tk()
		self.screen_height,self.screen_width=self.win.winfo_screenheight(),self.win.winfo_screenwidth()
		self.win.geometry(f"{self.screen_width}x{self.screen_height}")
		self.win.state("zoomed")
		self.win.title("Himanshu Snake Game ")
		self.win.attributes("-alpha",0.98)
		self.canvas = Canvas(self.win,bg="black",highlightthickness=0,cursor="none")
		self.canvas.pack(fill=BOTH,expand=True)
		self.win.bind("<Return>",lambda e : self.start(e))
		self.boundary()
		self.images()
		self.canvas.create_image(self.width//2,self.height//2,image=self.back_img,tag="background")
		self.canvas.create_text(self.screen_width//2,self.screen_height//2,text="START",fill="red",font="gthoic 50 bold",tag="start")
		self.canvas.create_text(self.screen_width//2+20,30,text="Snake Game By Himanshu Mahajan",fill="white",font="gthoic 20 bold")
		self.win.iconbitmap(self.path("icon_snake.ico"))
		self.win.mainloop()
	def path(self,filename):
		if hasattr(sys,"_MEIPASS"):
			return f"{path.join(sys._MEIPASS,filename)}"
		else:
			return f"{filename}"
	def boundary(self):
		try:
			self.width = self.screen_width-self.screen_width%20 if self.screen_width%20!=0 else self.screen_width
			self.height = self.screen_height-self.screen_height%20 if self.screen_height%20!=0 else self.screen_height
			self.canvas.create_rectangle(20,60,self.width-20,self.height-60,outline="red",tag="rect")
		except:
			None
	def images(self):
		try:
			self.head_img = ImageTk.PhotoImage(Image.open(self.path("head.png")).resize((25,25)))
			self.body_img = ImageTk.PhotoImage(Image.open(self.path("body.png")).resize((25,25)))
			self.food_img = ImageTk.PhotoImage(Image.open(self.path("food.png")).resize((25,25)))
			self.back_img = ImageTk.PhotoImage(Image.open(self.path("back.png")).resize((self.width-42,self.height-122)))
		except:
			None
	def creating_snake_body(self):
		try:
			h = 0
			for x,y in self.snake_pos:
				if h == 0:
					self.canvas.create_image(x,y,image=self.head_img,tag="snake")
					h+=1
				else:
					self.canvas.create_image(x,y,image=self.body_img,tag="snake")
			self.placing_food()
		except:
			None
	def placing_food(self):
		try:
			l=[]
			for i in range(40,self.width-40):
				for j in range(80,self.height-80):
					if i%20==0  and j%20==0:
						l.append((i,j))
			lw,lh = choice(l)
			self.canvas.create_image(lw,lh,image=self.food_img,tag="food")
		except:
			None
	def snake_direction(self,event=None):
		try:
			all_directions = ["Right","d","Left","a","Up","w","Down","s"]
			opposite_directions = [{"Right","Left"},{"Up","Down"},{"Up","s"},{"Right","a"},{"Left","d"},{"Down","w"}]
			if (event == None or event.keysym not in all_directions or 
				{self.direction,event.keysym} in opposite_directions):
				None
			else:
				self.direction = event.keysym
			self.food_eaten()
			self.head_x,self.head_y = self.snake_pos[0]
			if self.direction in ["Right","d"]:
				self.new_head_pos,self.direction = (self.head_x+20 ,self.head_y),"Right"
			if self.direction in ["Left","a"]:
				self.new_head_pos,self.direction = (self.head_x-20 ,self.head_y),"Left"
			if self.direction in ["Up","w"]:
				self.new_head_pos,self.direction = (self.head_x ,self.head_y-20),"Up"
			if self.direction in ["Down","s"]:
				self.new_head_pos,self.direction = (self.head_x ,self.head_y+20),"Down"
			self.snake_pos=[self.new_head_pos]+self.snake_pos[:-1]
			for item,pos in zip(self.canvas.find_withtag("snake"),self.snake_pos):
				self.canvas.coords(item,pos)
		except:
			None
	def move_snake(self):
		try:
			self.food_eaten()
			self.snake_direction()
			if self.collision():
				return False
			self.win.after(self.speed,self.move_snake)

		except:
			None
	def food_eaten(self):
		try:
			if [*self.snake_pos[0]] == self.canvas.coords("food"):
				Beep(600,50)
				self.score+=1
				self.canvas.delete("food")
				self.canvas.itemconfig("score",text=f"SCORE : {self.score}")
				self.snake_pos.append(self.snake_pos[:-1])
				x,y=[*self.snake_pos[-1]][1]
				self.canvas.create_image(int(x),int(y),image=self.body_img,tag="snake")
				if self.score%5==0:
					self.speed-=5
				self.placing_food()
		except:
			None
	def collision(self):
		try:
			if (self.canvas.coords("snake")[0] in (self.canvas.coords("rect")[0],self.canvas.coords("rect")[2])
				or self.canvas.coords("snake")[1] in (self.canvas.coords("rect")[1],self.canvas.coords("rect")[3])or
				tuple(self.canvas.coords("snake")) in self.snake_pos[1:]):
				self.canvas.create_text(self.width//2,self.height//2,text=f"SCORE : {self.score} \nGame Over \nPlay Again ? \nPress Enter ",
					fill="red",font="Arial 50 bold",tag="over")
				self.win.unbind_all("<Key>")
				self.win.bind_all("<Key>",self.restart)
				Beep(200,200)
				return True
			else:
				return False
		except:
			None
	def restart(self,event):
		try:
			if event.keysym == "Return":
				self.win.unbind_all("<Key>")
				self.canvas.destroy()
				self.win.destroy()
				self.__init__()
			else:
				self.win.destroy()
		except:
			None
	def start(self,event):
		try:
			self.win.unbind("<Return>")
			self.canvas.delete("start")
			self.score = 0
			self.canvas.create_text(80,30,text=f"SCORE : {self.score}",fill="gray99",font="gthoic 15 bold",tag="score")
			self.creating_snake_body()
			self.win.bind_all("<Key>",lambda e:self.snake_direction(e))
			self.move_snake()
		except:
			None
if __name__ == "__main__":
	try:
		start = Snake()
	except:
		showerror("Himanshu Snake Game","Error Occured")