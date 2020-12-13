from app import *




        

def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            print("true")
            return f(*args, **kwargs)
        else:
            return redirect(url_for('admin_login'))

    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('add_trending_news'))
        else:
            return f(*args, **kwargs)
    return wrap


@app.route('/')
def index():
   

    total_corona_main_data = requests.get(app.config['TOTAL_DATA_URL']).json()
    total_confirm_cases = 0
    total_acive_cases = 0
    total_deaths = 0
    total_recovered = 0


    total_confirm_cases = total_corona_main_data['cases']
    total_acive_cases = total_corona_main_data['active']
    total_deaths = total_corona_main_data['deaths']
    total_recovered = total_corona_main_data['recovered']


    country_wise_data = []
    country_names = []
    
    get_country_wise_data = requests.get(app.config['TOTAL_COUNTRY_WISE_DATA_URL']).json()

    for corona_data in get_country_wise_data:
        info = {
          "country" : corona_data["country"],
          "confirmed" : corona_data["cases"],
          "active"   : corona_data["active"],
          "deaths"   : corona_data["deaths"],
          "recovered" : corona_data["recovered"]
        }
        country_names.append(corona_data["country"])
        country_wise_data.append(info)

    labels = []
    total_confirmed_f_graph = []
    total_deaths_f_graph = []
    total_recovered_f_graph = []



    get_total_corona_main_data_in_dt = requests.get(app.config["TOTAL_DATA_IN_DT_URL"]).json()

    for corona_data_dt in get_total_corona_main_data_in_dt["cases"]:
        labels.append(corona_data_dt)
        total_confirmed_f_graph.append(get_total_corona_main_data_in_dt["cases"][corona_data_dt])

    for corona_data_dt in get_total_corona_main_data_in_dt["deaths"]:
        total_deaths_f_graph.append(get_total_corona_main_data_in_dt["deaths"][corona_data_dt])    

    for corona_data_dt in get_total_corona_main_data_in_dt["recovered"]:
        total_recovered_f_graph.append(get_total_corona_main_data_in_dt["recovered"][corona_data_dt])    

        
    return render_template('index.html',total_confirm_cases=total_confirm_cases,total_active_cases = total_acive_cases,total_deaths=total_deaths,total_recovered=total_recovered,country_names=country_names,country_wise_data=country_wise_data,labels=labels,total_confirmed_f_graph=total_confirmed_f_graph,total_deaths_f_graph=total_deaths_f_graph,total_recovered_f_graph=total_recovered_f_graph)




@app.route('/top-10')
def top_10_cases():
    top_10_datas = []
    get_country_wise_data = requests.get(app.config['TOTAL_COUNTRY_WISE_DATA_URL']).json()

    for corona_data in get_country_wise_data:
        info = {
          "country" : corona_data["country"],
          "confirmed" : corona_data["cases"],
          "active"   : corona_data["active"],
          "deaths"   : corona_data["deaths"],
          "recovered" : corona_data["recovered"]
        }
        
        top_10_datas.append(info)
    
    top_10_datas = sorted(top_10_datas,key= lambda i:i['confirmed'],reverse=True)    

    top_10_datas = top_10_datas[:10]

    return render_template('top_10_datas.html',top_10_datas=top_10_datas)


@app.route('/bottom-10')
def bottom_10_cases():

    bottom_10_datas = []

    get_country_wise_data = requests.get(app.config['TOTAL_COUNTRY_WISE_DATA_URL']).json()

    for corona_data in get_country_wise_data:
        info = {
          "country" : corona_data["country"],
          "confirmed" : corona_data["cases"],
          "active"   : corona_data["active"],
          "deaths"   : corona_data["deaths"],
          "recovered" : corona_data["recovered"]
        }
        
        bottom_10_datas.append(info)


    bottom_10_datas = sorted(bottom_10_datas,key= lambda i:i['confirmed'])

    bottom_10_datas = bottom_10_datas[:10]

    return render_template('bottom_10_datas.html',bottom_10_datas=bottom_10_datas)    



@app.route('/country/<string:country_name>')
def country_wise_data(country_name):

    get_country_data = requests.get(app.config["COUNTRY_DATA_URL"].format(country_name)).json()

    total_confirmed = get_country_data["cases"]
    total_active = get_country_data["active"]
    total_deaths = get_country_data["deaths"]
    total_recovered = get_country_data["recovered"]

    labels = []
    total_confirmed_f_graph = []
    total_deaths_f_graph = []
    total_recovered_f_graph = []

    get_country_data_in_dt = requests.get(app.config["COUNTRY_DATA_IN_DT_URL"].format(country_name)).json()

    get_country_data_in_dt  = get_country_data_in_dt["timeline"]
        
    for corona_data_dt in get_country_data_in_dt["cases"]:
        labels.append(corona_data_dt)
        total_confirmed_f_graph.append(get_country_data_in_dt["cases"][corona_data_dt])

    for corona_data_dt in get_country_data_in_dt["deaths"]:
        total_deaths_f_graph.append(get_country_data_in_dt["deaths"][corona_data_dt])    

    for corona_data_dt in get_country_data_in_dt["recovered"]:
        total_recovered_f_graph.append(get_country_data_in_dt["recovered"][corona_data_dt]) 

    
    if  country_name == 'India':
        scrape_state_wise_date(app.config['STATE_WISE_DATA_URL'])

        state_wise_datas = []
        with open('state_wise_data.json') as json_file:
            data = json.load(json_file)

            for i in range(1,len(data['state_wise_data'])):

                info = {

                    "state" : data['state_wise_data'][i]['state'] ,
                    "confirmed" :data['state_wise_data'][i]['confirmed'],
                    "deaths" : data['state_wise_data'][i]['deaths'],
                    "recovered": data['state_wise_data'][i]['recovered'],
                }
                state_wise_datas.append(info)
             

            total_state_data =[]
            total_state_data.append(data['state_wise_data'][0]['Total number of confirmed cases in India'])
            total_state_data.append(data['state_wise_data'][0]['Total number of deaths  in India']) 
            total_state_data.append(data['state_wise_data'][0]['Total number of recovered  in India'])

        
        return render_template('county_wise_corona_data.html',country_name=country_name,total_confirmed=total_confirmed,total_active=total_active,total_deaths=total_deaths,total_recovered=total_recovered,labels=labels,total_confirmed_f_graph=total_confirmed_f_graph,total_deaths_f_graph=total_deaths_f_graph,total_recovered_f_graph=total_recovered_f_graph,state_wise_datas=state_wise_datas,total_state_data=total_state_data)
       

              

    return render_template('county_wise_corona_data.html',country_name=country_name,total_confirmed=total_confirmed,total_active=total_active,total_deaths=total_deaths,total_recovered=total_recovered,labels=labels,total_confirmed_f_graph=total_confirmed_f_graph,total_deaths_f_graph=total_deaths_f_graph,total_recovered_f_graph=total_recovered_f_graph)



@app.route('/articles',methods=['GET'])
def trending_news():
    data = db.child(app.config['TABLE_NAME1']).get()
    d_dat = data.val()
  

    return render_template('trending_news.html',trending_news=d_dat.values())

@app.route('/articles/<string:news_name>',methods=['GET'])
def trending_news_detail(news_name):
    
    data = db.child(app.config['TABLE_NAME1']).get()
    d_dat = data.val()
    d_dat = d_dat.values()
    trending_news = None
    for d_dat in d_dat:
        if str(d_dat['title']).strip() == str(news_name):
            trending_news = {
                  "created_at" : d_dat['created_at'],
                  "title" : d_dat['title'],
                  "description" : d_dat['description'],
                  "source" :d_dat['source'],
                  "image" :  d_dat['image'],
                  "tags" : d_dat['tags']  
            }               
    return render_template('trending_news_detail.html',trending_news=trending_news)   
   
       
     

@app.route('/add-article',methods=['GET','POST'])
@is_admin_logged_in
def add_trending_news():
    if request.method == 'POST':
        created_at = str(datetime.now().strftime("%B %d, %Y %I:%M:%S %p"))
        title = request.form['title']
        description = request.form['description']
        source = request.form['source']
        image_name = ''
    
        if 'image' in request.files:
            image = request.files['image']
            img_ext = image.filename.rsplit('.',1)[1].lower()
            image.filename = 'img' + str(datetime.now().date()) + '_' + str(datetime.now().time())+ '.' + img_ext
            image_name = secure_filename(image.filename)
            image.save(os.path.join(app.config['SERVER_FILES_PATH'],image_name))
        else:
            image_name = ''
        tags = request.form['tags']
        data = {
        "created_at" : str(created_at),
        "title" : str(title),
        "description" :str(description),
        "source" :str(source),
        "image" : str(image_name),
        "tags" :str(tags)
        }
        db.child(app.config['TABLE_NAME1']).push(data)

        flash('New news added successfully. Want to add another news?' + Markup("<a href='/add-trending-news'> Click Here.</a>"), 'success')
        return redirect(url_for('trending_news'))
        # return render_template('add_trending_news.html')
    return render_template('add_trending_news.html')    



@app.route("/articles/admin-login",methods=['GET','POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        print("true")
        email = request.form['email']
        password = request.form['password']
      
        data = db.child(app.config['TABLE_NAME2']).get()
        d_dat = data.val()
  
        d_dat = d_dat.values()
  

        email_found = False
        for d_dat in d_dat:
            if d_dat['email']  == email:
                email_found =True
                break
        if email_found == True:

            d_dat = data.val()
            d_dat = d_dat.values()
   
            for d_dat in  d_dat:
     
                if d_dat['email'] == str(email):
                    get_enc_password = str(d_dat['password'])

            if sha256_crypt.verify(password,get_enc_password):
                session['admin_logged_in'] = True
                session['email'] = email

                flash('Login done successfully', 'success')
                return redirect(url_for('add_trending_news'))
            else:
                flash('Incorrect password', 'danger')
                render_template('admin_login.html')
        else:
            flash('Email not found', 'danger')
            render_template('admin_login.html')
     
    return render_template('admin_login.html')


@app.route("/articles/admin-logout",methods=['GET','POST'])
def admin_logout():
    if 'email' in session:
        session.clear()
        flash('Logout done successfully', 'success')
        return redirect(url_for('trending_news'))
    return redirect(url_for('admin_login'))    




