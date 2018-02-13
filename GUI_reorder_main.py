# -*- coding: UTF-8 -*-

import time
import Tkinter
import tkMessageBox
import Produce_Read_Order_List
from Tkinter import *
import ImageTk
import Image
import random
# from Spring import Spring


class Experiment_Session:

    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.title("Haptic Experiment")
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.width = w
        self.height = h
        self.root.geometry("%dx%d" % (w, h))
        self.root.minsize(300, 240)

        self.user_name = ""
        self.user_gender = ""
        self.user_age = 0

        self.cmd = Produce_Read_Order_List.Produce_Read_Order_List()
        self.cmd.make_pairs()

        self.User_feel_FP = -1         # record the user's actual choice of haptic feeling
        self.global_times_counter = 0  # record the user's repeated times
        self.start = 0
        self.end = 0
        self.deltatime = 0
        self.startTrialNum = 0
        self.outputfile = None
        self.currentTrial = None
        self.SpacePressTime = 0
        self.EnterPressTime = 0
        self.user_choice = -1
        self.ask_last_num = 0
        self.write_info = ""
        self.show_info = ""

        self.TrialInfo = Tkinter.StringVar(value='')
        self.Answer = Tkinter.StringVar(value='')
        self.Question_text = Tkinter.StringVar(value='')

        # Bind the Space Key press to continue
        self.root.bind("<KeyPress>", self.SpaceContinue)
        self.root.focus_set()
        self.root.bind('<Return>', self.EnterPress)
        # self.spring = Spring()

        self.varNum = Tkinter.StringVar(value='')
        self.varName = Tkinter.StringVar(value='')
        self.varGender = Tkinter.StringVar(value='')
        self.varAge = Tkinter.StringVar(value='')

        top_entry_y = h/80
        self.labelNum = Tkinter.Label(self.root, text='User Num:')
        self.labelNum.place(x=w/80, y=top_entry_y, width=w/12, height=h/20)
        self.labelNum.config(font=("Courier", 15, "bold"))
        self.entryNum = Tkinter.Entry(self.root, textvariable=self.varNum)
        self.entryNum.place(x=w/80 + w/12, y=top_entry_y, width=w/18, height=h/20)

        self.LabelName = Tkinter.Label(self.root, text='Name:')
        self.LabelName.place(x=w/80 + w/12 + w/20, y=top_entry_y, width=w/12, height=h/20)
        self.LabelName.config(font=("Courier", 15, "bold"))
        self.entryName = Tkinter.Entry(self.root, textvariable=self.varName)
        self.entryName.place(x=w/80 + 2 * w/12 + w/20, y=top_entry_y, width=w/20, height=h/20)

        self.LabelGender = Tkinter.Label(self.root, text='Gender:')
        self.LabelGender.place(x=w/80 + 2 * w/12 + 2 * w/20, y=top_entry_y, width=w/12, height=h/20)
        self.LabelGender.config(font=("Courier", 15, "bold"))
        self.entryGender = Tkinter.Entry(self.root, width=80, textvariable=self.varGender)
        self.entryGender.place(x=w/80 + 3 * w/12 + 2 * w/20, y=top_entry_y, width=w/20, height=h/20)

        self.LabelAge = Tkinter.Label(self.root, text='Age:')
        self.LabelAge.place(x=w/80 + 3 * w/12 + 3 * w/20, y=top_entry_y, width=w/12, height=h/20)
        self.LabelAge.config(font=("Courier", 15, "bold"))
        self.entryAge = Tkinter.Entry(self.root, width=80, textvariable=self.varAge)
        self.entryAge.place(x=w/80 + 4 * w/12 + 3 * w/20, y=top_entry_y, width=w/20, height=h/20)

        self.LabelStartFromTrial = Tkinter.Label(self.root, text='Start Num:')
        self.LabelStartFromTrial.place(x=w/80 + 4 * w/12 + 4 * w/20, y=top_entry_y, width=w / 12, height=h / 20)
        self.LabelStartFromTrial.config(font=("Courier", 15, "bold"))
        self.entryStartFromTrial = Tkinter.Entry(self.root, width=80, textvariable=self.startTrialNum)
        self.entryStartFromTrial.place(x=w/80 + 5 * w/12 + 4 * w/20, y=top_entry_y, width=w / 20, height=h / 20)

        self.buttonOk = Tkinter.Button(self.root, text='Confirm', command=self.login)
        self.buttonOk.place(x=w/80 + 5 * w/12 + 6 * w/20, y=top_entry_y, width=w / 20, height=h / 20)
        self.buttonOk.config(font=("Courier", 12, "bold"))
        self.buttonCancel = Tkinter.Button(self.root, text='Cancel', command=self.cancel)
        self.buttonCancel.place(x=w/80 + 6 * w/12 + 6 * w/20, y=top_entry_y, width=w / 20, height=h / 20)
        self.buttonCancel.config(font=("Courier", 12, "bold"))

        self.Info_Header = Label(self.root, text="Times\tRecongition Load\tHandness\tForce Profile\tRepeated Times")
        self.Info_Header.config(font=("Courier", 12, "bold"))

        self.Info = Label(self.root, textvariable=self.TrialInfo)
        self.Info.config(font=("Courier", 12, "bold"))
        # self.Info.place_forget()

        # Set up and place the images
        img_1 = Image.open('img/F01.jpg')
        img_1 = img_1.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_1 = ImageTk.PhotoImage(img_1)

        img_2 = Image.open('img/F02.jpg')
        img_2 = img_2.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_2 = ImageTk.PhotoImage(img_2)

        img_3 = Image.open('img/F03.jpg')
        img_3 = img_3.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_3 = ImageTk.PhotoImage(img_3)

        img_4 = Image.open('img/F04.jpg')
        img_4 = img_4.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_4 = ImageTk.PhotoImage(img_4)

        img_5 = Image.open('img/F05.jpg')
        img_5 = img_5.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_5 = ImageTk.PhotoImage(img_5)

        img_6 = Image.open('img/F06.jpg')
        img_6 = img_6.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_6 = ImageTk.PhotoImage(img_6)

        img_7 = Image.open('img/F07.jpg')
        img_7 = img_7.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_7 = ImageTk.PhotoImage(img_7)

        img_8 = Image.open('img/F08.jpg')
        img_8 = img_8.resize((w / 6, h / 6), Image.ANTIALIAS)
        img_8 = ImageTk.PhotoImage(img_8)

        col_x_1 = w / 80
        col_x_2 = 6 * w / 80 + w / 6
        col_x_3 = 12 * w / 80 + 2 * w / 6
        col_x_4 = 18 * w / 80 + 3 * w / 6

        label_level_1_y = top_entry_y + 2*h/20
        label_level_2_y = top_entry_y + 4 * h / 20 + h/6

        img_level_1_y = top_entry_y + 3*h/20
        img_level_2_y = top_entry_y + 5 * h / 20 + h/6

        self.FP1 = Label(self.root, text="Force Profile 1", fg='blue')
        self.FP1.place(x=col_x_1, y=label_level_1_y)
        self.FP1.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_1).place(x=w / 80, y=img_level_1_y)

        self.FP2 = Label(self.root, text="Force Profile 2", fg='blue')
        self.FP2.place(x=col_x_2, y=label_level_1_y)
        self.FP2.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_2).place(x= col_x_2, y=img_level_1_y)

        self.FP3 = Label(self.root, text="Force Profile 3", fg='blue')
        self.FP3.place(x=col_x_3, y=label_level_1_y)
        self.FP3.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_3).place(x=col_x_3, y=img_level_1_y)

        self.FP4 = Label(self.root, text="Force Profile 4", fg='blue')
        self.FP4.place(x=col_x_4, y=label_level_1_y)
        self.FP4.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_4).place(x=col_x_4, y=img_level_1_y)

        self.FP5 = Label(self.root, text="Force Profile 5", fg='blue')
        self.FP5.place(x=col_x_1, y= label_level_2_y)
        self.FP5.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_5).place(x=w / 80, y=img_level_2_y)

        self.FP6 = Label(self.root, text="Force Profile 6", fg='blue')
        self.FP6.place(x=col_x_2, y=label_level_2_y)
        self.FP6.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_6).place(x=col_x_2, y=img_level_2_y)

        self.FP7 = Label(self.root, text="Force Profile 7", fg='blue')
        self.FP7.place(x=col_x_3, y=label_level_2_y)
        self.FP7.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_7).place(x=col_x_3, y=img_level_2_y)

        self.FP8 = Label(self.root, text="Force Profile 8", fg='blue')
        self.FP8.place(x=col_x_4, y=label_level_2_y)
        self.FP8.config(font=("Courier", 15, "bold"))
        Label(self.root, text="abc", image=img_8).place(x=col_x_4, y=img_level_2_y)

        # User haptic feel part and Quize part
        self.Question = Label(self.root, textvariable=self.Question_text, text="hello world")
        self.Question.place(x=5*w/16, y=2*h/3)
        self.Question.config(font=("Courier", 15, "bold"))

        self.User_Answer = Tkinter.Label(self.root, text='Answer: ', fg="blue")
        self.User_Answer.place(x=w/2 - w/10, y=7*h/8)
        self.User_Answer.config(font=("Courier", 15, "bold"))
        self.entry_Answer = Tkinter.Entry(self.root, width=80, textvariable=self.Answer)
        self.entry_Answer.place(x=w/2 - w/25, y=7*h/8, width=w / 12, height=h / 25)

        self.root.mainloop()

    def login(self):

        # Hide the label and entry from the panel
        self.labelNum.place_forget()
        self.entryNum.place_forget()
        self.LabelName.place_forget()
        self.entryName.place_forget()
        self.LabelGender.place_forget()
        self.entryGender.place_forget()
        self.LabelAge.place_forget()
        self.entryAge.place_forget()
        self.LabelStartFromTrial.place_forget()
        self.entryStartFromTrial.place_forget()
        self.buttonOk.place_forget()
        self.buttonCancel.place_forget()

        self.Info_Header.place(x=self.width / 80, y=self.height / 80, width=3 * self.width / 4, height=self.height / 25)
        self.Info_Header.config(bg="red")

        self.Info.place(x=self.width/80, y=self.height/80 + self.height/20, width=3 * self.width / 4, height=self.height/25)

        user_num = self.entryNum.get()

        if user_num == "":
            tkMessageBox.showinfo(title='Warning', message='Please complete number')
            return

        if user_num.isdigit() and 0 < int(user_num) < 17:

            self.user_name = self.entryName.get()
            self.user_age = self.entryAge.get()
            self.user_gender = self.entryGender.get()

            if self.user_name == "":
                tkMessageBox.showinfo(title='Warning', message='Please complete name')
                return
            if self.user_age == "":
                tkMessageBox.showinfo(title='Warning', message='Please complete age')
                return
            if self.user_gender == "":
                tkMessageBox.showinfo(title='Warning', message='Please complete gender')
                return
            if self.entryStartFromTrial.get() != "":
                self.startTrialNum = int(self.entryStartFromTrial.get())

            self.cmd.start_up(int(user_num))     # Produce commands by user number
            self.cmd.read_command()              # Read commands => commands
            # write the head information to the first line in the file
            self.outputfile = open("Records/User_" + str(user_num) + "_record.txt", "w")
            self.outputfile.write(
                "User_name,User_age,User_gender,Times,Recognition_Load,Handness,Force_Profile,Repeated_Times,Duration_Time,User_Choice,ask_last_num,user_RL_Choice \n")
            self.outputfile.close()

            # Re-open the output file again for later record useage
            self.outputfile = open("Records/User_" + str(user_num) + "_record.txt", "a")
        else:
            tkMessageBox.showinfo('Error', message='Please enter an valid number[0-16]')

    def cancel(self):
        self.varNum.set('')
        self.varAge.set('')
        self.varGender.set('')
        self.varName.set('')

    def SpaceContinue(self, event):
        if event.keysym == "space":

            if self.EnterPressTime % 2 != 1:
                tkMessageBox.showinfo('Warning', message='Press Enter before proceed')
                return

            print "Space Entered"
            if self.SpacePressTime % 2 == 0:
                self.start = int(round(time.time() * 1000))
                self.Question_text.set("Haptic TEST START")
                self.SpacePressTime += 1
                # self.spring = Spring()
                # self.spring.set_profile(currFP)
                # self.spring.run()
            else:
                # self.spring.terminate()
                self.deltatime = int(round(time.time() * 1000)) - self.start
                self.Question_text.set("Haptic TEST END")
                self.Question.after(1000, lambda: self.Question_text.set("Please select a haptic feeling you sensed"))
                self.SpacePressTime += 1

    def EnterPress(self, event):

        if self.EnterPressTime == 0:
            self.currentTrial = self.cmd.read_command_by_line()
            print self.currentTrial

            # Current/Total times
            self.write_info += self.user_name + "," + str(self.user_age) + "," + self.user_gender + ","

            if self.startTrialNum == 0:
                current_time = self.global_times_counter + 1
            else:
                current_time = self.global_times_counter + self.startTrialNum

            self.show_info += str(current_time) + "\t"
            self.write_info += str(current_time) + ","

            for i in range(len(self.currentTrial)):
                if i == 0:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 1:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 2:
                    self.show_info += self.currentTrial[i]+"\t\t"
                    self.write_info += self.currentTrial[i] + ","
                if i == 3:
                    self.show_info += self.currentTrial[i]
                    self.write_info += self.currentTrial[i] + ","

            self.TrialInfo.set(self.show_info)
            self.global_times_counter += 1
            self.show_info = ""

        elif self.EnterPressTime % 2 == 1:
            if len(self.entry_Answer.get()) == 0:
                tkMessageBox.showinfo('Warning', message='Enter your actual feel before proceed')
                return
            else:
                self.User_feel_FP = int(self.entry_Answer.get())
                tkMessageBox.showinfo(title='Notice', message='Haptic Choice Successfully Entered')
                self.Answer.set("")

                if self.currentTrial[0] == '1':
                    self.ask_last_num = random.randrange(1, 7)  # random number for quiz of last element
                    self.Question_text.set("Select the last " + str(self.ask_last_num) + " electronic element\n\n"
                                                                                        "1. Resistor  2. Capacitor\n"
                                                                                        "3. LED       4. Transistor\n"
                                                                                        "       5. Inductor  6.Integrated Circuit")
                else:
                    self.Question_text.set("No Question just Press [Enter] to Proceed")

        elif self.EnterPressTime % 2 == 0:

            if self.currentTrial[0] == '1':
                if len(self.entry_Answer.get()) == 0:
                    tkMessageBox.showinfo('Warning', message='Select the element you hear before proceed')
                    return
                else:
                    self.user_choice = self.entry_Answer.get()
            else:
                self.user_choice = -1

            tkMessageBox.showinfo('Notice', message='Question answered successfully')
            self.Question_text.set("")
            self.Answer.set("")

            self.write_info += str(self.User_feel_FP) + ","
            self.write_info += str(self.ask_last_num) + ","
            self.write_info += str(self.user_choice) + "\n"
            self.outputfile.write(self.write_info)
            self.write_info = ""

            # Begin the next trial
            self.currentTrial = self.cmd.read_command_by_line()
            print self.currentTrial

            # Current/Total times
            self.write_info += self.user_name + "," + str(self.user_age) + "," + self.user_gender + ","

            if self.startTrialNum == 0:
                current_time = self.global_times_counter + 1
            else:
                current_time = self.global_times_counter + self.startTrialNum

            self.show_info += str(current_time) + "\t\t"
            self.write_info += str(current_time) + ","

            for i in range(len(self.currentTrial)):
                if i == 0:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 1:
                    if self.currentTrial[i] == '1':
                        self.show_info += "True\t\t"
                        self.write_info += "1,"
                    else:
                        self.show_info += "False\t\t"
                        self.write_info += "0,"
                if i == 2:
                    self.show_info += self.currentTrial[i] + "\t\t"
                    self.write_info += self.currentTrial[i] + ","
                if i == 3:
                    self.show_info += self.currentTrial[i]
                    self.write_info += self.currentTrial[i] + ","

            self.TrialInfo.set(self.show_info)
            self.global_times_counter += 1
            self.show_info = ""

        self.EnterPressTime += 1


if __name__ == "__main__":
    Experiment_Session()
