from flask import Flask, render_template,request,redirect,url_for
from datetime import datetime,date

import sqlite3
app=Flask(__name__)
e=""
p=""
@app.route('/')
def home():
    return render_template('home.html')
'''@app.route('/homepage')
def homepage():
    return render_template('homepage.html')'''
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('customer_register.html')

@app.route('/result',methods = ['POST'])
def result():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    m=request.form['name']
    n=request.form['email']
    o=request.form['pswd']
    d=request.form['dr_no']
    p=request.form['ph_no']
    q=request.form['street']
    r=request.form['city']
    s=request.form['state']
    t=request.form['pin']
    
    #cur.execute("INSERT INTO admin (ad_name,ad_email,ad_pswd,ad_ph_no,ad_street,ad_city,ad_state,ad_pin) VALUES (?,?,?,?,?,?,?,?)" ,(m,n,o,p,q,r,s,t))
    cur.execute("insert into customer(cus_name,cus_email,cus_pswd,cus_phn_no,cus_dr_no,cus_street,cus_city,cus_state,cus_pin) values(?,?,?,?,?,?,?,?,?)",(m,n,o,p,d,q,r,s,t))
    
    conn.commit()
    return "sucessfull"


@app.route('/loginvalidate',methods=['POST'])
def loginvalidate():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    global e,p
    e=request.form['email']
    p=request.form['pswd']
    cur.execute("select count(*) from admin where ad_email=='"+e+"' and ad_pswd=='"+p+"'")
    rows=cur.fetchone()
    if rows[0]==0:
        cur.execute("select count(*) from customer where cus_phn_no=='"+e+"' and cus_pswd=='"+p+"'")
        res=cur.fetchone()
        if(res[0]==0):
            return "invalid user"
        else:
            cur.execute("delete from orders where or_cus_phn_no=='"+e+"' and or_status=='pending' ")
            conn.commit()                        
            val=(e,date.today(),'pending')
            cur.execute("insert into orders(or_cus_phn_no,or_date,or_status) values(?,?,?)",val)
            conn.commit()
            cur.execute("select or_id from orders where or_cus_phn_no=='"+e+"' order by or_id desc limit 1")
            res=cur.fetchone()
            global orderid
            orderid=res[0]
            return redirect(url_for('cuspage'))
    else:
        return render_template('admin_page.html')

'''@app.route('/loginvalidate',methods=['POST'])
def loginvalidate():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    global e,p
    e=request.form['email']
    p=request.form['pswd']
    cur.execute("select count(*) from admin where ad_email=='"+e+"' and ad_pswd=='"+p+"'")
    rows=cur.fetchone()
    if rows[0]==0:
        cur.execute("select count(*) from customer where cus_email=='"+e+"' and cus_pswd=='"+p+"'")
        res=cur.fetchone()
        if(res[0]==0):
            return "invalid user"
        else:
            
            return redirect(url_for('cuspage'))
    else:
        return render_template('admin_page.html')'''



@app.route('/customerpage')
def cuspage():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    #cur.execute("select cus_name from customer where cus_email=='"+e+"'")
    cur.execute("select cus_name from customer where cus_phn_no=='"+e+"' and cus_pswd=='"+p+"'")
    name=cur.fetchone()
    return render_template('customer.html',name=name[0])
    #return render_template('customerpage.html',name=name[0])



@app.route('/adminadd')
def adminadd():
    return render_template('admin_add.html')


    
@app.route('/additem', methods=['POST'])
def additem():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    pname=request.form['pn']
    pcat=request.form['cp']
    pimg=request.form['p3']
    pdesc=request.form['p4']
    pcost=request.form['p5']
    pqty=request.form['pq']
    val=(pname,pcat,pimg,pdesc,pcost,pqty)
    cur.execute("insert into product (pr_name,pr_cat_name,pr_img,pr_desc,pr_price,pr_qty) values(?,?,?,?,?,?)",val)
    conn.commit()
    return "inserted"


@app.route('/updateform')
def updateform():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    
    cur.execute("select  pr_id from product  ")
    row=cur.fetchall()
    return render_template('updateitem.html',row=row)

@app.route('/adminupdate',methods=['POST'])
def adminupdate():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    pid=request.form['p1']
    cur.execute("select * from product where pr_id=='"+pid+"' ")
    rows=cur.fetchone()
    return render_template('admin_update.html',rows=rows)


@app.route('/updateitem',methods=['POST'])
def updateitem():
     conn=sqlite3.connect('ecommerce.db')
     cur=conn.cursor()
     pid=request.form['p1']
     pname=request.form['pn']
     pcat=request.form['cp']
     pimg=request.form['p3']
     pdesc=request.form['p4']
     pcost=request.form['p5']
     pqty=request.form['p6']
     cur.execute("update product set pr_id='"+pid+"',pr_name='"+pname+"',pr_cat_name='"+pcat+"',pr_img='"+pimg+"',pr_desc='"+pdesc+"',pr_price='"+pcost+"',pr_qty='"+pqty+"' where pr_id=='"+pid+"' ")
     conn.commit()
     return "updated items successfully"



'''@app.route('/editdelsaree')
def editdelsaree():
    return render_template('delsaree.html')'''
@app.route('/editdelsaree')
def editdelsaree():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select  pr_id from product  ")
    row=cur.fetchall()
    return render_template('delitem.html',row=row)

@app.route('/delete_item', methods=['post'])
def delete_item():
    i=request.form['i']
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from product where pr_id=='"+i+"' ")
    rows=cur.fetchone()
    if(rows==None):
            return ("No records")
    else:
        return render_template("del_itemrecord.html",rows=rows)


@app.route('/delete_item_rec', methods=['post'])
def delete_item_rec():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    i=request.form['i']
    pname=request.form['pn']
    pcat=request.form['cp']
    pimg=request.form['p3']
    pdesc=request.form['p4']
    pcost=request.form['p5']
    pqty=request.form['p6']
    cur.execute("delete from product where pr_id == '"+i+"' ")
    conn.commit()
    cur.execute("select * from product")
    x=cur.fetchall()
    return render_template("item_rec_delete.html",x=x)

@app.route('/view_items/<catname>')
def view_items(catname):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from product where pr_name=='"+catname+"' ")
    x=cur.fetchall()
    return render_template("item_rec_delete.html",x=x)







    

@app.route('/adminorder') 
def adminorder():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,orders o,cart c where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and or_status=='placed' order by o.or_id desc")
    rows=cur.fetchall()     
    return render_template('admin_order.html',rows=rows)


@app.route('/cancelorder/<iid>') 
def cancelorder(iid):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("update orders  set or_status='cancelled' where or_id=='"+iid+"' ")
    conn.commit()
    return redirect(url_for('adminorder')) 

@app.route('/finishorder/<iid>') 
def finishorder(iid):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("update orders set or_status='finished' where or_id=='"+iid+"' ")
    conn.commit()
    return redirect(url_for('adminorder'))

@app.route('/getdetails/<iid>') 
def getdetails(iid):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from doordetails where do_or_id=='"+iid+"' ")
    rows=cur.fetchone()
    return render_template('view_door_delivery.html',rows=rows)


@app.route('/adminfinish/') 
def adminfinish():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,orders o,cart c where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and or_status=='finished' order by o.or_id desc")
    rows=cur.fetchall()
    return render_template('admin_finish.html',rows=rows)  

@app.route('/admincancel') 
def admincancel():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,orders o,cart c where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and or_status=='cancelled' order by o.or_id desc")
    rows=cur.fetchall()
    return render_template('admin_finish.html',rows=rows)

######
@app.route('/product/<catname>')
def product(catname):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from product where pr_name == '"+catname+"' ")
    x=cur.fetchall()
    return render_template('itemlist.html',x=x)


@app.route('/productquantityform/<ptid>')
def productquantityform(ptid):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from product where pr_id== '"+ptid+"' ")
    x=cur.fetchone()
    return render_template('cart.html',rows=x)

'''@app.route('/productquantityform/<ptid>')
def productquantityform(ptid):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from product where pr_id== '"+ptid+"' ")
    x=cur.fetchone()
    return "first need to log in"'''


@app.route('/addtocart',methods=['POST'])
def addtocart():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cpid=request.form['p1']
    cq=request.form['q']
    cat=request.form['cat']
    cur.execute("select count(*) from cart where cart_or_id=='"+str(orderid)+"' and cart_pr_id=='"+cpid+"'")
    x=cur.fetchone()
    if(x[0]==0):
        cur.execute("insert into cart (cart_or_id,cart_pr_id,cart_quantity) values (?,?,?)",(orderid,cpid,cq))
    else:
        cur.execute("update cart set cart_quantity=='"+cq+"' where cart_or_id=='"+str(orderid)+"' and cart_pr_id=='"+cpid+"'")
                    
    conn.commit()
    cur.execute("select * from product where pr_name == '"+cat+"'")
    x=cur.fetchall()
    return render_template('itemlist.html',x=x)

@app.route('/viewcart')
def viewcart():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select pr_id,pr_name,pr_cat_name,pr_img,pr_price,cart_quantity,pr_price*cart_quantity as Total from product p,cart c where cart_or_id=='"+str(orderid)+"' and cart_pr_id==pr_id ")
    rows=cur.fetchall()
    total=0
    for row in rows:
        total=total+row[6]
    return render_template('viewcart.html',rows=rows,total=total)


@app.route('/doordelivery')
def doordelivery():
    #return str(orderid)
    return render_template('door_delivery.html',orderid=orderid)



'''@app.route('/finish',methods=['POST'])
def finish():
    global orderid
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    o=request.form['o']
    n=request.form['n']
    m=request.form['m']
    a=request.form['a']    #crebaseate door data
    cur.execute("INSERT INTO doordetails (do_or_id,do_name,do_ph_no,do_address) VALUES (?,?,?,?)" ,(o,n,m,a))
    cur.execute("update orders set or_status='placed' where or_id=='"+str(orderid)+"' ")
    conn.commit()
    val=(e,date.today(),'pending')
    cur.execute("insert into orders(or_cus_phn_no,or_date,or_status) values(?,?,?)",val)
    conn.commit()
    cur.execute("select or_id from orders where or_cus_phn_no=='"+e+"' order by or_id desc limit 1")
    res=cur.fetchone()
    orderid=res[0]
    return "placed successfully"'''

@app.route('/finish',methods=['POST'])
def finish():
    global orderid
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    o=request.form['o']
    n=request.form['n']
    m=request.form['m']
    a=request.form['a']    #crebaseate door data
    cur.execute("INSERT INTO doordetails (do_or_id,do_name,do_ph_no,do_address) VALUES (?,?,?,?)" ,(o,n,m,a))
    cur.execute("update orders set or_status='placed' where or_id=='"+str(orderid)+"' ")
    conn.commit()
    val=(e,date.today(),'pending')
    cur.execute("insert into orders(or_cus_phn_no,or_date,or_status) values(?,?,?)",val)
    conn.commit()
    cur.execute("select or_id from orders where or_cus_phn_no=='"+e+"' order by or_id desc limit 1")
    res=cur.fetchone()
    orderid=res[0]
    return "placed successfully"


@app.route('/placedorders') 
def placedorders():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    #cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,customer cu,orders o,cart c where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and or_status=='placed' and cu.cus_phn_no==o.or_cus_phn_no and cu.cus_email=='"+e+"' order by o.or_id desc")
    cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,customer cu,orders o,cart c where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and or_status=='placed' and cu.cus_phn_no==o.or_cus_phn_no and cu.cus_phn_no=='"+e+"' order by o.or_id desc")
    rows=cur.fetchall()
    return render_template('placedorders.html',rows=rows)


@app.route('/usercancelorder/<iid>') 
def usercancelorder(iid):
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("update orders set or_status='cancelled' where or_id=='"+iid+"' ")
    conn.commit()
    return redirect(url_for('placedorders'))

@app.route('/ucancelorders') 
def ucancelorders():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    #cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,orders o,cart c,customer cu where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and cu.cus_phn_no==o.or_cus_phn_no and or_status=='cancelled' and  cus_phn_no=='"+phn+"' order by o.or_id desc")
    cur.execute("select or_id,pr_img,pr_name,pr_price,cart_quantity,or_date,or_status from product p,orders o,cart c,customer cu where o.or_id==c.cart_or_id and p.pr_id==c.cart_pr_id and cu.cus_phn_no==o.or_cus_phn_no and or_status=='cancelled' and  cus_phn_no=='"+e+"' order by o.or_id desc")
    rows=cur.fetchall()
    return render_template('admin_finish.html',rows=rows)
#######

@app.route('/fetchuserdetails')
def fetchuserdetails():
    conn=sqlite3.connect('ecommerce.db')
    cur=conn.cursor()
    cur.execute("select * from customer where cus_phn_no=='"+e+"'")
    #cur.execute("select * from customer where cus_phn_no=='"+phn+"'")
    rows=cur.fetchone()
    return render_template('updateprofile.html',rows=rows)

@app.route('/savedetails',methods=['POST'])
def savedetails():
     conn=sqlite3.connect('ecommerce.db')
     cur=conn.cursor()
     name=request.form['n1']
     email=request.form['n2']
     passwd=request.form['n3']
     address=request.form['n4']
     street=request.form['n5']
     city=request.form['n6']
     #district=request.form['n7']
     state=request.form['n7']
     pincode=request.form['n8']
     phoneno=request.form['n9']
     cur.execute("update customer set cus_name='"+name+"',cus_email='"+email+"',cus_pswd='"+passwd+"',cus_dr_no='"+address+"',cus_street='"+street+"',cus_city='"+city+"',cus_state='"+state+"',cus_pin='"+pincode+"',cus_phn_no='"+phoneno+"' where cus_phn_no=='"+e+"' ")
     #cur.execute("update customer set cus_name='"+name+"',cus_email='"+email+"',cus_pswd='"+passwd+"',cus_dr_no='"+address+"',cus_street='"+street+"',cus_city='"+city+"',cus_state='"+state+"',cus_pin='"+pincode+"',cus_phn_no='"+phoneno+"' where cus_email=='"+e+"' ")
     conn.commit()
     return "updated successfully"


@app.route('/display')
def list():
   con = sqlite3.connect("ecommerce.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from customer")
   
   rows = cur.fetchall(); 
   return render_template("display.html",rows = rows)

orderid=""
e=""

    
if __name__ == '__main__':
   app.run(debug = True)



