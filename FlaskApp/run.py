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
currentPersonCusID = ""


#show live count under info
votingInfo = Voting.find_one({"_id" : "VoteCounts"})
LowVotes = votingInfo['LowVote']
MidVotes = votingInfo['MidVote']
HighVotes = votingInfo['HighVote']

def AddPersonToDB(newPerson):
    People.insert_one(newPerson)
    IncrementMidVoteCount()
    
    
def IncrementMidVoteCount():
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
    # session["ID"] = None
    # session["isMem"] = None
    if not session.get("ID"):
        # if not there in the session then redirect to the login page
        return redirect("/dull")
    return redirect("/news")
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
    if not session.get("ID"):
        # if not there in the session then redirect to the login page
        return redirect("/dull")
    person = People.find_one({"_id" : session["ID"]})
    if not person:
       return
    if person['isMem'] == True:
       currentPersonCusID = person['stripeID']
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
    email = userinfo['email']
    person = People.find_one({Companies.google.value : email})
    if person:
        currentPersonID = person['_id']
        currentPersonisMem = person['isMem']
        currentPersonCusID = person['stripeID']
        currentPersonAweCoin = person['AweCoin']
        session["ID"] = person['_id']
        session["isMem"] = person['isMem']
        # set current person
        # set session data  session["ID"] = returningPerson['_id']
        print(currentPersonID)
        print("here,google auth person found")
        return redirect('/news')
    # makenewperson 
    else:
        newPerson = Person.makeNewPerson(email=email,company=Companies.google.value)
        AddPersonToDB(newPerson=newPerson)
        print("after added new person")
        session["ID"] = newPerson['_id']
        currentPersonID = newPerson['_id']
        session["isMem"] = False
        return redirect('/news')
    
    
    
    
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
    email = profile['email']
    person = People.find_one({Companies.facebook.value : email})
    if person:
        currentPersonID = person['_id']
        # set current person
        # set session data  session["ID"] = returningPerson['_id']
        print(currentPersonID)
        print("here,facebook auth person found")
        return redirect('/news')
    # makenewperson 
    else:
        newPerson = Person.makeNewPerson(email=email,company=Companies.facebook.value)
        People.insert_one(newPerson)
        currentPersonID = newPerson['_id']
        # currentPerson = Person(id=newPerson['_id'],isSubscribed=newPerson['isSubscribed'],AweCoin=newPerson['AweCoin'],paymentID=newPerson['paymentID'])
        print(currentPersonID)
        print("here1")
        return redirect('/news')

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
    email = profile['email']
    person = People.find_one({Companies.twitter.value : email})
    if person:
        currentPersonID = person['_id']
        # set current person
        # set session data  session["ID"] = returningPerson['_id']
        print(currentPersonID)
        print("here,twitter auth person found")
        return redirect('/news')
    # makenewperson 
    else:
        newPerson = Person.makeNewPerson(email=email,company=Companies.twitter.value)
        People.insert_one(newPerson)
        currentPersonID = newPerson['_id']
        # currentPerson = Person(id=newPerson['_id'],isSubscribed=newPerson['isSubscribed'],AweCoin=newPerson['AweCoin'],paymentID=newPerson['paymentID'])
        print(currentPersonID)
        print("here1")
        return redirect('/news')

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
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
    
@app.route('/create_portal_session', methods=['POST','GET'])
def create_portal_session():
    
    session = stripe.billing_portal.Session.create(
    customer=currentPersonID,
    return_url=YOUR_DOMAIN + '/info',
    )
    return redirect(session.url,code=303)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Fulfill the purchase...
        handle_checkout_session(session)

    return "Success", 200

def handle_checkout_session(session):
    # here you should fetch the details from the session and save the relevant information
    # to the database (e.g. associate the user with their subscription)
    customer = stripe.Customer.retrieve(session.customer)
    stripeID = str(customer['id'])
    print(customer)
    print(stripeID)
    print(currentPersonID)
    currentPersonisMem = True
    print(" ^^^ ")
    myquery = { "_id": currentPersonID }
    newvalues = { "$set": { "stripeID": stripeID } }
    newvalues = { "$set": { "isMem": True } }
    People.update_one(myquery, newvalues)
    print(customer)
    return redirect('/news')
    print("Subscription was successful.")
    
@app.route("/success", methods=['GET'])
def success():
    print('cancelled')
    return redirect('/news')
    

@app.route("/cancelled")
def cancelled():
    print('cancelled')
    return redirect('/news')

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

@app.route("/logout")
def logout():
    session["ID"] = None
    session["isMem"] = None
    return redirect('/')

@app.route("/delete")
def delete():
    person = People.find_one({"_id" : session["ID"]})
    if person:
        if person["isMem"] == True:
            # cancel subscription
            return
        if person["hasVoted"] == VotingOptions.middle:
            # subtract vote
            return
        People.delete_one(person)
        session["ID"] = None
        session["isMem"] = None
        return redirect('/')
    return print("not in db")
    

@app.route("/news")
def news():
    if not session.get("ID"):
        # if not there in the session then redirect to the login page
        return redirect("/dull")
    person = People.find_one({"_id" : session["ID"]})
    if not person:
       return redirect('/')
    if person['isMem'] == True:
       currentPersonCusID = person['stripeID']
       return render_template("news.html", visibility="hidden")
   
    return render_template("news.html", visibility="visible")


@app.route("/shop")
def shop():
    
    return render_template('shop.html',Awecoin=currentPersonAweCoin)


if __name__ == '__main__':
    app.run()
