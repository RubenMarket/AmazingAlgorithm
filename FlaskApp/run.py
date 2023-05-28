from flask import Flask, render_template,flash,redirect,jsonify,json,session,url_for,g
from flask.globals import request
from passlib.hash import pbkdf2_sha256
from config import *
from authlib.integrations.flask_client import OAuth
from flask_session import Session
from models import *
import stripe
# path

# cd c:\Users\ruben\OneDrive\Desktop\Utopyism\FlaskApp

# Activate the virtualenv (Windows)
# $ venv\Scripts\activate

# Deactivate the virtualenv (Windows)
# $ deactivate

# check python
#   --> python --version || python3 --version

# get pip
# --> python -m pip install --upgrade pip || python3 -m pip3 install --upgrade pip

# install packages to venv
#   --> pip3 install -r requirements.txt

# run application 
#   --> python run.py


# stop application 
#   --> Ctrl + C

# stripe.api_key = stripe_keys['secret_key']
stripe.api_key = 'sk_test_51MoHqnBRa4aUdrbV65FlMZ8jI7NZLTB1xUROXOjRasxir03V1gHoqjP6KX2U8ZpyxESjzXcbfXkeMXWNT4aRT1UG00XUuPWyPr'
app = Flask(__name__)
app.config['SECRET_KEY'] = secret
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
oauth = OAuth(app)

# 22
# Create a state token to prevent request forgery.
# Store it in the session for later validation.
# session['state'] = state
# Set the client ID, token state, and application name in the HTML while
# serving it.
# response = make_response(
#     render_template('index.html',
#                     CLIENT_ID=CLIENT_ID,
#                     STATE=state,
#                     APPLICATION_NAME=APPLICATION_NAME))
#Database
db = client.Utopyism
People = db.People
Voting = db.Voting
News = db.News
# MainBase = db.MainBase
# News = db.News
YOUR_DOMAIN = 'http://localhost:5000'

currentPersonID = ""
currentPersonisMem = False
currentPersonAweCoin = 0


#show live count under info
votingInfo = Voting.find_one({"_id" : "VoteCounts"})
LowVotes = votingInfo['LowVote']
MidVotes = votingInfo['MidVote']
HighVotes = votingInfo['HighVote']

def AddPerson(newPerson):
    People.insert_one(newPerson)
    global currentPersonID
    global currentPersonisMem
    currentPersonID = newPerson['_id']
    currentPersonisMem = False
    myquery = { "_id": "VoteCounts" }
    newvalues = { "$inc": { "MidVote": +1 } }
    Voting.update_one(myquery, newvalues)

def UpdatePersonVote(currentVotedFor,newVotedFor):
    #midVote is 0, lowVote is -1, highVote is 1
    if currentVotedFor == 0:
        #decrement Mid -1
        return
    if currentVotedFor == -1:
        #decrement low -1
        return
    if currentVotedFor == 1:
        #decrement HIgh -1
        return
    #Set PersonVotedfor to newVotedFor
    if newVotedFor == 0:
        #increment Mid +1
        return
    if newVotedFor == -1:
        #increment low -1
        return
    if newVotedFor == 1:
        #increment HIgh -1
        return
    
    
     
#intial route (not signed in)
@app.route("/",methods = ['POST','GET'])
def index():
    # check for session cookie, if active then log in person
    if not session.get("ID"):
        # if not there in the session then redirect to the login page
        return redirect("/dull")
    return redirect("/home")
    # if request.method == "POST":
    #    username = request.form.get("username")
    #    email = username + companyDomainExtension
    #    password = request.form.get("password")
    #    email_found = users.find_one({"email": email})
    #    if email_found:
    #       email_val = email_found['email']
    #       passwordcheck = email_found['password']
            
    #       if pbkdf2_sha256.verify(password,passwordcheck):
    #          session["logged_in"] = True
    #          session["username"] = username
    #          return redirect(url_for("home", person=username))
    #       else:
    #           print("wrongpass")
    #           message = 'Wrong password'
    #         #   return redirect(url_for("home"))
    #    else:
    #       print("user not in db")
    #       encrypted_Password = pbkdf2_sha256.hash(password)
    #       users.insert_one(newUser(username))
    #       session["logged_in"] = True
    #       session["username"] = username
    #       print("You are successfully logged in")
    #       flash('You are successfully logged in','success')
    #       return redirect(url_for("home", person=username))


#signed in route (signed in home page)
@app.route("/home",methods = ['POST','GET'])
def home():
    
    global currentPersonID
    global currentPersonisMem
    if not session.get("ID"):
        # if not there in the session then redirect to the login page
        return redirect("/dull")
    person = People.find_one({"_id" : session["ID"]})
    if not person:
       return
    if person['isMem'] == True:
       return render_template("home.html", visibility="hidden")
   
    return render_template("home.html", visibility="visible")

@app.route('/google/')
def google():
   
    # Google Oauth Config
    # Get client_id and client_secret from environment variables
    # For developement purpose you can directly put it
    # here inside double quotes
    GOOGLE_CLIENT_ID = googleAuthKeys['ClientID']
    GOOGLE_CLIENT_SECRET = googleAuthKeys['ClientSecret']
     
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
     
    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    userinfo = token['userinfo']
    # token = oauth.google.authorize_access_token()
    # user = oauth.google.parse_id_token(token)
    print(" Google User ", userinfo)
    global currentPersonID
    global currentPersonisMem
    email = userinfo['email']
    person = People.find_one({Companies.google.value : email})
    if person:
        currentPersonID = person['_id']
        currentPersonisMem = person['isMem']
        currentPersonAweCoin = person['AweCoin']
        # set current person
        # set session data  session["ID"] = returningPerson['_id']
        print(currentPersonID)
        print("here,google auth person found")
    # makenewperson 
    else:
        newPerson = Person.makeNewPerson(email=email,company=Companies.google.value)
        AddPerson(newPerson=newPerson)
        print("after added new person")
    session["ID"] = currentPersonID
    session["isMem"] = currentPersonisMem
    return redirect('/home')
    
    
    
@app.route('/facebook/')
def facebook():
   
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = facebookAuthKeys['ClientID']
    FACEBOOK_CLIENT_SECRET = facebookAuthKeys['ClientSecret']
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)

@app.route('/facebook/auth/',methods = ['GET'])
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get(
        'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    global currentPersonID
    email = profile['email']
    person = People.find_one({Companies.facebook.value : email})
    if person:
        currentPersonID = person['_id']
        # set current person
        # set session data  session["ID"] = returningPerson['_id']
        print(currentPersonID)
        print("here,facebook auth person found")
        return redirect('/home')
    # makenewperson 
    else:
        newPerson = Person.makeNewPerson(email=email,company=Companies.facebook.value)
        People.insert_one(newPerson)
        currentPersonID = newPerson['_id']
        # currentPerson = Person(id=newPerson['_id'],isSubscribed=newPerson['isSubscribed'],AweCoin=newPerson['AweCoin'],paymentID=newPerson['paymentID'])
        print(currentPersonID)
        print("here1")
        return redirect('/home')

@app.route('/twitter/')
def twitter():
   
    # Twitter Oauth Config
    TWITTER_CLIENT_ID = twitterAuthKeys['ClientID']
    TWITTER_CLIENT_SECRET = twitterAuthKeys['ClientID']
    oauth.register(
        name='twitter',
        client_id=TWITTER_CLIENT_ID,
        client_secret=TWITTER_CLIENT_SECRET,
        request_token_url='https://api.twitter.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.twitter.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.twitter.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.twitter.com/1.1/',
        client_kwargs=None,
    )
    redirect_uri = url_for('twitter_auth', _external=True)
    return oauth.twitter.authorize_redirect(redirect_uri)
 
@app.route('/twitter/auth/')
def twitter_auth():
    token = oauth.twitter.authorize_access_token()
    resp = oauth.twitter.get('account/verify_credentials.json')
    profile = resp.json()
    print(" Twitter User", profile)
    global currentPersonID
    email = profile['email']
    person = People.find_one({Companies.twitter.value : email})
    if person:
        currentPersonID = person['_id']
        # set current person
        # set session data  session["ID"] = returningPerson['_id']
        print(currentPersonID)
        print("here,twitter auth person found")
        return redirect('/home')
    # makenewperson 
    else:
        newPerson = Person.makeNewPerson(email=email,company=Companies.twitter.value)
        People.insert_one(newPerson)
        currentPersonID = newPerson['_id']
        # currentPerson = Person(id=newPerson['_id'],isSubscribed=newPerson['isSubscribed'],AweCoin=newPerson['AweCoin'],paymentID=newPerson['paymentID'])
        print(currentPersonID)
        print("here1")
        return redirect('/home')

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    global currentPersonID
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': "price_1NCCOEBRa4aUdrbVOadSUFVz",
                    'quantity': 1,
                },
            ],
            mode='subscription',
            client_reference_id=currentPersonID,
            success_url=YOUR_DOMAIN +
            '/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancelled',
        )
        
    except Exception as e:
        print(e)
        return "Server error", 500
    return redirect(checkout_session.url, code=303)
    
@app.route('/create-portal-session', methods=['POST'])
def customer_portal():
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    checkout_session_id = request.form.get('session_id')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = YOUR_DOMAIN

    portalSession = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url,
    )
    return redirect(portalSession.url, code=303)

@app.route("/subscribe")
def subscribe():
    return render_template('subscribe.html')

@app.route('/webhook', methods=['POST'])
def webhook_received():
    # Replace this endpoint secret with your endpoint's unique secret
    # If you are testing with the CLI, find the secret by running 'stripe listen'
    # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
    # at https://dashboard.stripe.com/webhooks
    webhook_secret = 'whsec_12345'
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
    elif event_type == 'customer.subscription.trial_will_end':
        print('Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.updated':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.deleted':
        # handle subscription canceled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print('Subscription canceled: %s', event.id)

    return jsonify({'status': 'success'})

@app.route("/success", methods=['GET'])
def success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    customer = stripe.Customer.retrieve(session.customer)
    customerID = str(customer['id'])
    print(customerID)
    global currentPersonID
    global currentPersonisMem
    print(currentPersonID)
    currentPersonisMem = True
    print(" ^^^ ")
    myquery = { "_id": currentPersonID }
    newvalues = { "$set": { "customerID": customerID } }
    newvalues = { "$set": { "isSubscribed": True } }
    People.update_one(myquery, newvalues)
    print(customer)
    return redirect('/home')

@app.route("/cancelled")
def cancelled():
    print('cancelled')
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/info")
def info():
    return render_template('info.html')

@app.route("/peeple/privacyPolicy")
def privacy_Policy():
    return render_template('PPP.html')

@app.route("/peeple/EULA")
def peeple_EULA():
    return render_template('PEULA.html')

@app.route("/peeple/support")
def peeple_Support():
    return render_template('support.html')

@app.route("/dull")
def dull():
    return render_template('dull.html')

@app.route("/news")
def news():
    
    return render_template('news.html')


@app.route("/shop")
def shop():
    return render_template('shop.html')


if __name__ == '__main__':
    app.run()
