#EPISODE PICKER V1.0

import urllib.request
#url handling
import sys
#system communication to kill program if url is incorrect

ignore = ['a', 'of', 'and', 'the', 'to','s']
#list of words that shouldnt get capitalised; 's' makes sure that 's doesnt get capitalised
wikipedia1 = 'https://en.wikipedia.org/w/api.php?format=json&action=query&titles='
#first half of wikipedia link
wikipedia2 = '&prop=revisions&rvprop=content'
#second half
spoiler_list = []
#list that spoilers will be saved into

def url(name):
    #setting up all strings that go into the url and getting correct capitalisation
    name = name.replace("'"," ' ")
    #makes phrases after apostrophes act as new words, stops title() from capitalising 's
    name_list = name.split(' ')
    #splits string into individual words
    for count in range(0,len(name_list)):
        if name_list[count] in ignore:
            #checks that words need capitalisation
            if count == 0:
                #always capitalises the first word in a title
                name_list[count] = name_list[count].title()
        else:
            name_list[count] = name_list[count].title()
            #capitalises nouns
    name = " ".join(name_list)
    #joins list back into a string
    
    name = name.replace(" ' ","'")
    #getting rid of spaces around apostrophes, makes outputting message look nice
    print('Looking for episode named '+ name + ', please wait.')
    print('...')
    #lets the user know that it is about to access wikipedia
    name = name.replace("'", "%27")
    #url addresses cannot use apostrophes, they're replaced with %27
    name = name.replace(' ','_')
    #url addresses use _ instead of spaces
    address = wikipedia1 + name + wikipedia2
    #creates a full url to open, to search for spoilers
    return address

def get(url):
    spoilerpage = urllib.request.urlopen(url)
    #requesting the page html code
    content = str(spoilerpage.read())
    #saves webpage contents to a string
    return content

def plot(content):
    #isolating the plot
    try:
        #this will show up whether the user input a correct episode name
        content = content[content.index("Plot"):content.index("==Production==")]
        #deletes everything except plot, these are the tags where the plot of the episode lies
        content = content.strip('\\n')
        #preliminary stripping of html formatting tags
        print('Extracting Plot.')
        print('...')
        #lets the user know that the page was succesfully found
        return content
    except ValueError:
        #occurs if a 404 page not found error occurs
        print("Page not found!")
        #if it cant find 'Plot' or '==Production=='
        print('Aborting attempt!')
        #lets user know the program is aborting
        sys.exit(0)

def listify(content):
    rawlist = []
    #list that spoilers will be saved into
    plotlist = content.split(' ')
    #splits the plot into a list
    for count in range(0, len(plotlist)) :
        if plotlist[count] == plotlist[count].title() :
            #Checks if the word starts with a capital letter, looking for proper nouns
            rawlist.append(plotlist[count].strip("\\'").strip('.').strip('(')
                .strip(')').strip('[').strip(']').strip(',').strip('([[')
                .strip(']])').strip('\\"').strip(']]\\"').strip('\\"[[').lower())
            #very inneficient way to remove unwanted characters but very simple
    return rawlist

def cleanup(raw):
    for count in range(0, len(raw)) :
        if raw[count] not in spoiler_list :
            #checks for repitition
            spoiler_list.append(raw[count].lower())
            #adds items that havent yet appeared in the list, to the list
    top = top100()
    #gets the 100 most common words from it's procedure
    for i in range(0, len(top)):
        if top[i] in spoiler_list:
            #checks the list for any of these words
            spoiler_list.remove(top[i])
            #removes them if found
    return spoiler_list

def save(spoiler_list, name, update):
    if update == True:
        #checks whether this is an episode plot or name
        episode_list = readepisodes()
        #reads episode list, to avoid duplicates and because the write command wipes the file
        if name in episode_list:
            return None
        #aborts procedure if a duplicate name is found
        else:
            episode_list.append(name)
            #adds the episode name to the list of episodes
            name = 'episodes'
            spoiler_list = episode_list
            #sets the name and list so that the rest of this function works with episode lists or spoiler lists
    tempstring = ''
    #string to write to the text file
    for count in range(0, len(spoiler_list)):
        #basically does the reverse of the readepisodes() function
        tempstring += spoiler_list[count]
        tempstring += ','
        #makes the list distinguishable for the function that opens the text document
    file = open(name + '.txt', 'w')
    #names the text document after the name input by the user
    file.write(tempstring)
    file.close()
    #saves and closes the text file
    print('Saved!')
    #lets user know the saving is successful

def readepisodes():
    tempepisode = ''
    #episode name, added character by character
    templist = []
    #list where episode names are stored
    file = open('episodes.txt', "r")
    #opens a ffile to be read
    rawdata = file.read()
    #reads file to variable
    file.close()
    #closes file to save memory
    for count in range(0,len(rawdata)):
        if rawdata[count] == ',' :
            templist.append(tempepisode)
            tempepisode = ''
            #adds content of $tempepisode to $templist everytime a comma is read
        else:
            tempepisode += (rawdata[count])
            #adds character bing examined to the end of $tempepisode otherwise
    return templist

def top100():
    top = ['the','be','to','of','and','a','in','that','have','i',
           'it','for','not','on','with','he','as','you','do','at',
           'this','but','his','by','from','they','we','say','her','she',
           'or','an','will','my','one','all','would','there','their','what',
           'so','up','out','if','about','who','get','which','go','me',
           'when','make','can','like','time','no','just','him','know','take',
           'people','into','year','your','good','some','could','them','see','other',
           'than','then','now','loook','only','come','its','over','think','also',
           'back','after','use','two','how','our','work','first','well','way',
           'even','new','want','because','any','these','give','day','most','us']
    #100 most common words in the english language
    return top
           
name = input('Enter Episode Title')
#user names an episode
name = name.lower()
#this makes the string easier to handle

save(cleanup(listify(plot(get(url(name))))), name, False)
#saves list of spoilers generated by the functions, in a file called $name
save(name,name,True)
#saves $name into episode list
