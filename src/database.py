# coding: utf-8
import sqlite3
import random
import numpy as np
import io
import cv2


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

def init_database():
	try:
		conn = sqlite3.connect('../eye_database.db',detect_types=sqlite3.PARSE_DECLTYPES)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE Contacts (id INTEGER PRIMARY KEY NOT NULL, nom TEXT NOT NULL, prenom TEXT NOT NULL, keypoint TEXT NOT NULL, descriptor array NOT NULL)")
		conn.commit()	
	except sqlite3.OperationalError:
		print('Erreur la table existe déjà')
	except Exception as e:
		print("Erreur inconnue")
		conn.rollback()
	finally:
		conn.close()

def add(nom,prenom,kp,desc):
	try:
		kp = str(kp)[1:-1]
		id_rand = random.randint(0,10000)
		print(id_rand)
		conn = sqlite3.connect('../eye_database.db',detect_types=sqlite3.PARSE_DECLTYPES)
		cursor = conn.cursor()
		sqlite_insert_with_param = """INSERT INTO 'Contacts'('id','nom', 'prenom', 'keypoint', 'descriptor') VALUES (?,?, ?, ?, ?);"""
		data_tuple = (id_rand,nom,prenom,kp,desc)
		cursor.execute(sqlite_insert_with_param, data_tuple)
		conn.commit()
	except sqlite3.OperationalError:
		print('Erreur lors de l\'ajout des valeurs')
	except Exception as e:
		print(e)
		conn.rollback()
	finally:
		conn.close()

def compare(desc):
	try:
		conn = sqlite3.connect('../eye_database.db',detect_types=sqlite3.PARSE_DECLTYPES)
		cursor = conn.cursor()
		sqlite_select_query = """SELECT * from Contacts"""
		cursor.execute(sqlite_select_query)
		records = cursor.fetchall()
		for row in records:
			print(row[4].size)
			print(desc.size)
			bf = cv2.BFMatcher(cv2.NORM_HAMMING)
			matches = bf.knnMatch(desc,row[4],k=2)
			good = []
			for m,n in matches:
				if m.distance < 0.9*n.distance:
					good.append([m])
            
			print(len(good))
			if len(good)>= 42:
				print(row[1])
				print(row[2])
				break
                        
			
	except sqlite3.OperationalError:
		print('Erreur lors de la récupération des valeurs')
	except Exception as e:
		print("Erreur inconnue")
		conn.rollback()
	finally:
		conn.close()  
