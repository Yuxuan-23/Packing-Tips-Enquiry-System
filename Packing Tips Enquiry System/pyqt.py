from tkinter import *
import cv2
import os
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, scrolledtext
import search_new
import detection.detect


# import facial_recognition
# import database

class APP:
    def __init__(self):
        self.camera = None 
        self.root = Tk()
        self.root.title('Packing Tips Enquiry System')
        self.root.geometry('%dx%d' % (800, 500))
        self.yolo = detection.detect.YoloTest()
        self.createFirstPage()
        mainloop()



    def createFirstPage(self):
        self.page1 = Frame(self.root)
        self.page1.pack()
        Label(self.page1, text='Welcome to ues the Packing Tips Enquiry System\n\n\n\n', font=('Arial', 20, 'italic')).pack()

        self.wel_label = Label(self.page1)
        self.wel_label.pack()

        self.button11 = Button(self.page1, width=18, height=2, text="Detection", bg='red', font=("宋", 12),
                               relief='raise', command=self.createSecondPage)
        self.button11.pack(side=LEFT, padx=25, pady=80)

        self.button13 = Button(self.page1, width=18, height=2, text="Search", bg='white', font=("宋", 12),
                               relief='raise',
                               command=self.SearchObject)
        self.button13.pack(side=LEFT, padx=25, pady=80)
        self.button14 = Button(self.page1, width=18, height=2, text="Exit", bg='gray', font=("宋", 12),
                               relief='raise', command=self.quitMain)
        self.button14.pack(side=LEFT, padx=25, pady=80)

        numIdx = 20  
        frames = [PhotoImage(file='welcome.gif',format='gif -index %i' % (i)) for i in range(numIdx)]
        def update(idx):
            frame = frames[idx]
            idx += 1 
            self.wel_label.configure(image=frame)  
            self.page1.after(400, update, idx % numIdx)  
        self.page1.after(0, update, 0) 




    def createSecondPage(self): 
        self.root.geometry('%dx%d' % (800, 600))
        self.camera = cv2.VideoCapture(0)
        self.page1.pack_forget()
        self.page2 = Frame(self.root,height=600) #主frame
        self.page2.pack()

        self.frame_t = Frame(self.page2)
        self.frame_t.pack(side='top')

        self.frame_b = Frame(self.page2)  
        self.frame_b.pack(side='bottom')

        self.data2 = Label(self.frame_t) 
        self.data2.pack() 

        self.button20 =  Button(self.frame_b, width=18, height=2, text="Detect", bg='gray', font=("宋", 12),
               relief='raise', command=self.takePhoto)
        self.button20.pack(side=LEFT, padx=25, pady=30)
        self.button23 = Button(self.frame_b, width=18, height=2, text="Return", bg='gray', font=("宋", 12),
                               relief='raise', command=self.backFirst)
        self.button23.pack(side=LEFT, padx=25, pady=30)
        self.video_loop(self.data2)

    def takePhoto(self):
        cv2.imwrite("./obj.png",self.frame)

        image = cv2.imread('obj.png')
        bboxes, result = self.yolo.predict(image)
        self.name_list = []
        for item in result:
            temp=item.replace('_',' ')
            self.name_list.append(temp)

        print(self.name_list)
        self.yolo.draw(image, bboxes)

        self.det_num=len(self.name_list)
        print(self.det_num)
        if self.det_num == 0: messagebox.showerror(message='Sorry, Not detected!')
        else:
            messagebox.showinfo(title='Hi', message='You have successfully uploaded, please waiting...')
            self.camera.release()
            self.root.geometry('%dx%d' % (800, 600))
            self.data2.pack_forget()
            self.button20.pack_forget()
            self.button23.pack_forget()
            # self.button20.pack_forget()

            Label(self.frame_t, text='行李提示\nPacking Tips', fg='#8B4513', font=('Arial', 25, 'bold italic')).pack()

            pic_name = 'text.png'
            img_open = Image.open(pic_name)
            image = img_open.resize((150, 120), Image.ANTIALIAS)
            img_png = ImageTk.PhotoImage(image)
            label_img = Label(self.frame_t, image=img_png)
            label_img.pack()

            string_obj = 'Object Detection:'+self.name_list[0]
            # self.search_top_var.set('行李提示\nPacking Tips\n\n查询(Query):' + string)
            # self.search_label.config(text=self.search_top_var)
            self.det_name = Label(self.frame_t, text=string_obj, fg='#8B4513', font=('Arial', 25, 'bold italic'))
            self.det_name.pack()


            self.detect_canvas = Canvas(self.frame_t, height=70, width=550)

            flag, result = search_new.getCheck(self.name_list[0])

            flag1 = result['carry_on']
            flag2 = result['checked']
            if flag1 == 0:
                flag1_color = 'red'
            else:
                flag1_color = 'green'
            if flag2 == 0:
                flag2_color = 'red'
            else:
                flag2_color = 'green'

            tip_result =result['detail']
            self.detect_canvas.create_text(100, 40, fill='#8B4513', text='        手提行李\nCarry-on Baggage', font=('宋体',18,'bold italic'))
            self.detect_canvas.create_oval(190, 25, 210, 45, fill=flag1_color)
            self.detect_canvas.create_text(400, 40, fill='#8B4513', text='        寄舱行李\nChecked Baggage', font=('宋体',18,'bold italic'))
            self.detect_canvas.create_oval(490, 25, 510, 45, fill=flag2_color)
            self.detect_canvas.pack()

            self.tips = scrolledtext.ScrolledText(self.frame_t, bg='#F5F5F5', width=45, height=10, font=("隶书", 18))
            self.tips.insert(END, tip_result)
            self.tips.pack()

            def changeNext():
                self.next_flag += 1
                print(self.next_flag)
                if (self.next_flag+1) == self.det_num: self.button24.pack_forget()
                self.det_name.config(text='Object Detection:'+self.name_list[self.next_flag])

                flag, result = search_new.getCheck(self.name_list[self.next_flag])
                flag1 = result['carry_on']
                flag2 = result['checked']
                if flag1 == 0:
                    flag1_color = 'red'
                else:
                    flag1_color = 'green'
                if flag2 == 0:
                    flag2_color = 'red'
                else:
                    flag2_color = 'green'
                tip_result = result['detail']
                print('7777',flag1_color,flag2_color)

                self.detect_canvas.create_oval(190, 25, 210, 45, fill=flag1_color)
                self.detect_canvas.create_oval(490, 25, 510, 45, fill=flag2_color)
                self.tips.delete(1.0,END)
                self.tips.insert(END, tip_result)
                print(self.next_flag)
                print(self.det_num)

            self.button24 = Button(self.frame_t, width=18, height=2, text="next", bg='gray', font=("宋", 12),
                                   relief='raise',command=changeNext)
            self.next_flag=0
            if (self.next_flag+1)!=self.det_num: self.button24.pack()
            Button(self.frame_t, width=18, height=2, text="Back", bg='gray', font=("宋", 12),
                   relief='raise', command=self.backFirst).pack()
            self.frame_t.mainloop()


    def video_loop(self, panela):
        success, img = self.camera.read()
        self.frame = img
        if success:
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
            current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=current_image)
            panela.imgtk = imgtk
            panela.config(image=imgtk,height=500)
            self.root.after(1, lambda: self.video_loop(panela))

    def SearchObject(self):
        self.page1.pack_forget()
        self.page3 = Frame(self.root)
        self.page3.pack()

        self.frame_3t = Frame(self.page3)
        self.frame_3t.pack()

        self.search_top_var = StringVar()
        self.search_top_var.set('\nInput the object name, waiting...\n')
        self.search_label = Label(self.frame_3t, textvariable=self.search_top_var, fg='#8B4513', font=('Arial', 30,'bold italic'))
        self.search_label.pack()
        def on_keyrelease(event):
            value = event.widget.get()
            value = value.strip().lower()
            if value == '':
                data = []
            else:
                data = []
                for item in set(search_new.getSuggest(value)):
                    data.append((item))
            listbox_update(data)

        def listbox_update(data):
            self.lb.pack()
            self.button32.pack()
            self.button33.pack()
            self.lb.delete(0, 'end')
            data = sorted(data, key=str.lower)
            for item in data:
                self.lb.insert('end', item)

        e = StringVar()
        e.set('')
        self.input_object = Entry(self.frame_3t,textvariable=e, width=20)
        self.input_object.pack()
        self.input_object.bind('<KeyRelease>', on_keyrelease)

        def on_select(event):
            e.set(event.widget.get(event.widget.curselection()))
            print('(event) previous:', event.widget.get('active'))
            print('(event)  current:', event.widget.get(event.widget.curselection()))
            print('---')
        self.lb = Listbox(self.frame_3t)
        # self.lb.pack()
        self.lb.bind('<<ListboxSelect>>', on_select)

        self.button32 = Button(self.frame_3t, width=15, height=2, text="Search", bg='gray', font=("宋", 12),
               relief='raise', command=self.getselect)
        # self.button32.pack()#.place(x=250,y=200)
        self.button33 = Button(self.frame_3t, width=15, height=2, text="Return", bg='gray', font=("宋", 12),
               relief='raise', command=self.backMain)
        # self.button33.pack()

    def getresult(self,flag,data={}):
        if flag == 1:
            item = self.tree.selection()[0]
            category = (self.tree.item(item, "values"))[0]
            data = search_new.getDetail(category)
            self.tree.pack_forget()


        string = self.object_name
        self.search_top_var.set('行李提示\nPacking Tips\n\n查询(Query):'+string)
        self.search_label.config(text=self.search_top_var)


        flag1 = data['carry_on']
        flag2 = data['checked']
        if flag1 == 0: flag1_color='red'
        else: flag1_color='green'
        if flag2 == 0: flag2_color='red'
        else: flag2_color='green'

        tip_result = data['detail']

        self.canvas = Canvas(self.frame_3t, height=70, width=700)
        self.canvas.create_text(180, 50, fill='#8B4513',text='        手提行李\nCarry-on Baggage', font=('宋体',18,'bold italic'))
        self.canvas.create_oval(260, 45, 280, 65, fill=flag1_color)
        self.canvas.create_text(480, 50, fill='#8B4513', text='        寄舱行李\nChecked Baggage',font=('宋体',18,'bold italic'))
        self.canvas.create_oval(560, 45, 580, 65, fill=flag2_color)

        self.canvas.pack()
        tips = scrolledtext.ScrolledText(self.frame_3t,bg='#F5F5F5',width=45, height=10,font=("隶书",18))
        tips.insert(END,tip_result)
        tips.pack()

        self.button33.pack()
    def getselect(self):
        self.button32.pack_forget()
        self.button33.pack_forget()
        self.lb.delete(0, END)
        self.lb.pack_forget()
        self.input_object.pack_forget()
        value = self.input_object.get()
        self.object_name=str(value)
        print('根据用户选择的的object得到的keys：'+ value)

        flag, result = search_new.getCheck(value)
        if flag == "detail":
            resultFlag=0
            print("行李提示")
            print('手提行李', result['carry_on'])
            print('寄舱行李', result['checked'])
            print('详情', result['detail'])
            self.getresult(resultFlag,result)
        else:
            resultFlag = 1
            if len(result['category']) == 0:
                messagebox.showerror(message='在限制性物品和危險品中沒有查詢到該物品。\n您可以嘗試不同的搜索詞。\n如果仍有疑問，您可以詢問機場的工作人員。\nThis item was not found in restricted goods and dangerous goods.\nYou can try different search terms.\nIf you still confused, you can ask the staff at the airport.\n')
                self.page3.pack_forget()
                self.SearchObject()
            else:
                print("aaaaaaaa搜索结果：")
                for i in range(0, len(result['category'])):
                    print("----------------------------")
                    print("第一行：", result['category'][i])
                    print("第二行：", result['name'][i])
                # cate_key=result['category']
                self.search_top_var.set('\nCATEGORIES\n')
                self.search_label.config(text=self.search_top_var)
                self.tree = ttk.Treeview(self.frame_3t, show="headings", height=10,columns=('col1', 'col2'))
                self.tree.column('col1', width=500, anchor='w')
                self.tree.column('col2', width=500, anchor='w')
                self.tree.heading('col1', text='TYPES')
                self.tree.heading('col2', text='EXAMPLES')

                for i in range(len(result['category'])):
                    self.tree.insert('', i, values=(result['category'][i], result['name'][i]))

                def onDBClick(event):
                    self.getresult(resultFlag)
                self.tree.bind("<Double-1>", onDBClick)


                self.tree.pack()

    # def getmatch(self):
    #     self.button33.pack_forget() #返回按钮隐藏
    #     self.lb.pack()
    #     qianzhui = self.input_object.get() #用户输入的前缀
    #     print('用户输入的前缀：'+ qianzhui)
    #     match = ['apple', 'watermenon', 'orange']
    #     self.button32.pack_forget() #匹配按钮隐藏
    #     self.button31.pack(side=TOP, pady=50)
    #     self.lb.delete(0, END)
    #     for item in match:
    #         self.lb.insert(0, item)


    def backFirst(self):
        self.root.geometry('%dx%d' % (800, 500))
        self.page2.pack_forget()
        self.page1.pack()
        self.camera.release()
        cv2.destroyAllWindows()

    def backMain(self):
        self.page3.pack_forget()
        self.page1.pack()

    def quitMain(self):
        sys.exit(0)


if __name__ == '__main__':
    demo = APP()

