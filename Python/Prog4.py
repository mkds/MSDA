__author__ = 'Mohan Kandaraj'

######################################################################################################################
# *** Wiki Keywords ***
# Enter a topic in the text input and press enter. The program will try to find a wikipage for the topic entered
#   If a wiki page for a topic is found then the program gets the wiki page content and uses part of that
#   content to find keyword (using AlchemyAPI). The top 10 keywords are then displayed in UI.
#
#   If there are more than one wiki page related to the topic entered, then wikipedia returns a disambiguation
#   page where all the related page title are listed. In this case the program displays the keyword on UI so that
#   user can refine the topic
#
#   If there is no wiki page related to topic entered then user is informed so and asked to enter a different topic.
#
#   Test case - "Data Science", "New York", "Intelligence","Fun" - Direct hit (Wiki page for topic is found)
#               "Test","wonder" - ambiguous, display related page titles
#               "Thisisnotfound", "ab123cdef" - No wiki page found. Try different topic
######################################################################################################################

import sys
from bs4 import BeautifulSoup
from alchemyapi import AlchemyAPI
from Tkinter import *
import json
import random



class wiki_keywords:
    """Display UI to get a topic from user and fetch the Wikipedia page for given topic.
     Pass the text from Wikipedia page to AlchemyAPI to get keywords for the topic"""

    #Constants
    WIKI_SEARCH_URL_PREFIX="https://en.wikipedia.org/wiki/Special:Search/"
    RAINBOW = ["red", "orange", "yellow", "green", "indigo", "violet","blue"]
    INITIAL_TOPIC = "Data Science"

    def __init__(self):
        self.root=None
        self.keytext=None
        self.message_label=None
        self.message=None
        self.content=None

        
    def init_ui(self):
        """Construct and display UI"""
        self.root = Tk()
        self.root.title("Wiki Keywords")
        #Instructional or prompt message
        prompt=Label(self.root,text="Type a topic that you like to find keywords for and press enter.\n The keywords from the Wikipedia page for the topic will be displayed")
        prompt.pack()

        #Input for search word
        self.search_word = Entry(self.root,bd=3)
        self.search_word.insert(0, wiki_keywords.INITIAL_TOPIC)
        self.search_word.bind('<KeyRelease-Return>',self.search_action)
        self.search_word.focus_set()
        self.search_word.pack(fill=BOTH)

        #Message to User
        self.message=StringVar()
        self.message_label=Label(self.root,textvariable=self.message,foreground="blue",font=('Arial',10))
        self.message_label.pack()

        #Scroll Bar
        scroll=Scrollbar(self.root)

        #Area to display Words
        self.keytext=Text(self.root,height=20, width=50,yscrollcommand=scroll.set)
        scroll.config(command=self.keytext.yview)
        self.keytext.configure(state=DISABLED)
        self.keytext.pack(side=LEFT)
        scroll.pack(side=RIGHT)

        #Try to display the UI in top middle part of screen
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        x = w/2 - 200
        y = 100
        self.root.geometry("+%d+%d" %  (x, y))
        scroll.pack(side=RIGHT,fill=Y)
        self.search_topic(wiki_keywords.INITIAL_TOPIC)
        self.root.mainloop()


    def search_action(self,event):
        """UI Action for search word input"""
        self.search_topic(event.widget.get().strip())


    def search_topic(self,topic):
        """Search for the topic in Wikipedia"""
        wiki_search_url="%s%s" % (wiki_keywords.WIKI_SEARCH_URL_PREFIX,topic.replace(" ","-"))
        content=self.get_content(wiki_search_url)
        self.process_content(content)


    def read_page(self,url):
        """Read web page given it's URL"""
        import urllib
        try:
            web=urllib.urlopen(url)
            return web.read()
            web.close()
        except Exception, e:
            print "Error:"+str(e)
            sys.exit(e)


    def get_content(self,url="https://en.wikipedia.org/wiki/Data_science"):
        """Read the html page source"""
        self.html_raw=self.read_page(url)
        #print(html_raw)
        self.content=BeautifulSoup(self.html_raw,"html.parser")
        return self.content


    def process_content(self,content):
        """Process the content from Wikipedia"""

        if "Search results" in content.title.text:
            # The topic is not found on wikipedia as wikipedia returned search result instead of a wiki page
            self.message_label.config(foreground="orange")
            self.message.set("The topic entered is not found in wikipeida.\n Try a different topic")
            self.keytext.configure(state=NORMAL)
            self.keytext.delete(1.0,END)
            self.keytext.configure(state=DISABLED)
            return

        if "This disambiguation page lists articles associated with the title" in content.text:
            #There are more than one wiki page related to the topic. Display the page titles for the user so that they can refine their topic
            ambiguous_words_results=[link.find("a",href=re.compile("/wiki/(?!.*:).*")) for link in content.find_all("li", id=None,class_=None)]
            ambiguous_words=[word.text for word in ambiguous_words_results if word is not None]
            self.message_label.config(foreground="blue")
            self.message.set("More than one page related to the topic entered.\n Please refer the list provided below and enter a word from the list")
            self.display_words(ambiguous_words)
        else:
            #We found the wiki page let's extract 3 paragraphs and find keywords
            part_content = " ".join([paragraph.text for paragraph in content.find_all("p",limit=3)])
            keywords=self.get_keywords(content.p.text,10)
            self.message_label.config(foreground="purple")
            self.message.set("Top  Keywords for %s" % self.search_word.get().strip())
            self.display_words(keywords)


    def get_keywords(self,text,limit=100):
        """Get Keywords for the given Text using AlchemyAPI"""
        alchemyapi=AlchemyAPI()
        response = alchemyapi.keywords('text', text, {'sentiment': 1,'maxRetrieve':limit})

        if response['status'] == 'OK':
            for keyword in response['keywords']:
                 print('Keyword: %s ' % keyword['text'].encode('utf-8'))
            return ([keyword['text'] for keyword in response['keywords']])


    def display_words(self,keywords):
        """Display the keywords in UI in rainbow color"""
        self.keytext.configure(state=NORMAL)
        self.keytext.delete(1.0,END)
        for word in keywords:
            color_sch=random.choice(wiki_keywords.RAINBOW)
            self.keytext.tag_configure(color_sch, font=('Georgia', 12),foreground=color_sch)
            self.keytext.insert(END,word+"\n",color_sch)
        self.keytext.configure(state=DISABLED)



if __name__ == "__main__":
    try:
        wiki_keywords().init_ui()
    except Exception, e:
        print "Error:"+str(e)

