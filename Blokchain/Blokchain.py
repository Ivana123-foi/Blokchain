import functools
import hashlib
import json
from collections import OrderedDict

#ovo je globalna varijabla koja se ne smije mijenjati 
MINING_REWARD = 10

genesis_block={
	'prosli_hash': '',
	'index': 0,
	'transakcija': [],
	'dokaz': 100
	}

blockchain = [genesis_block]
otvorene_transakcije=[]
owner = 'Ivana'
participants = {'Ivana'}

def valid_dokaz (transakcija, zadnji_hash, dokaz):
	pogodak = (str(transakcija) + str(zadnji_hash) + str(dokaz)).encode()
	pogodak_hash = hashlib.sha256(pogodak).hexdigest()
	#print(pogodak_hash)
	return pogodak_hash[0:2] == '00'

def dokaz_rada():
	zadnji_blok= blockchain[-1]
	zadnji_hash = hash_block(zadnji_blok)
	dokaz=0
	while not valid_dokaz(otvorene_transakcije, zadnji_hash, dokaz):
		dokaz+=1
	return dokaz


def hash_block(block):
	return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

def get_balance(participant):
	tx_sender=[[transakcija['Kolicina'] for transakcija in block['transakcija'] if transakcija['Posiljatelj'] == participant] for block in blockchain]
	open_tx_sender =[ transakcija['Kolicina'] for transakcija in otvorene_transakcije if transakcija['Posiljatelj'] == participant ]
	tx_sender.append(open_tx_sender)

	amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum+0, tx_sender, 0)
	
	tx_recipient=[[transakcija['Kolicina'] for transakcija in block['transakcija'] if transakcija['Primatelj'] == participant] for block in blockchain]
	amount_primljena = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt)>0 else tx_sum+0, tx_recipient, 0)
	
	
	return amount_primljena-amount_sent


#rudarenje bloka u blokchain
def mine_block():

	zadnji_block=blockchain[-1]
	hashed_block = hash_block(zadnji_block)

	dokaz=dokaz_rada()

	transakcija_nagrade = OrderedDict(
		[('Posiljatelj', 'MINING'), ('Primatelj',owner),('Kolicina', MINING_REWARD)]
		)

	kopirane_transakcije = otvorene_transakcije[:]
	kopirane_transakcije.append(transakcija_nagrade)

	block = {
		'prosli_hash': hashed_block,
		'index': len(blockchain),
		'transakcija': kopirane_transakcije,
		'dokaz': dokaz
		}
	blockchain.append(block)
	return True

def get_zadnju_blockchain_vrijednost():
	
	if len(blockchain) < 1:
		return None

	return blockchain[-1]


def dodaj_transakciju(posiljatelj, primatelj, kolicina=1.0):
	posiljatelj=owner

	#transakcija={
	#	'Posiljatelj':posiljatelj, 
	#	'Primatelj':primatelj, 
	#	'Kolicina': kolicina 
	#	}

	transakcija = OrderedDict(
		[('Posiljatelj',posiljatelj), ('Primatelj',primatelj),('Kolicina', kolicina)]
		)

	if provjera_transakcij(transakcija):
		otvorene_transakcije.append(transakcija)
		participants.add(posiljatelj)
		participants.add(primatelj)
		return True
	return False

def get_vrijednost_transakcije():

	Primatelj_osoba= input('Unesite primatelja transakcije:')
	vrijednost_korisnika= float(input('Vrijednost vaše transakcije: '))
	return Primatelj_osoba, vrijednost_korisnika

def get_izbor_korisnika():
	vrijednost_korisnika=input('Vaš izbor je:')
	return vrijednost_korisnika

def print_blockchain_elemente():
	for block in blockchain:
		print('Outputting Block')
		print(block) 

bool_provjera=True

#Radimo provjeru lanca ako je tocan, ako je manipuliran vrati false
def provjeri_lanac():
	for (index, block) in enumerate(blockchain):
		if index == 0:
			continue
		if block['prosli_hash'] != hash_block(blockchain[index-1]):
			return False
		if not valid_dokaz(block['transakcija'][:-1], block['prosli_hash'], block['dokaz']):
			print('Dokaz nije valjan!')
			return False
	return True

#Provjera transakcije
def provjera_transakcij(transaction):
	sender_balance=get_balance(transaction['Posiljatelj'])
	if sender_balance >= transaction['Kolicina']:
		return True
	else:
		return False

def provjera_transakcija():
	return all([provjera_transakcij(transak) for transak in otvorene_transakcije])



while bool_provjera:
	print('Molim vas odaberite(1/2/3/...):')
	print('1: Dodaj novu vrijednost transakcije!')
	print('2: Ispis svih vrijednosti! ')
	print('3: Ispis participants! ')
	print('4: Mine a block! ')	
	print('5: Provjera transakcije! ')	
	print('h: Manipulacija! ')	
	print('q: Izadi! ')

	izbor_korisnika=get_izbor_korisnika()

	if izbor_korisnika == '1':
		K_transakcije = get_vrijednost_transakcije()
		primatelj_v, kolicina_v=K_transakcije

		if dodaj_transakciju(owner, primatelj_v, kolicina=kolicina_v ):
			print('Dodana transakcija')
		else:
			print('Transakcija nije bila uspjesna!')

	elif izbor_korisnika == '2':
		print_blockchain_elemente()

	elif izbor_korisnika == '3':
		print(participants)
		
	elif izbor_korisnika == '4':
		if mine_block():
			otvorene_transakcije=[]

	elif izbor_korisnika == '5':
		if provjera_transakcija():
			print('Sve transakcije su dobre!')
		else:
			print('Nisu dobre transakcije!')
		
	elif izbor_korisnika == 'h':
		if len(blockchain)>=1:
			blockchain[0] = {
				'prosli_hash': '',
				'index': 0,
				'transakcija': [{'Posiljatelj':'Chris', 'Primatelj': 'Max', 'Kolicina':100.0}]
				}

	elif izbor_korisnika == 'q':
		break
	
	else:
		print('Niste dobro izabrali, molim vas ponovite!')

	if not provjeri_lanac():
		print_blockchain_elemente()
		print('Izlaz, manipulacija')
		break

	print('Stanje racuna od {}: {:6.2f}'.format('Ivana', get_balance('Ivana')))
else:
	print('Hvala što ste koristili našu aplikaciju!')






