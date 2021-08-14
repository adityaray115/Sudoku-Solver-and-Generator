from tkinter import *
from tkinter import messagebox
import numpy as np
import random
from numpy.random.mtrand import shuffle
import mysql.connector

root=Tk()
root.title('SUDOKU SOLVER')
'''rootwidth=1150
rootheight=690
root.minsize(rootwidth,rootheight)
root.maxsize(rootwidth,rootheight)'''
root.geometry('1150x690')
root.resizable(width=False,height=False)
counter=1

#variables
counter=1
name=''
d=''
tot_time='0:0:0'
fillgridcheck=0
autosolve=0
endgame=0
numberlist=list(range(1,10))
numlist=['1','2','3','4','5','6','7','8','9','']

#--------------------------------TIMER-------------------------
hour = minute = second = 0
h = m = s = 0
def counter_label(timer):
    #global timer
    hour = minute = second = 0
    h = m = s = 0
    def count():
        global s,m,h
        global second,minute,hour
        global fillgridcheck
        global autosolve
        global endgame
        global tot_time
        second = second + 1
        if second < 10:
            s = 1
        if minute < 10:
            m = 1
        if hour < 10:
            h = 1
        if second > 59:
            minute = minute + 1
            second = 0
            if minute > 59:
                hour = hour +1
                second = 0
                minute = 0
                if hour > 23:
                    fillgridcheck = 1
                    messagebox.showinfo('Message','One day completed')
        if fillgridcheck==1:
            resetgame['state']=DISABLED
            checkgame['state']=DISABLED
            solvegame['state']=DISABLED
            hour = minute = second = 0
            fillgridcheck=0
            if endgame==1:
                endgame = 0
                hour = minute = second = 0
                return
            if autosolve==1:
                tot_time = 'AUTO SOLVE'
                autosolve = 0
            messagebox.showinfo('Message','Game completed.')
            return
        if(s==1 and m==1 and h==1):
            timer.config(text = '0'+str(hour)+':'+'0'+str(minute)+':'+'0'+str(second))
            tot_time = '0'+str(hour)+':'+'0'+str(minute)+':'+'0'+str(second)
            h= m = s = 0
        elif(s==0 and m==1 and h==1):
            timer.config(text = '0'+str(hour)+':'+'0'+str(minute)+':'+str(second))
            tot_time = '0'+str(hour)+':'+'0'+str(minute)+':'+str(second)
            h = m = 0
        elif(s==1 and m==0 and h==1):
            timer.config(text = '0'+str(hour)+':'+str(minute)+':'+'0'+str(second))
            tot_time = '0'+str(hour)+':'+str(minute)+':'+'0'+str(second)
            h = s = 0
        elif(s==0 and m==0 and h==1):
            timer.config(text = '0'+str(hour)+':'+str(minute)+':'+str(second))
            tot_time = '0'+str(hour)+':'+str(minute)+':'+str(second)
            h = 0
        elif(s==1 and m==1 and h==0):
            timer.config(text = str(hour)+':'+'0'+str(minute)+':'+'0'+str(second))
            tot_time = str(hour)+':'+'0'+str(minute)+':'+'0'+str(second)
            m = s = 0
        elif(s==0 and m==1 and h==0):
            timer.config(text = str(hour)+':'+'0'+str(minute)+':'+str(second))
            tot_time = str(hour)+':'+'0'+str(minute)+':'+str(second)
            m =0
        elif(s==1 and m==0 and h==0):
            timer.config(text = str(hour)+':'+str(minute)+':'+'0'+str(second))
            tot_time = str(hour)+':'+str(minute)+':'+'0'+str(second)
            s = 0
        else:
            timer.config(text = str(hour)+':'+str(minute)+':'+str(second))
            tot_time = str(hour)+':'+str(minute)+':'+str(second)
        timer.after(1000,count)
    count()
#-------------------------------------------------------------------------------

def valid(x,y,n):
    for i in range(0,9):
        if entry[x][i].get()==str(n):
            return False
    for i in range(0,9):
        if entry[i][y].get()==str(n):
            return False
    for i in range(x-x%3,x-x%3+3):
        for j in range(y-y%3,y-y%3+3):
            if entry[i][j].get()==str(n):
                return False
    return True

def valid2(x,y,n):
    for i in range(0,9):
        if entry[x][i].get()==str(n) and y!=i:
            return False
    for i in range(0,9):
        if entry[i][y].get()==str(n) and x!=i:
            return False
    for i in range(x-x%3,x-x%3+3):
        for j in range(y-y%3,y-y%3+3):
            if entry[i][j].get()==str(n) and x!=i and y!=j:
                return False
    return True

def check_fill():
    for i in range(9):
        for j in range(9):
            if(entry[i][j].get()==''):
                return False
    return True

numberlist=list(range(1,10))

def fillGrid():
    #   global counter
  #Find next empty cell
  for i in range(0,81):
    row=i//9
    col=i%9
    if entry[row][col].get()=='':
    #   shuffle(numberlist)      
      for value in numberlist:
        value=str(value)
        #Check that this value has not already be used on this row
        if not value in (entry[row][0].get(),entry[row][1].get(),entry[row][2].get(),entry[row][3].get(),entry[row][4].get(),entry[row][5].get(),entry[row][6].get(),entry[row][7].get(),entry[row][8].get()):
            if not value in (entry[0][col].get(),entry[1][col].get(),entry[2][col].get(),entry[3][col].get(),entry[4][col].get(),entry[5][col].get(),entry[6][col].get(),entry[7][col].get(),entry[8][col].get()):
                l=[]
                for i in range(row-row%3,row-row%3+3):
                    for j in range(col-col%3,col-col%3+3):
                        l.append(entry[i][j].get())
                #Check that this value has not already be used on this 3x3 square
                if not value in l:
                    entry[row][col].delete(0,END)
                    entry[row][col].insert(0,str(value))
                    if check_fill():
                        return True
                    else:
                        if fillGrid():
                            return True
      break
  entry[row][col].delete(0,END)        
  entry[row][col].insert(0,str(''))

def solveGrid():
  global counter
  #Find next empty cell
  for i in range(0,81):
    row=i//9
    col=i%9
    if entry[row][col].get()=='':
      for value in numberlist:
        value=str(value)
        #Check that this value has not already be used on this row
        if not value in (entry[row][0].get(),entry[row][1].get(),entry[row][2].get(),entry[row][3].get(),entry[row][4].get(),entry[row][5].get(),entry[row][6].get(),entry[row][7].get(),entry[row][8].get()):
            if not value in (entry[0][col].get(),entry[1][col].get(),entry[2][col].get(),entry[3][col].get(),entry[4][col].get(),entry[5][col].get(),entry[6][col].get(),entry[7][col].get(),entry[8][col].get()):
                #Identify which of the 9 squares we are working on
                square=[]
                l=[]
                for i in range(row-row%3,row-row%3+3):
                    for j in range(col-col%3,col-col%3+3):
                        l.append(entry[i][j].get())
                #Check that this value has not already be used on this 3x3 square
                if not value in l:
                    entry[row][col].delete(0,END)
                    entry[row][col].insert(0,str(value))
                    if check_fill():
                        counter+=1
                        break
                        return True
                    else:
                        if fillGrid():
                            return True
            
      break
  entry[row][col].delete(0,END)        
  entry[row][col].insert(0,str(''))

def newg():
    global timer
    global counter
    if entryname.get()=='' and diff.get()=='SELECT':
        messagebox.showerror('Error','Enter name and select difficulty level.')
    elif entryname.get()=='':
        messagebox.showerror('Error','Name field should not be empty.')
    elif diff.get()=='SELECT':
        messagebox.showerror('Error','Difficulty level not selected.')
    else:
        global name 
        name=entryname.get()
        global fillgridcheck
        fillgridcheck=0
        resetgrid(entry)
        newbuttonpressed()
        fillGrid()
        for row in range(9):
            for col in range(9):
                entry[row][col].configure(state='readonly')
        count=0
        if diff.get()=='EASY':count=40
        elif diff.get()=='NORMAL':count=50
        elif diff.get()=='HARD':count=60
        counter=1
        while count>0:
            # Select a random cell that is not already empty
            row = random.randint(0,8)
            col = random.randint(0,8)
            while entry[row][col].get()=='':
                row = random.randint(0,8)
                col = random.randint(0,8)
            #Remember its cell value in case we need to put it back  
            entry[row][col].configure(state='normal')
            backup = entry[row][col].get()
            entry[row][col].delete(0,END)
            
            #Take a full copy of the grid
            gridcopy=[]
            l=[]
            for i in range(0,9):
                l=[]
                for j in range(0,9):
                    l.append(entry[i][j].get())
                gridcopy.append(l)
            #Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
            counter=0
            solveGrid()   
            #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
            if counter!=1:
                entry[row][col].delete(0,END)
                entry[row][col].insert(0,str(backup))
                #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
                count -= 1
            for i in range(0,9):
                for j in range(0,9):
                    entry[i][j].delete(0,END)
                    entry[i][j].insert(0,str(gridcopy[i][j]))
        counter_label(timer)        

def saveg():
    global name
    global tot_time
    global d
    d = diff.get()
    sud=mysql.connector.connect(host='localhost',username='root',passwd='')
    obj=sud.cursor()
    obj.execute('create database if not exists sudoku')
    obj.execute('use sudoku')
    obj.execute('create table if not exists sudoku(NAME varchar(30),TIME varchar(30),DIFFICULTY varchar(20))')
    sql='insert into sudoku values(%s,%s,%s);'
    var=(name,tot_time,d)
    obj.execute(sql,var)
    obj.execute('commit;')
    messagebox.showinfo('Saved','Your record has been saved.')

def solveg():
    global fillgridcheck,autosolve
    for row in range(9):
        for col in range(9):
            if entry[row][col].cget('state')=='normal':
                entry[row][col].delete(0,END)
                entry[row][col].insert(0,'')
    fillGrid()
    autosolve = 1
    fillgridcheck = 1

def checkg():
    global fillgridcheck
    for i in range(9):
        for j in range(9):
            num=entry[i][j].get()
            if(num not in numlist):
                messagebox.showerror('Error','Invalid entries are present.')
                return
            if(num==''):
                messagebox.showwarning('Warning','Empty spaces are present.')
                return
            for row in range(9):
                for col in range(9):
                    if not valid2(row,col,entry[row][col].get()):
                        messagebox.showerror('Error','Number is repeated')
                        return                   
    fillgridcheck=1

def resetg():
    messagebox.showwarning('Warning','Timer will not stop.')
    ans=messagebox.askyesno('Confirm','Are you sure you want to reset?')
    if ans==1:
        # resetgrid(entry)
        for row in range(9):
            for col in range(9):
                if entry[row][col].cget('state')=='normal':
                    entry[row][col].delete(0,END)
                    entry[row][col].insert(0,'')
    else:
        pass

def exitg():
    ex1=messagebox.askyesno('Warning','Any unsaved changes may be lost. Do you want to end the game?')
    if ex1==1:
        ex2=messagebox.askyesno('Close Game','Do you want to exit the application?')
        if ex2==1:
            root.destroy()
        else:
            global endgame
            global fillgridcheck
            fillgridcheck = 1
            endgame = 1
            exitbuttonpressed()
            resetgrid(entry)
            disname.configure(text=entryname.get())
            diffright2.configure(text='')
            timer.config(text='')
            username['state']=DISABLED
            time['state']=DISABLED
            diffright1['state']=DISABLED
    else:
        pass

def newbuttonpressed():
    messagebox.showinfo('Game','Lets Play.....'+entryname.get())
    disname.configure(text=entryname.get())
    diffright2.configure(text=diff.get())
    entryname.delete(0,END)
    entryname['state']=DISABLED
    diffselect['state']=DISABLED
    namelabel['state']=DISABLED
    difficulty['state']=DISABLED
    newgame['state']=DISABLED
    checkgame['state']=NORMAL
    solvegame['state']=NORMAL
    savegame['state']=NORMAL
    resetgame['state']=NORMAL
    exitgame['state']=NORMAL
    username['state']=NORMAL
    time['state']=NORMAL
    diffright1['state']=NORMAL

def exitbuttonpressed():
    entryname['state']=NORMAL
    entryname.configure(text='')
    diffselect['state']=NORMAL
    diff.set('SELECT')
    namelabel['state']=NORMAL
    difficulty['state']=NORMAL
    newgame['state']=NORMAL
    checkgame['state']=DISABLED
    solvegame['state']=DISABLED
    savegame['state']=DISABLED
    resetgame['state']=DISABLED
    exitgame['state']=DISABLED

def resetgrid(entry):
    for i in range(9):
        for j in range(9):
            entry[i][j].configure(state='normal')
            entry[i][j].delete(0,END)

#Main Frame
mainframe=Frame(root,bg='violet')
mainframe.pack(expand=True,fill='both')

#Title of the Application
titleframe=Frame(mainframe,bg='pink')
title=Label(titleframe,text='SUDOKU',font=('arial black',70,'bold','underline'),fg='purple',bg='pink')
title.pack()
titleframe.pack(anchor=N,fill='x')

#Interaction Area for User
leftframe=Frame(mainframe,bg='light blue',width=300)
namelabel=Label(leftframe,text='Enter Name:',bg='light blue',font=('Arial',15))
namelabel.place(x=5,y=20)
entryname=Entry(leftframe,width=15,font=('Arial',15),fg='red')
entryname.place(x=125,y=20)
difficulty=Label(leftframe,text='Difficulty:',bg='light blue',font=('Arial',15))
difficulty.place(x=5,y=60)
newgame=Button(leftframe,text='NEW GAME',bg='light green',font=('Arial',15,'bold'),command=newg,bd=5)
newgame.place(x=90,y=270)
checkgame=Button(leftframe,text='CHECK',bg='light green',font=('Arial',15,'bold'),command=checkg,bd=5)
checkgame.place(x=170,y=330)
solvegame=Button(leftframe,text='SOLVE',bg='light green',font=('Arial',15,'bold'),command=solveg,bd=5)
solvegame.place(x=50,y=330)
savegame=Button(leftframe,text='SAVE',bg='light green',font=('Arial',15,'bold'),command=saveg,bd=5)
savegame.place(x=50,y=390)
resetgame=Button(leftframe,text='RESET',bg='light green',font=('Arial',15,'bold'),command=resetg,bd=5)
resetgame.place(x=170,y=390)
exitgame=Button(leftframe,text='END GAME',bg='light green',font=('Arial',15,'bold'),command=exitg,bd=5)
exitgame.place(x=90,y=450)
diff=StringVar()
diff.set('SELECT')
diffselect=OptionMenu(leftframe,diff,'EASY','NORMAL','HARD')
diffselect.config(font=('Arial',10,'italic'),fg='red')
diffselect.place(x=100,y=60)
exitbuttonpressed()
leftframe.pack(side=LEFT,fill='y')

#Details display
rightframe=Frame(mainframe,bg='light blue',width=300)
username=Label(rightframe,text='Username:',bg='light blue',font=('Arial',15))
username.place(x=5,y=20)
disname=Label(rightframe,bg='light blue',font=('Arial',15),fg='red')
disname.place(x=105,y=20)
diffright1=Label(rightframe,text='Difficulty:',bg='light blue',font=('Arial',15))
diffright1.place(x=5,y=60)
diffright2=Label(rightframe,bg='light blue',font=('Arial',15),fg='red')
diffright2.place(x=90,y=60)
time=Label(rightframe,text='Time:',bg='light blue',font=('Arial',15))
time.place(x=5,y=100)
timer=Label(rightframe,bg='light blue',font=('Arial',15),fg='red')
timer.place(x=70,y=100)
username['state']=DISABLED
time['state']=DISABLED
diffright1['state']=DISABLED
rightframe.pack(side=RIGHT,fill='y')

#Play Area
canvas1 = Canvas(mainframe, width = 455, height = 455, bd=1)
canvas1.pack(pady=44)
canvas1.create_line(155, 0,155,500)
canvas1.create_line(305, 0,305,500)
canvas1.create_line(5, 155,500,155)
canvas1.create_line(5, 305,500,305)

entry=np.array([[Entry()]*9]*9)
x=30
y=30
for i in range(9):
    for j in range(9):
        entry[i][j] = Entry(canvas1,width=2,font=('arial balck',30),fg='red',justify='center')
        canvas1.create_window(x+i*50,y+j*50,window=entry[i][j])

root.mainloop()