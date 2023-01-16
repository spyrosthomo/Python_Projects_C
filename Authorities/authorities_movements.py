# 21.3 Tελική εργασία: Ανάκτηση δεδομένων από τη diavgeia.gov.gr
# Πρότυπο λύσης

import re
import urllib.request
import urllib.error

arxes = {}
tonoi =['αά','εέ','οό','ωώ','ιί','ηή','υύ']


def process_feed(filename): #3 μονάδες *
    '''
    συνάρτηση που ανοίγει το αρχείο με το rss feed και 
    τυπώνει την ημερομηνία και τους τίτλους των αναρτήσεων που περιέχει.
    Xρησιμοποιήστε regular expressions 
    '''
    #tag_pattern = r'<'+tag+r'\b[^>]*>(.*?)</'+tag+r'>'
    tag_date = 'lastBuildDate'
    tag_pattern_date = r'<'+tag_date+r'\b[^>]*>(.*?)</'+tag_date+r'>'
    tag_title = 'title'
    tag_pattern_title = r'<'+tag_title+r'\b[^>]*>(.*?)</'+tag_title+r'>'
    with open(filename , 'r' , encoding='utf-8') as f :
        rss_f = f.read().replace('\n','')
        
        #Εύρεση Ημερομηνιας
        
        in_date_tag = re.findall(tag_pattern_date , rss_f , re.I)
        d = in_date_tag[0].split(' ')
        date = ' '.join(d[:4])
        
        #Εύρεση τίτλων αναρτήσεων 
        
        in_title_tag = re.findall(tag_pattern_title, rss_f , re.I)[1:] #Βάζω απο 1 εως το τέλος ([1:]) γιατό μέσα στο πρώτο title tag  περιέχεται η φράση 'Διαύγεια RSS - ΥΠΟΥΡΓΕΙΟ ΔΙΚΑΙΟΣΥΝΗΣ'

        #Εκτύπωση ημερομηνίας και τίτλψν αναρτήσεων
        print(process_date(date))
        c = 0
        for i in in_title_tag :
            c+=1
            print(str(c)+'.\t\t'+i.replace(';','  ').upper()) 


def rss_feed(url): #3 μονάδες *
    '''
    Άνοιγμα του rss feed,
    :param url: η διεύθυνση του rss feed.
    Αυτή η συνάρτηση δημιουργεί ένα αρχείο
    με τα περιεχόμενα του rss_feed με όνομα
    την διεύθυνση του rss feed.
    Καλεί την συνάρτηση process_feed
    η οποία επιλέγει και τυπώνει περιεχόμενο
    Προσπαθήστε να κάνετε try/except τα exceptions
    HTTPError και URLError.
    '''
    #σύμφωνα με την ανακοίνωση της διαύγειας τα rss feeds είναι στο ίδιο url/rss
    url+=r'/rss'
    try:
        req = urllib.request.Request(url) 
        with urllib.request.urlopen(req) as response:
            char_set = response.headers.get_content_charset()
            rss = response.read().decode(char_set)
    except urllib.errorr.HTTPError as e :
        print("Σφάλμα HTTPError: ",e.code)
    except urllib.error.URLError as e :
        print('Αποτυχία σύνδεσης στον server\nΑιτία: ' ,  e.reason )
    else:
        rss=rss.replace('\n','')
        filename = url.replace(':','=').replace('.','_').replace('/','-')  # αντικαθιστω τα συμβολα ':',.' και'/' γιατι δεν ειναι αποδεκτα στην ονομασια των αρχειων
        with open(filename ,'w',encoding='utf-8') as f:
            to_file = rss
            f.write(to_file)
            process_feed(filename)

def process_date(date): #2 μονάδες
    '''
    η συνάρτηση διαμορφώνει την ελληνική ημερομηνία του rss feed:
    Στο rss αρχείο η ημερομηνία είναι της μορφής: Wed, 14 Jun 2017 17:21:16 GMT
    Θα πρέπει να διαμορφώνεται σε ελληνική ημερομηνία, πχ: Τετ, 14 Ιουν 2017
    :param date:
    :return: η ελληνική ημερομηνία
    '''
    days = {'Mon':'Δευ', 'Tue':'Τρί' , 'Wed':'Τετ' , 'Thu':'Πεμ' ,'Fri':'Παρ' , 'Sat':'Σαβ', 'Sun':'Κυρ'}
    months = {'Jan':'Ιαν' , 'Feb':'Φεβ' , 'Mar':'Μαρ' , 'Apr':'Απρ' ,'May':'Μαϊ' ,'Jun':'Ιουν' , 'Jul':'Ιουλ' ,'Aug':'Αυγ' ,'Sep':'Σεπ' ,'Oct':'Οκτ' , 'Nov':'Νοε' ,'Dec': 'Δεκ'}
    for c in date.split() :
        if c in months :
            date=date.replace(c,months[c])
    d=date.split(', ')
    for c in d :
        if c in days :
            d[0]= days[c]
    date_gr=', '.join(d) 
    return date_gr



   
    

def search_arxes(arxh): #2 μονάδες
    '''
    Αναζήτηση ονόματος Αρχής που ταιριάζει στα κριτήρια του χρήστη
    '''
    starts=''
    arx=[]
    try:
        with open('500arxes.csv','r',encoding='utf-8') as f :
            starts = f.read()
    except IOError as e :
        print(e)
    pattern = '.*'+arxh+'.*'
    arx = re.findall(pattern, starts, re.I)

    return arx


def load_arxes(): #2 μονάδες
    '''
    φορτώνει τις αρχές στο λεξικό arxes{}
    '''
    with open('500arxes.csv','r',encoding='utf-8') as f:
        text = f.read()
        pattern_name = r'(.*);'
        pattern_url = r';(.*)\n'
        onoma = re.findall(pattern_name , text)
        ur = re.findall(pattern_url ,text)
        i=0
        for c in range(0,551) : 
            arxes[onoma[i]] = ur[i]
            i+=1


######### main ###############
'''
το κυρίως πρόγραμμα διαχειρίζεται την αλληλεπίδραση με τον χρήστη
'''
load_arxes()
while True :
    arxh = input(50*"^"+"\nΟΝΟΜΑ ΑΡΧΗΣ:(τουλάχιστον 3 χαρακτήρες), ? για λίστα:")
    if arxh == '':
        break
    elif arxh == "?": # παρουσιάζει τα ονόματα των αρχών
        for k,v in arxes.items():
            print (k,v)
    elif len(arxh) >= 3 :
        # αναζητάει όνομα αρχής που ταιριάζει στα κριτήρια του χρήστη
        result = search_arxes(arxh)
        for r in result:
            print (result.index(r)+1, r  )   #, arxes[r]) , βγαζω αυτο το κομματι εκτος προγραμματος καθοτι δημιουργει καποιο προβλημα στην εκτελεση
        while result:
            epilogh = input("ΕΠΙΛΟΓΗ....")
            if epilogh == '': break
            elif epilogh.isdigit() and 0<int(epilogh)<len(result)+1:
                epilogh = int(epilogh)
                url = arxes[result[epilogh-1].split(';')[0]]
                print(url)
                # καλεί τη συνάρτηση που φορτώνει το αρχείο rss:
                rss_feed(url)
            else: continue
    else :
        continue
