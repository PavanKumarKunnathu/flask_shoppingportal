from flask import Flask,render_template,request,redirect,flash,session
from werkzeug.utils import secure_filename
import logging
from model import *
from model import Products
import os
from werkzeug.security import generate_password_hash, check_password_hash





app=Flask(__name__)
app.secret_key = "pavan"


logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s)') 

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/hello')
def hello():
    return ' hii dude'

@app.route('/home')
def Home():
    all_products=eng.execute("select * from products order by product_date")
    all_subcategories=eng.execute("select * from sub_categories ")
    return render_template('home.html',all_products=all_products,all_subcategories=all_subcategories)

@app.route('/login')
def Login():      
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def Register():
    if request.method =='POST' and 'phone' in request.form and 'email' in request.form and 'password' in request.form:
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        password=request.form['password']
        hashed_password=generate_password_hash(password)
       
        temp=""
        for i in (eng.execute("select email from users where email= %s limit 1", (email))):
            temp=i.email
        if str(temp) == email:	
            flash('Email already exist')
            return redirect('/login')   
        else:
            eng.execute("INSERT INTO users(name, phone, email, password) VALUES(%s, %s, %s, %s)",(name, phone, email, hashed_password))
            flash('You have successfully registered !! Please Login to continue')
            return redirect('/login')

@app.route('/loginValidation',methods=['GET', 'POST'])
def LoginValidation():
     if request.method =='POST' and 'useremail' in request.form and 'userpass' in request.form:
        email=request.form['useremail']
        password=request.form['userpass']

        if email == 'Admin@gmail.com' and password == 'admin':
            session['admin_email']='Admin@gmail.com'
            return redirect('/adminhome')
        for i in (eng.execute("select * from users where email= %s limit 1", (email))):
            if i.email==email:
                if check_password_hash(i.password, password):
                   session['email']=email
                   session['username']=i.name
                   flash('You have successfully logged in')
                  
                   return redirect('/')
                else:
                    flash('Wrong Password')
                    return redirect('/login')
        else:
            flash('Not Registered Please Sign up')
            return redirect('/login')

        

@app.route('/demo')
def demo():
    # app.logger.info('Index page loaded fine!') 
    # app.logger.warning('this seems to a problem!') 
    return render_template('index.html',name="pavan")

@app.route('/')
def HomePage():
    email=""
    if 'email' in session:
        email=session['email']
        username=session['username']
        cart_value=eng.execute("select count(*) from cart where email=%s",email).fetchall() 
        return render_template('index.html',email=email,username=username,cart_length=cart_value[0][0])
    return render_template('index.html',email=email)

@app.route('/allproducts')
def Items():
    cat_and_subcat={}
    category_names={}
    all_carts=[]
    scat_id=""
    items=eng.execute("select * from  products  ;")
    all_cat=eng.execute("select * from categories ;")
    categories=eng.execute("select * from categories ;")
    all_scat=eng.execute("select * from sub_categories ;")
    for i in categories:
        c=eng.execute("select * from sub_categories where category_id=%s",i.category_id)  
        cat_and_subcat[i.category_id]=c
        category_names[i.category_id]=i.category_name
    if 'email' in session:
        email=session['email']
        username=session['username']
        cart=eng.execute("select * from cart where email=%s",email)
        cart_value=cart.fetchall() 
        for i in cart_value:
            all_carts.append(i[2])
        return render_template('items.html',items=items,all_cat=all_cat,all_scat=all_scat,scat_id=scat_id,cat_and_subcat=cat_and_subcat,category_names=category_names,email=email,username=username,cart_length=len(cart_value),cart=cart,all_carts=all_carts)
    return render_template('items.html',items=items,all_cat=all_cat,all_scat=all_scat,scat_id=scat_id,cat_and_subcat=cat_and_subcat,category_names=category_names)

@app.route('/items/<scat_id>')
def SelectItems(scat_id):
    cat_and_subcat={}
    category_names={}
    all_carts=[]
    items=eng.execute("select * from  products  where subcategory_id=%s",scat_id)
    all_cat=eng.execute("select * from categories ")
    categories=eng.execute("select * from categories ;")
    all_scat=eng.execute("select * from sub_categories ")
    for i in categories:
        c=eng.execute("select * from sub_categories where category_id=%s",i.category_id)  
        cat_and_subcat[i.category_id]=c
        category_names[i.category_id]=i.category_name
    if 'email' in session:
        email=session['email']
        username=session['username']
        cart=eng.execute("select * from cart where email=%s",email)
        cart_value=cart.fetchall() 
        for i in cart_value:
            all_carts.append(i[2])
        return render_template('items.html',items=items,all_cat=all_cat,all_scat=all_scat,scat_id=scat_id,cat_and_subcat=cat_and_subcat,category_names=category_names,email=email,username=username,cart_length=len(cart_value),cart=cart,all_carts=all_carts)

    return render_template('items.html',items=items,all_cat=all_cat,all_scat=all_scat,scat_id=scat_id,cat_and_subcat=cat_and_subcat,category_names=category_names)



# admin things

@app.route('/adminhome')
def AdminHome():
    s=eng.execute("select * from products")
    all_categories=eng.execute("select * from  categories ;")
    all_cat=eng.execute("select * from  categories ;")
    all_subcategories=eng.execute("select * from  sub_categories order by category_id ;")
    all_cat_names={}
    for i in all_cat:
        all_cat_names[i.category_id]=i.category_name

    list_users=s.fetchall()
    
    if 'admin_email' in session:
        admin_email=session['admin_email']
        return render_template('admin/admin_home.html',list_users = list_users,all_categories=all_categories,all_subcategories=all_subcategories,all_cat_names=all_cat_names)
    return redirect('/login')


    
@app.route('/categories')
def Categories():
    return render_template('admin/admin_addCotegory.html')

@app.route('/addcategories',methods=['POST'])
def AddCategories():
    if request.method=="POST":
        id=uuid.uuid4()
        category=request.form['category']
        ins=eng.execute("insert into categories (category_id,category_name) values (%(cat_id)s, %(cat_name)s)", {"cat_id":id, "cat_name":category})
        return render_template('admin/admin_addCotegory.html',message=category)
@app.route('/editcategories/<cat_id>')
def EditCategories(cat_id):
    cat_data=eng.execute("select * from  categories where category_id=%s",cat_id)
    category_data=cat_data.fetchall()
    return render_template('admin/admin_editcategory.html',category_data=category_data)

@app.route('/updatecategories',methods=['POST'])
def UpdateCategories():
    if request.method=="POST":
        id=request.form['category_id']
        category=request.form['category']
        update=eng.execute("update  categories set category_name=%s where category_id=%s",(category,id))
        flash('Category Updated Successfully')
        return redirect('/adminhome')

@app.route('/deletecategories/<cat_id>')
def DeleteCategories(cat_id):
    eng.execute('DELETE FROM categories WHERE category_id = %s',(cat_id))
    flash('category Removed Successfully')
    return redirect('/adminhome')

@app.route('/subcategories')
def SubCategories():
    all_categories=eng.execute("select * from  categories ;")
    return render_template('admin/admin_addSubcategory.html',all_categories=all_categories)


@app.route('/addsubcategory',methods=['POST'])
def AddSubCategory():
    c_id=request.form['category_id']
    subcat_name=request.form['subcategory']
    subcat_id=uuid.uuid4()
    all_categories=eng.execute("select * from  categories ;")
    # add_sub=SubCategories(subcat_id,c_id,subcat_name)
    # db.session.add(add_sub)
    # db.session.commit()
    add_sub_category=eng.execute("insert into sub_categories (subcategory_id,category_id,subcategory_name) values (%(subcat_id)s, %(c_id)s, %(subcat_name)s)", {"subcat_id":subcat_id,"c_id":c_id, "subcat_name":subcat_name})
    return render_template('admin/admin_addSubcategory.html',all_categories=all_categories,message=subcat_name) 

@app.route('/editsubcategories/<scat_id>')
def EditSubCategories(scat_id):
    all_categories=eng.execute("select * from  categories ;")
    selected_category=eng.execute("select c.category_id,c.category_name  from  categories as c inner join sub_categories as s on c.category_id=s.category_id where s.subcategory_id=%s",scat_id).fetchall()
    scat_data=eng.execute("select * from  sub_categories where subcategory_id=%s",scat_id)
    scategory_data=scat_data.fetchall()
    return render_template('admin/admin_editSubCategory.html',scategory_data=scategory_data,all_categories=all_categories,selected_category=selected_category)

@app.route('/updatesubcategories',methods=['POST'])
def UpdateSubCategories():
    if request.method=="POST":
        id=request.form['scategory_id']
        scategory=request.form['subcategory']
        update=eng.execute("update  sub_categories set subcategory_name=%s where subcategory_id=%s",(scategory,id))
        flash('SubCategory Updated Successfully')
        return redirect('/adminhome')
        
@app.route('/deletesubcategories/<scat_id>')
def DeleteSubCategories(scat_id):
    eng.execute('DELETE FROM sub_categories WHERE subcategory_id = %s',(scat_id))
    flash('subcategory Removed Successfully')
    return redirect('/adminhome')


@app.route('/products')
def Products():
    all_categories=eng.execute("select * from  categories ;")
    all_subcategories=eng.execute("select * from  sub_categories ;")
    return render_template('admin/admin_addProduct.html',all_categories=all_categories,all_subcategories=all_subcategories)

@app.route('/getsubcategories',methods=['POST'])
def getSubCategory():
    c_id=request.form['cat_id']
    s=""
    get_allsub=eng.execute("select * from  sub_categories  where  category_id=%s",(c_id))
    for i in get_allsub:
        s+="<option value="+i.subcategory_id+">"+i.subcategory_name+"</option>"
    return s
@app.route('/addtocart/<prod_id>')
def AddToCart(prod_id): 
    email=session['email']
    ins=eng.execute("insert into cart(email,product_id) values(%s,%s)",(email,prod_id))
    all_prod=eng.execute("select subcategory_id from products where product_id=%s limit 1",prod_id).fetchall()
    return redirect('/items/'+all_prod[0][0]) 
@app.route('/cart')
def cart():
    email=session['email']
    cart_items=eng.execute('''select * from products where product_id in
                        (select product_id from cart where email=%s)
    
                        ''',email).fetchall()
    total_count=0
    for i in cart_items:
        total_count+=int(i.price)
    return render_template('cart.html',cart_items=cart_items,total_count=total_count)
    
   
@app.route('/addproducts',methods=['POST'])
def AddProducts():
    if request.method=="POST":
        c_id=request.form['category_id']
        sc_id=request.form['subcategory_id']
        p_name=request.form['product_name']
        actual_price=request.form['price']
        s_price=request.form['striked_price']
        product_image=request.files['product_image']
        prod_id=uuid.uuid4()
        product_date=datetime.datetime.utcnow()

        all_categories=eng.execute("select * from  categories ;")
        all_subcategories=eng.execute("select * from  sub_categories ;")

        filename = secure_filename(product_image.filename)
        
        eng.execute('''insert into products (product_id,category_id,subcategory_id,product_name,price,striked_price,product_image,product_date) 
                    values(%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (prod_id,c_id,sc_id,p_name,actual_price,s_price,filename,product_date)
                    )
        product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('admin/admin_addProduct.html',all_categories=all_categories,all_subcategories=all_subcategories,message=p_name)

@app.route('/editproducts/<prod_id>')
def EditProduct(prod_id):
    all_categories=eng.execute("select * from  categories ;")
    all_subcategories=eng.execute("select * from  sub_categories ;")
    selected_category=eng.execute("select c.category_id,c.category_name  from  categories as c inner join products as s on c.category_id=s.category_id where s.product_id=%s",prod_id).fetchall()
    selected_subcategory=eng.execute("select s.subcategory_id,s.subcategory_name  from  sub_categories as s inner join products as p on p.subcategory_id=s.subcategory_id where p.product_id=%s",prod_id).fetchall()
    prod_data=eng.execute("select * from  products where product_id=%s",prod_id)
    product_data=prod_data.fetchall()
    return render_template('admin/admin_editProduct.html',product_data=product_data,all_categories=all_categories,selected_category=selected_category,all_subcategories=all_subcategories,selected_subcategory=selected_subcategory)

@app.route('/deleteproducts/<prod_id>')
def DeleteProducts(prod_id):
    eng.execute('DELETE FROM products WHERE product_id = %s',(prod_id))
    flash(' product Removed Successfully')
    return redirect('/adminhome')
@app.route('/updateproducts',methods=['POST'])
def UpdateProducts():
    if request.method=="POST":
        c_id=request.form['category_id']
        sc_id=request.form['subcategory_id']
        p_name=request.form['product_name']
        actual_price=request.form['price']
        s_price=request.form['striked_price']
        product_image=request.files['product_image']
        prod_id=request.form['product_id']
        product_date=datetime.datetime.utcnow()

        all_categories=eng.execute("select * from  categories ;")
        all_subcategories=eng.execute("select * from  sub_categories ;")

        filename = secure_filename(product_image.filename)
        
        eng.execute('''update products set category_id=%s,subcategory_id=%s,product_name=%s,price=%s,striked_price=%s,product_image=%s,product_date=%s where product_id=%s 
                    ''',
                    (c_id,sc_id,p_name,actual_price,s_price,filename,product_date,prod_id)
                    )
        product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        flash('product updated Successfully')
        return redirect('/adminhome')

@app.route('/deletecartitem/<prod_id>')
def DeleteCartItem(prod_id):
    email=session['email']
    eng.execute("delete from cart where product_id=%s and email=%s ",(prod_id,email))
    return redirect('/cart')

@app.route('/thanks')
def Thankyou():
    return render_template('thanks.html')


@app.route('/home/<user_id>')
def home(user_id):
    return render_template('home.html',uid=user_id)
@app.route('/logout')
def logout():
    session.pop('email',None)
    session.pop('username',None)
    return redirect('/login')

@app.route('/adminlogout')
def AdminLogout():
    session.pop('admin_email',None)
    return redirect('/login')


if __name__=='__main__':
    app.run(debug=True)