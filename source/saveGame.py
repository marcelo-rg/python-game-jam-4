import pickle
from cryptography.fernet import Fernet
import os
import variables
cwd = os.getcwd()

class SaveGame:
	def __init__(self, key_file=variables.key_file):
		file_path = os.path.join(cwd, key_file)
		if os.path.exists(file_path):
			with open(file_path, 'rb') as file:
				self.key = file.read()
		else:
			self.key = Fernet.generate_key()
			with open(file_path, 'wb') as file:
				file.write(self.key)
		self.cipher_suite = Fernet(self.key)
		
	def save(self, data, filename):
		file_path = os.path.join(cwd, filename)
		with open(file_path, 'wb') as file:
			encrypted_data = self.cipher_suite.encrypt(pickle.dumps(data))
			file.write(encrypted_data)

	def load(self, filename):
		file_path = os.path.join(cwd, filename)
		if not os.path.exists(file_path):
			print("No save file found!")
		with open(file_path, 'rb') as file:
			encrypted_data = file.read()
			decrypted_data = self.cipher_suite.decrypt(encrypted_data)
			#print(pickle.loads(decrypted_data))
			variables.saved_game_data = pickle.loads(decrypted_data)
