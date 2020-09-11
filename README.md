# Anki-V-to-S-or-A

!!!!!
Warning!  As far as helpful error messages, this add-on is not user friendly.  If you give it the wrong kind of input, it will throw an error and not tell you exactly why.

I'd recommend testing it out with a SMALL set of input instructions first to make sure it's behaving as you want.  And then if it works as you wanted, feel free to give it lots of input instructions (just in the format it desires).

Also, you'll have to add your input to the python file before running the add-on's script (there's no input through Anki itself in this add-on).
!!!!!

Purpose:  You're studying vocab cards that also have sentence and audio cards, but you've learned the vocab,
           so now you want to suspend that vocab card and schedule either the sentence, audio, or both to study instead.
           The sentence card gains the vocab card's due date (or "3 days" if new/learning), and the audio card gets due date + padding.

The code is labeled to help explain things / call out spots where you might need to make changes according to your setup
The code expects a deck with 3 templates, numbered in the following way:  0. Vocab type, 1. Sentence type, 2. Audio type
Expects input of the form:  unique identifier for each triplet of cards, action to take, all on a new line.

For example, (say, typed in a text file):

167, a

291, s

371, b

where a is the command to make an audio card, s a sentence card, b both a sentence and an audio card
 
Copy that input and then paste into the strInput variable in the ###Your Input### section of the code

Also in Your Input, name the deck you want to look thru (if you want to restrict it to a certain deck)

Also, specify what field on your cards is the unique identifier for the triplet.  Example:  Optimized-Voc-Index

In the ####CONSTANTS YOU MAY NEED/WANT TO CHANGE####, make sure your deck templates numbers minus 1 are assigned appropriately

Change other settings if you'd like to

Save the python file, and file should be stored in the right Anki folder and in its own folder called VocabToSnA:

For windows, see:  https://massimmersionapproach.com/table-of-contents/anki/low-key-anki/low-key-anki-summary-and-installation/

For mac, Anki2 > addons21 > VocabToSnA folder

Open Anki (or if already open, close, and then re-open so that it detects the updated file)

Click  "Vocab to Sentence and/or Audio" in the Tools menu on the main screen (ie, Decks screen, not Browse) to use
