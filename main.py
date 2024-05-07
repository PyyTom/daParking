import flet as fl,datetime,sqlite3
def main(page:fl.Page):
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
    page.window_full_screen=True
    page.theme_mode=fl.ThemeMode.LIGHT
    c_sector1=fl.Column(height=600)
    c_sector2=fl.Column(height=600)
    c_historial=fl.Column(controls=[fl.Row(controls=[fl.Text('HISTORIAL')],alignment=fl.MainAxisAlignment.CENTER)],height=600,scroll=fl.ScrollMode.ALWAYS)
    db = sqlite3.connect('db.db')
    db.execute('create table if not exists PARKING(NUMBER integer,STATUS)')
    if db.execute('select COUNT(*) from PARKING').fetchone()[0] == 0:
        for n in range(1, 11):
            db.execute('insert into PARKING VALUES(?,?)', (n, 'FREE',))
            db.commit()
    else:
        for n in range(1,6):
            if db.execute('select STATUS from PARKING where NUMBER=?',(n,)).fetchone()[0]=='FREE':color='green'
            else:color='red'
            c_sector1.controls.append(fl.ElevatedButton('PARKING '+str(n),icon=fl.icons.CAR_REPAIR,color=color,width=300,height=100,on_click=action))
        for n in range(6,11):
            if db.execute('select STATUS from PARKING where NUMBER=?', (n,)).fetchone()[0]== 'FREE':color = 'green'
            else:color = 'red'
            c_sector2.controls.append(fl.ElevatedButton('PARKING ' + str(n), icon=fl.icons.CAR_REPAIR, color=color, width=300, height=100,on_click=action))
    db.close()
    page.add(fl.Row(controls=[fl.Text('daPARKING')],alignment=fl.MainAxisAlignment.CENTER),
             fl.Row(controls=[fl.Column(width=50),c_sector1,fl.Column(width=200),c_sector2,fl.Column(width=50),c_historial]),
             fl.Row(controls=[fl.IconButton(icon=fl.icons.EXIT_TO_APP,icon_size=50,icon_color='red',on_click=xit)],alignment=fl.MainAxisAlignment.CENTER))
fl.app(target=main)