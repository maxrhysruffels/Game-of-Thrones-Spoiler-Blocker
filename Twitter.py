#TWITTER NO SPOILERS V1.0

from tkinter import *
#gui for python
import webbrowser
#library to allow python to open your default browser
import tweepy
#twitter interaction and api handling

complist = []
#list of blocked tweets that can be deleted

def setup():
    consumer_key="ujuYZtAQFRh5HAEA6SRUmbWDJ"
    consumer_secret="af2GbN9OAdbRNbnVhGim7jpl9wO4IhogEgVt3JfcdKoZIi3Cuj"
    #the application's keys to access twitter, kept private for security reasons

    username = input('Please input your twitter username: ')
    #gets the user's twitter handle to access follower count and following list

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    redirect_url = auth.get_authorization_url()
    #sends the app's keys to twitter and gets a url for an authorisation page

    webbrowser.open(redirect_url)
    #opens page for user to allow app access to twitter

    verifier = input('Input PIN given by twitter: ')
    #gets the PIN that twitter gives the user once they have allowed app access

    auth.get_access_token(verifier)
    access_token = auth.access_token
    access_secret = auth.access_token_secret
    #gets the user's access token and secret from twitter

    api = tweepy.API(auth)
    #authorises the app to access twitter's API
    return api, username, verifier

def postlist(api):
    userlist = []
    tweetlist = []
    #lists to contain the tweet's authors and content

    public_tweets = api.home_timeline()
    #accesses user's timeline
    for tweet in public_tweets:
        userlist.append(str(tweet.user.screen_name)+' / '+str(tweet.user.name))
        #grabs the author's username and screen name
        tweetlist.append(str(tweet.text))
        #grabs the tweet's text
    return userlist, tweetlist

def block(tweetlist, blacklist):
    blockedlist = []
    #list to be filled with cencored tweets
    for tweet in tweetlist:
        spoilcount = 0
        #counts spoilers in a tweet
        for spoiler in blacklist:
            if spoiler in tweet:
                #looks for spoilers in each string
                spoilcount += 1
                #ups count by 1 each time a spoiler is found
        if spoilcount > 0:
            blockedlist.append(str(spoilcount) + ' SPOILER(S) BLOCKED')
            #blocks tweet is spoilers are found
        else:
            blockedlist.append(tweet)
            #returns tweet unadultered if there  are no problems
    return blockedlist

def read(name):
    tempstring = ''
    #string that will becomee a list item
    templist = []
    #list of data once read
    file = open(name+'.txt', "r")
    #opens file
    rawdata = file.read()
    #reads file data to variable
    file.close()
    #closes file
    for count in range(0,len(rawdata)):
        #goes through the string one character at a time
        if rawdata[count] == ',' :
            templist.append(tempstring)
            tempstring = ''
            #adds $tempstring to the list everytime a commma is found
        else:
            tempstring += (rawdata[count])
            #forms words in between commas
    return templist

def bigspoiler():
    blacklist = []
    #list to be filled with every spoiler
    episode_list = read('episodes')
    #gets list of episode files to open
    for count in range(0, len(episode_list)):
        tempname = episode_list[count]
        templist = read(tempname)
        #reads every spoiler list in turn
        blacklist += templist
        #adds them all to one big list
        return blacklist
    
def displaypage():
    gridrow = 1
    #the row to place post 
    
    usernamelabel = Label(following, text = username.upper())
    usernamelabel.grid(row = gridrow)
    #places user's screen name at the top of the left frame 

    gridrow +=1
    #adds one to gridrow, meaning the next item will be placed in the row below
    followernotext = str(user.followers_count) + ' Followers'
    followernolabel = Label(following, text = followernotext)
    followernolabel.grid(row = gridrow)
    #displays how many followers the user has in the left frame

    gridrow +=1
    PINtext = 'KEY: ' + str(verifier)
    PINlabel = Label(following, text = PINtext)
    PINlabel.grid(row = gridrow)
    #displays the PIN that the user used to authorise the application in the row blow

    for x in range(3):
        gridrow += 1
        spacelabel = Label(following, text = ' ')
        spacelabel.grid(row = gridrow)
        #leaves a 3 line gap, by filling 3 rows of the grid with blank labels

    for friend in user.friends():
        #only displaays a limited number for some reason
        gridrow += 1
        followerlabel = Label(following, text = friend.screen_name)
        followerlabel.grid(row = gridrow)
        #displays information about who the user is following in sequencial rows
    

def displaypost():
    global complist
    #gets complist in to add tweets to it
    for x in range(0, len(userlist)):
        #compiling and displaying tweets
        try:
            #tkinter cant display emojis, if a post contains one, my program will post an error instead
            comptweet = userlist[x] + '\n ' + blockedlist[x]
            #combining user and blocked tweet text to make a complete tweet
            complist.append(Label(postframe, text = comptweet, bg = 'white', relief = RIDGE))
            #adds the label as a list item, this allows deletion
            complist[x].pack(ipady = 5, pady = 5, padx = 10, fill = X)
            #packs it a set distance away from any other object
        except:
            comptweet = userlist[x] + '\n \n ' + '~~~ ERROR DISPLAYING POST, CONTAINS EMOJI ~~~'
            #replaces tweet text with an emoji error message
            complist.append(Label(postframe, text = comptweet, bg = 'white', relief = RIDGE))
            complist[x].pack(ipady = 5, pady = 5, padx = 10, fill = X)
            #acts the same as the 'try' command in every other way

def unblock():
    global complist
    #fetches complist in order to delete all of it's posts
    for i in range(0, len(complist)):
        complist[i].destroy()
        #systematically destroys all of the blocked posts
    for x in range(0, len(userlist)):
        #goes back over what went on in the display post algorithm
        try:
            comptweet = userlist[x] + '\n ' + tweetlist[x]
            #uses tweetlist instead of blockedlist to display uncensored posts
            tweet0 = Label(postframe, text = comptweet, bg = 'white', relief = RIDGE)
            #uses a static variable instead of a list to store labels, deletion is not required
            tweet0.pack(ipady = 5, pady = 5, padx = 10, fill = X)
            #packs as before
        except:
            comptweet = userlist[x] + '\n \n ' + '~~~ ERROR DISPLAYING POST, CONTAINS EMOJI ~~~'
            #handles emoji in the same way
            tweet0 = Label(postframe, text = comptweet, bg = 'white', relief = RIDGE)
            #again uses a static variable, I found reassigning the list items caused lots of errors
            tweet0.pack(ipady = 5, pady = 5, padx = 10, fill = X)


def onframeconfigure(event):
    canvas.configure(scrollregion = canvas.bbox('all'))
    #binds canvas and scrollbar together

def spacecorrect(list1):
    list2 = []
    #list to add space corrected tweets
    for i in range(0, len(list1)):
        post = list1[i]
        #singles out one tweet at a time
        n = 0
        #number to offset each line by, due to \n taking up 2 characters
        for x in range(0,len(post)):
            if x % 50 == 0:
                n2 = x + n
                #adds offset to place to create an index to insert the new line
                post1 = post[:n2]
                post2 = post[n2:]
                #splits $post into 2 strings around the correct index
                post = post1 + '\n' + post2
                #inserts new line tag
                n += 2
                #adds 2 to offset
        list2.append(post)
        #note: this adds a new line before each post
    return list2
                   
api, username, verifier = setup()
#get's the user's username and api, verifies the app to work with twitter
user = api.get_user(username)
#gets public api for user - who follows them, number of followers, etc.
userlist, tweetlist = postlist(api)
#gets list of tweet content and people who posteed the tweets
blacklist = bigspoiler()
#collects all spoiler keywords into one list
blockedlist = block(tweetlist, blacklist)
#blocks spoilers from list of tweets, keeps original list unchanged, notes index of changes
blockedlist = spacecorrect(blockedlist)
tweetlist = spacecorrect(tweetlist)
#corrects spacing of tweets, so the text doesnt spill over the edge of a label


window = Tk()
#sets up main window
window.geometry("600x600+1+1")
#set's the window's default geometry to 600x600

mainframe = Frame(relief = RIDGE, borderwidth = 1)
#sets up parent frame of $following and both buttons
mainframe.pack(fill = BOTH, expand = 1)
#places it into the window to fill it up

following = Frame(mainframe, relief = RIDGE, width = 150)
#creates frame to put user information
following.pack(side = LEFT, fill = Y)
#places it into the far left of $mainframe, filling up the frame vertically
 
frame2 = Frame(mainframe, relief = RIDGE, background = '#FFFFFF')
#creates parent frame for the canvas - needed to work with a scrollbar
frame2.pack(side = TOP, fill = BOTH, expand = True)
#packs it to fill up the rest of $mainframe

canvas=Canvas(frame2, bg='gray')
#creates canvas
bar = Scrollbar(frame2, orient = VERTICAL)
#creates scrollbar
bar.config(command=canvas.yview)
#configures scrollbar to change the view of $canvas, on the y axis
canvas.config(yscrollcommand=bar.set)
#configures $canvas to change it's y view with the scrollbar
bar.pack(side = RIGHT, fill = Y)
#packs the scrollbar to the right of $frame2, filling up it's height
canvas.bind('<Configure>',onframeconfigure)
#binds the scrollbar to the canvas
canvas.pack(fill = BOTH, expand = True)
#packs the canvas to fill up any remaining space in $frame2
postframe = Frame(canvas, background = '#cceeff')
#sets up frame foor the tweet labels to go
canvas.create_window((0,0), window=postframe, anchor = NW, width=427)
#creates $postframe in the canvas to allow scrolling

unblockButton = Button(text="Unblock All", font = 'Helvetica 10', command=unblock)
#creates button to unblock all spoilers when pressed
unblockButton.pack(side = RIGHT, padx = 5, pady = 5)
#packs it inside main window, to the right

displaypage()
#displays every bit of content that isnt a tweet on the page
displaypost()
#displays tweets on the page

window.mainloop()
#loops the page
