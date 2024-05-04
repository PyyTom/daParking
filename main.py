import flet as fl,datetime,sqlite3
db=sqlite3.connect('db.db')
db.execute('create table if not exists PARKING(NUMBER integer,STATUS)')
if db.execute('select COUNT(*) from PARKING').fetchone()[0]==0:
    for n in range(1,11):
        db.execute('insert into PARKING VALUES(?,?)',(n,'FREE',))
        db.commit()
db.close()
def main(page:fl.Page):
    page.window_full_screen=True
    def xit(e):
        page.window_destroy()
    def action(e):
        number=e.control.text.split(' ')[1]
        db=sqlite3.connect('db.db')
        status=db.execute('select STATUS from PARKING where NUMBER=?',(number,)).fetchone()
        if status[0]=='FREE':
            e.control.color = 'red'
            c_historial.controls.append(fl.Text('PARKING n.'+number+', OCCUPATED IN '+datetime.datetime.now().strftime('%m-%d,%Y AT %H:%M'),color='red'))
            db.execute('update PARKING set NUMBER=?,STATUS="OCCUPATE" where NUMBER=?',(number,number,))
        else:
            e.control.color = 'green'
            c_historial.controls.append(fl.Text('PARKING n.' +number+ ', LIBERATED IN ' + datetime.datetime.now().strftime('%m-%d,%Y AT %H:%M'),color='green'))
            db.execute('update PARKING set NUMBER=?,STATUS="FREE" where NUMBER=?', (number,number,))
        e.control.update()
        c_historial.update()
        db.commit()
        db.close()
    c_sector1=fl.Column(controls=[fl.ElevatedButton('PARKING '+str(n),icon=fl.icons.CAR_REPAIR,color='green',width=300,height=100,on_click=action) for n in range(1,6)],height=600)
    c_sector2=fl.Column(controls=[fl.ElevatedButton('PARKING '+str(n),icon=fl.icons.CAR_REPAIR,color='green',width=300,height=100,on_click=action) for n in range(6,11)],height=600)
    c_historial=fl.Column(controls=[fl.Row(controls=[fl.Text('HISTORIAL')],alignment=fl.MainAxisAlignment.CENTER)],height=600,scroll=fl.ScrollMode.ALWAYS)
    page.add(fl.Row(controls=[fl.Text('daPARKING')],alignment=fl.MainAxisAlignment.CENTER),
             fl.Row(controls=[fl.Column(width=50),c_sector1,fl.Column(width=200),c_sector2,fl.Column(width=50),c_historial]),
             fl.Row(controls=[fl.IconButton(icon=fl.icons.EXIT_TO_APP,icon_size=50,icon_color='red',on_click=xit)],alignment=fl.MainAxisAlignment.CENTER))
fl.app(target=main)