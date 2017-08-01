import os
from datetime import datetime
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score

#some properties.
#The extension name was added just for fun.
#It can be changed to anything you want.
#But ensure to make appropriate changes in the consumer API(spring boot) as well

all_models_path = r"D:\kaam\all_models"
ext = ".tupperware"



def train_svm(params):

	try:
		all_of_it = load_files(params['dirPath'], shuffle=True, random_state=None)


		print(params['dirPath'])
		total = len(all_of_it.target)
		print(total)
		num = int(params['train_ratio'] * total)
		print("num ",num)
		train_data = all_of_it.data[:num]
		validation_data = all_of_it.data[num:]
		vect = TfidfVectorizer()
		X_train_tf = vect.fit_transform(train_data)

		clf = svm.SVC(decision_function_shape="ovo", C = params['C_provided'], kernel=params['kernel_provided'], gamma = params['gamma_provided'])
		clf.fit(X_train_tf, all_of_it.target[:num])

		modelFileName = str(datetime.now()).replace(':','-').replace(' ','-').replace('.','-') + ext
		modelFilePath = os.path.join(all_models_path, modelFileName)
		iskodumpkar = {"modelFile": clf, "vectFile": vect, "dirPath" = params['dirPath']}
		joblib.dump(iskodumpkar,modelFilePath)

		###Added code after the successful demo on the last day
		###Uncomment the following lines to use the functionality
		# X_val_tf = loadedVect.transform(validation_data)
		# pred_values = clf.predict(X_val_tf)
		# true_values = all_of_it.target[num:]
		# val_accuracy = accuracy_score(true_values, pred_values)
		###Return the validation accuracy after this

		###Next is determining what the algorithm went wrong with
		###And what did it classify correctly
		# incorrect_indices=[]
		# for i, x in enumerate(true_values):
		# 	if not x == pred_values[i]:
		# 		incorrect_indices.append(i)

		# correct_indices = [i for i,j in enumerate(true_values) if i not in incorrect_indices]

		# with open('incorrect_class_file.csv','wb') as f:
		# 	f.write("Filename , ")
		# 	f.write("True Class , ")
		# 	f.write("Predicted Class\n")
		# 	for i in incorrect_indices:
		# 		f.write(all_of_it.filenames[num+i])
		# 		f.write(",")
		# 		f.write(all_of_it.target_names[true_values[i]])
		# 		f.write(",")
		# 		f.write(all_of_it.target_names[pred_values[i]])
		# 		f.write("\n")
		#
		#
		# with open('correct_class_file.csv','wb') as f:
		# 	f.write("Filename , ")
		# 	f.write("True Class , ")
		# 	f.write("Predicted Class\n")
		# 	for i in correct_indices:
		# 		f.write(all_of_it.filenames[num+i])
		# 		f.write(",")
		# 		f.write(all_of_it.target_names[true_values[i]])
		# 		f.write(",")
		# 		f.write(all_of_it.target_names[pred_values[i]])
		# 		f.write("\n")

	except:
		print("kisine lolwa kiya!!!!!!!!!!!!!!!!!!!!!!!")
		modelFilePath = ""
		modelFileName = ""
	return modelFileName

def test_svm(saved_model, TEST_DIR):
	loadedModelDict = joblib.load(saved_model)

	all_of_it = load_files(loadedModelDict['dirPath'], shuffle=True, random_state=None)
	# all_of_it = load_files(r"D:\kaam\AdditionalParsed", shuffle=True, random_state=None)
	# names = ["AoI", "MC"]

	if not saved_model:
		all_models_that_i_have = [(os.path.getmtime(fn), fn) for fn in os.scandir(all_models_path) if fn.name.endswith(ext)]
		all_models_that_i_have.sort(reverse=True)
		saved_model = all_models_that_i_have[0][1]

	loadedModel = loadedModelDict['modelFile']
	loadedVect = loadedModelDict['vectFile']

	# X_test_tf = loadedVect.transform(test_data)
	# your_score = loadedModel.score(X_test_tf, all_of_it.target[num:])
	# print(your_score)

	res = dict()

	# res['test_accuracy'] = your_score
	print("File:\tClassified as:")
	for home,subdir,files in os.walk(TEST_DIR):
		for file_ in files:
			with open(os.path.join(TEST_DIR, file_)) as f:
				# print(file_ + "\t" + all_of_it.target_names[int(loadedModel.predict(loadedVect.transform([f.read()])))])
				res[file_] = all_of_it.target_names[int(loadedModel.predict(loadedVect.transform([f.read()])))]
				# res[file_] = names[int(loadedModel.predict(loadedVect.transform([f.read()])))]
	resulta = [{"file": i,"cat":"{}".format(j)} for i,j in res.items()]
	return resulta
