import tkinter as tk
from tkinter import *
import time
import random


class pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        # placeholder image
        self.walking_right = [tk.PhotoImage(file='assets/pomright.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.walking_left = [tk.PhotoImage(file='assets/pomleft.gif', format='gif -index %i' % (i)) for i in range(4)]
        self.pomsit= [tk.PhotoImage(file='assets/pomsit.gif', format='gif -index %i' % (i)) for i in range(4)]

        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        # self.window.wm_attributes('-topmost', 1)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'green')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='green')
        
        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = 0
        self.y = self.window.winfo_screenheight()-78
        self.window.geometry('64x64+{x}+0'.format(x=str(self.x)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        #bed

        #clicks and drags
        self.is_sitting = False
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window.bind("<ButtonPress-1>", self.OnClick)
        self.window.bind("<ButtonRelease-1>", self.OnRelease)
        self.window.bind("<Motion>", self.OnMouseMove)
        self.window.bind("<Double-Button-1>", self.OnDoubleClick)
        self.window.bind("<Escape>", self.on_esc_pressed)
        
        self.label.config(cursor="hand2")

        #behaviors
        self.direction = True
        self.behavior = 0
        self.behaviorcounter = 100
        self.counter = 0

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.update)
        self.window.mainloop()

    def on_esc_pressed(self, event):
        if self.is_dragging:
            self.window.destroy()

    def OnClick(self, event):
        print("press")
        self.behavior = 4
        self.is_dragging = True
        self.drag_start_x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        self.drag_start_y = self.window.winfo_pointery() - self.window.winfo_rooty()
    
    def OnRelease(self, event):
        if self.behavior != 5:
            self.is_dragging = False
            print("release " + str(self.is_dragging))
            self.behavior = 2
            self.behaviorcounter = 200
    
    def OnDoubleClick(self, event):
        self.behavior = 5
        self.is_sitting = not self.is_sitting  # Reset dragging status
        if(not self.is_sitting):
            self.behavior = 2
            self.counter = 0
            self.behaviorcounter = 150
        print("double click " + str(self.is_sitting))

    def OnMouseMove(self, event):
        if self.is_dragging:
            cursor_x = self.window.winfo_pointerx()
            cursor_y = self.window.winfo_pointery()
            self.x = cursor_x - self.drag_start_x
            self.y = cursor_y - self.drag_start_y

            self.window.geometry('+{x}+{y}'.format(x=self.x, y=self.y))
            
    def bounce(self):
        self.window.wm_attributes('-topmost', 1)
        if self.x + 64 > self.window.winfo_screenwidth() and self.behavior == 0:
            print("bounce1")
            self.behavior = 1
        elif self.x < 0 and self.behavior == 1:
            print("bounce2")
            self.behavior = 0
        
    def switchbehavior(self):
        self.behavior = random.randrange(0,3,1)

    def switchbehaviorcounter(self):
        self.behaviorcounter = random.randrange(150,200,5)

    def update(self):
        
        self.bounce()
        # move and switch directions on screen edge    
        # 0 -> walk right
        # 1 -> walk left
        # 2 -> sit
        # 4 -> mouse drag
        # 5 -> double click
        if self.behavior == 0:
            self.x +=3
            self.img = self.walking_right[self.frame_index]
        elif self.behavior == 1:
            self.x -=3
            self.img = self.walking_left[self.frame_index]
        elif self.behavior == 2: 
            self.img = self.pomsit[self.frame_index]
        elif self.behavior == 4:
            self.img = self.pomsit[self.frame_index] #drag
        elif self.behavior == 5:
            self.img = self.pomsit[self.frame_index] #forced sit
        # print('behavior ' + str(self.behavior))
        
        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.05:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 4
                
            
        # create the window
        self.window.geometry('64x64+{x}+{y}'.format(x=str(self.x), y=str(self.y)))

        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()

        
        if(self.counter == self.behaviorcounter and self.behavior != 4 and self.behavior != 5):
            self.switchbehaviorcounter()
            print(str(self.behaviorcounter))
            self.switchbehavior()
            print("switched to " + str(self.behavior))
            self.counter = 0

        # call update after 10ms
        self.window.after(10, self.update)
        self.counter +=1


pet()