# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py for debugging
from aqt.utils import showInfo
# import all of the Qt GUI library for menu stuff
from aqt.qt import *
# card functions
from anki.cards import Card
#time calc
from datetime import date
import random

################################################################################################################################
# Purpose:  You're studying vocab cards that also have sentence and audio cards, but you've learned the vocab,
#           so now you want to suspend that vocab card and schedule either the sentence, audio, or both to study instead.
#           The sentence card gains the vocab card's due date (or "3 days" if new/learning), and the audio card gets due date + padding.
#
# The code is labeled to help explain things / call out spots where you might need to make changes according to your setup
# The code expects a deck with 3 templates, numbered in the following way:  0. Vocab type, 1. Sentence type, 2. Audio type
# Expects input of the form:  unique identifier for each triplet of cards, action to take, all on a new line:
# Example input (say, typed in a text file):
#           167, a
#           291, s
#           371, b
#			where a is the command to make an audio card, s a sentence card, b both a sentence and an audio card
# 
# Copy that input and then paste into the strInput variable below in the ###Your Input### section of the code
# Also in Your Input, name the deck you want to look thru (if you want to restrict it to a certain deck)
# Also, specify what field on your cards is the unique identifier for the triplet.  Example:  Optimized-Voc-Index
# In the CONSTANTS YOU MAY NEED/WANT TO CHANGE, make sure your deck templates numbers minus 1 are assigned appropriately
# Change other settings if you'd like to
# Save this file, and file should be stored in the right Anki folder and in its own folder called VocabToSnA:
#		For windows, see:  https://massimmersionapproach.com/table-of-contents/anki/low-key-anki/low-key-anki-summary-and-installation/
#		For mac, Anki2 > addons21 > VocabToSnA folder
# Open Anki (or if already open, close, and then re-open so that it detects the updated file)
# Click  "Vocab to Sentence and/or Audio" in the Tools menu on the main screen (ie, Decks screen, not Browse) to use
#
#
#  !!!! NEW !!!  can now stick , r at the end of a line of input to "reset the date" to be within 3 to 6 days of your current today
#  To do this, just sick ', r' at the end of a line of input like this:
#			236, b
#
#  Useful if you're studying a card that's not going to show up until a month or so later, but you want to see the sentence/audio
#  card sooner that than to practice.
#
################################################################################################################################



####CONSTANTS YOU MAY NEED/WANT TO CHANGE####

#Template type, aka card.ord values - YOURS MAY BE DIFFERENT DEPENDING HOW YOUR DECK WAS CONSTRUCTED#
  #To check your template types, go to:
  #Browse > Select your deck (that is, if you're looking at a single deck) > Click "Cards..."
  #At the top of the new window is a "Card Type" field; click that to see all your templates and type numbers
  #SUBTRACT 1 FROM THOSE NUMBERS AND ASSIGN THEM HERE ACCORDINGLY:
VOCAB = 0
SENT = 1
AUDIO = 2

#For scheduling review, PICK HOW MANY DAYS APART YOU WANT A SENTENCE AND AUDIO CARD TO APPEAR#
AUDIOPADDING = 4  # > 0 to prevent a sentence card and an audio card from being scheduled on the same day; 


#####!!!!!!!!!!!!!!!!!!!!!#####
#!!!!					  !!!!#
####	  Your Input 	  #####
#!!!!					  !!!!#
#####!!!!!!!!!!!!!!!!!!!!!#####
parentDeckName = "Learning Cards"  # or "" if no parent deck	# My deck is setup like:  Learning Deck > Core Deck
deckName = "Core 2000"  # or "" if you want to search every card in your profile
uniqueTripletIdentifier = "Optimized-Voc-Index"	#pick whatever unique identify your cards have; normally something like an ID or Index
DATEFIRSTSTARTEDANKI = date(2020, 8, 4)  #Input YOUR start date of using Anki


todaysDate = date(2020, 9, 26)  #Remember to update this along with adding in your new input
deltaDate = todaysDate - DATEFIRSTSTARTEDANKI
numDays = deltaDate.days
#Here's where you'll input those unique identifiers and the actions you want to take on those cards
#NOTE:  MUST Surround with triple quotes (or Python won't treat it as multi-line)
strInput = """532, s
315, s, r"""


####Constants for what input is expected####

#Processing the input  -- assumes input is of the form:  identifiernumber, input code#
STRINGSPLIT = ", "

#input codes#
ONLYAUDIO = "a"
ONLYSENTENCE = "s"
BOTH = "b"


####Code constants that should be left alone####

#queue values#
SUSPENDED = -1
DUE = 2  #(same for type)



####Code####

#so, you want to search for something like "Optimized-Voc-Index:whatever" but with NO SPACES (or crashes)
#Have to use * in place of spaces, then can include deck like this:  "deck:Learning*Cards::Core*2000 Vocabulary-English:car,*a*"
#create string accordingly:
baseSearchStr = '"deck:' + parentDeckName.replace(' ', '*') + "::" + deckName.replace(' ', '*') + '" ' + uniqueTripletIdentifier + ":"

arrInput = strInput.splitlines()

def justDoIt():
	for instruction in arrInput:
		arrPieces = instruction.split(STRINGSPLIT)

		arrTripletCardIds = mw.col.find_cards(baseSearchStr + arrPieces[0]) #unique identifier
		action = arrPieces[1] #instruction code

		#don't know how anki orders the cards it retrieves, so find the vocab card first to get its due date
		vocabCard = ""
		for id in arrTripletCardIds:
			card = mw.col.getCard(id)

			#card template type can be determined thru card.ord:  https://www.juliensobczak.com/write/2016/12/26/anki-scripting.html
			templateType = card.ord

			if templateType == VOCAB:
				vocabCard = card

		if vocabCard.queue == SUSPENDED:  #don't schedule a card based on a suspended vocab card
			continue

		vocabDueDate = numDays + random.randint(3, 6)  #if new or learning or resetting
		if (vocabCard.queue == DUE) and (len(arrPieces)) == 2:
			vocabDueDate = vocabCard.due  #apparently an integer based on whenever you first started Anki?



		#now take action on each card
		for id in arrTripletCardIds:
			card = mw.col.getCard(id)

			templateType = card.ord

			if templateType == SENT and (action == ONLYSENTENCE or action == BOTH):
				card.queue = DUE
				card.type = DUE
				card.due = vocabDueDate
			elif templateType == AUDIO and (action == ONLYAUDIO or action == BOTH):
				card.queue = DUE
				card.type = DUE
				card.due = (vocabDueDate + AUDIOPADDING)
				
			#save changes
			card.flush()

		vocabCard.queue = SUSPENDED  #can't do this in the above loop since python stores vocabCard.due in vocabDueDate as a reference; so, if you suspended this card first in the loop, Anki makes its due value a random int, which the other assignments then use
		vocabCard.flush()
		
	success = 100
	showInfo("Success! (Well, hopefully): %d" % success)

# create a new menu item
action = QAction("Vocab to Sentence and/or Audio", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(justDoIt)
# and add it to the tools menu
mw.form.menuTools.addAction(action)