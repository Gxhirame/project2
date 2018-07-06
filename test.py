from tkinter import *
import tkinter.ttk as ttk
import sqlite3

dbname="test.db"
conn=sqlite3.connect(dbname)
c=conn.cursor()

try:
    c.execute('''PRAGMA foreign_keys=1''')
    #c.execute('''Drop table if exists company''') #Dropはテーブル削除
    c.execute('''Create table if not exists company
        (company_name UNIQUE,
        company_memo TEXT,
        information_name TEXT,
        information_contents TEXT,
        information_memo TEXT)''')
    '''
    #試しに一つ追加
    c.execute("
    Insert into company
    VALUES('Google','大手','給料','１００万', '残業代含む')")
    '''
    conn.commit()

except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])
    conn.commit()


def registration_company():
    company_name=entry_company_name.get()
    company_memo=entry_company_memo.get()
    information_name=entry_information_name.get()
    information_contents=entry_information_contents.get()
    information_memo=entry_information_memo.get()
    #entry_company_name.delete(0,END)
    entry_company_memo.delete(0,END)
    entry_information_name.delete(0,END)
    entry_information_contents.delete(0,END)
    entry_information_memo.delete(0,END)
    try:
        c.execute('''
        Insert into company
        (company_name, company_memo, information_name, information_contents, information_memo)
        Values(?,?,?,?,?)
        ''',(company_name, company_memo, information_name, information_contents, information_memo))
        conn.commit()
        print ("１件登録しました")
        print ("---会社名:", company_name, "---")
        print ("---メモ:", company_memo, "---")
        print ("---情報名:", information_name, "---")
        print ("---内容:", information_contents, "---")
        print ("---メモ:", information_memo, "---")


    #エラー処理
    except:
        print('''エラーにより登録できませんでした''')
        print(company_name, company_memo, information_name, information_contents, information_memo)




def open_information():
    third_window=list2.get()
    open_information=Tk()
    open_information.title(third_window)
    open_information.geometry("600x600+1000+250")
    list2.delete(0,END)


    treee=ttk.Treeview(open_information)
    treee["columns"]=(1,2,3)
    treee["show"]="headings"
    treee.column(1, width=10)
    treee.column(2, width=50)
    treee.column(3, width=90)


    treee.heading(1, text="情報名")
    treee.heading(2, text="内容")
    treee.heading(3, text="メモ")

    for o in c.execute("Select information_name, information_contents, information_memo from company where company_name=?", (third_window,)):
        treee.insert("","end",values=o)

    treee.pack(fill="x")


    close_button=Button(open_information, text="閉じる", relief="raised", height="4", width="6", command=open_information.destroy)
    close_button.pack()

    open_information.mainloop()


def delete():
    delete=entry_sub_win.get()
    entry_sub_win.delete(0,END)
    c.execute("Delete From company Where company_name=?", (delete,))
    print (delete, "を削除しました")


for N in c.execute('''Select company_name From company '''):
    print(N)

conn.commit()


win=Tk()
win.title("登録")
win.geometry("400x400+300+100")


#名前登録用
frame_company_name=Frame(win, pady=10)
frame_company_name.pack()

label_company_name=Label(frame_company_name, text="名前:", font="12")
label_company_name.pack(fill="x", side="left")


entry_company_name=Entry(frame_company_name, font=("", 12), justify="center", width=15)
entry_company_name.pack(side="right")


#メモ登録用
frame_company_memo=Frame(win, pady=10)
frame_company_memo.pack()

label_company_memo=Label(frame_company_memo, text="メモ:", font="12")
label_company_memo.pack(fill="x", side="left")

entry_company_memo=Entry(frame_company_memo, font=("", 12), justify="center", width=15)
entry_company_memo.pack(side="right")


#情報の名前登録用
frame_information_name=Frame(win, pady=10)
frame_information_name.pack()

label_information_name=Label(frame_information_name, text="情報名:", font="12")
label_information_name.pack(fill="x", side="left")

entry_information_name=Entry(frame_information_name, font=("", 12), justify="center", width=15)
entry_information_name.pack(side="right")


#情報の内容登録用
frame_information_contents=Frame(win, pady=10)
frame_information_contents.pack()

label_information_contents=Label(frame_information_contents, text="内容:", font="12")
label_information_contents.pack(fill="x", side="left")

entry_information_contents=Entry(frame_information_contents, font=("", 12), justify="center", width=15)
entry_information_contents.pack(side="right")


#情報のメモ登録用
frame_information_memo=Frame(win, pady=10)
frame_information_memo.pack()

label_information_memo=Label(frame_information_memo, text="情報メモ:", font="12")
label_information_memo.pack(fill="x", side="left")

entry_information_memo=Entry(frame_information_memo, font=("", 12), justify="center", width=15)
entry_information_memo.pack(side="right")

button_registration_company=Button(win, text="登録", relief="raised", height="4", width="6", command=registration_company)
button_registration_company.pack()


#２つ目のウィンドウ
sub_win=Toplevel()
sub_win.title("List")
sub_win.geometry("300x400+700+100")

tree=ttk.Treeview(sub_win)

tree["columns"]=(1,2)
tree["show"]="headings"
tree.column(1, width=10)
tree.column(2, width=90)

tree.heading(1, text="名前")
tree.heading(2, text="メモ")


for r in c.execute("Select company_name, company_memo from company"):
    tree.insert("","end",values=r)

tree.pack(fill="x")

frame_sub_win=Frame(sub_win, pady=10)
frame_sub_win.pack()


entry_sub_win=Entry(frame_sub_win, font=("",12), justify="center", width=15)
entry_sub_win.pack()

button_sub_win=Button(sub_win, text="削除", relief="raised", height="4", width="6", command=delete)
button_sub_win.pack()

#３つめのウィンドウ
Third_win=Toplevel()
Third_win.title("検索画面")
Third_win.geometry("600x125+1000+100")

frame_third_window=Frame(Third_win, pady=10)
frame_third_window.pack()

label_third_window=Label(frame_third_window, text="名前検索", font="12")
label_third_window.pack(fill="x")

val=StringVar()
query=c.execute("Select company_name from company")
listitems=query.fetchall()
list2=ttk.Combobox(frame_third_window, width=14, height=2)
list2["values"]=listitems
list2.pack()

'''entry_third_window=Entry(frame_third_window, font=("",12), justify="center", width=15)
entry_third_window.pack()'''

button_third_window=Button(Third_win, text="検索", relief="raised", height="4", width="6", command=open_information)
button_third_window.pack()

sub_win.mainloop()
Third_win.mainloop()
win.mainloop()

conn.commit()

