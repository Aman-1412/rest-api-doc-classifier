import os
from datetime import datetime
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.externals import joblib



all_models_path = r"D:\kaam\all_models"
ext = ".tupperware"


# print(dir(all_of_it))
# print(all_of_it.target_names)
# print(len(all_of_it.data))
# print(all_of_it.target[:10])
# all_of_it.filenames[:5]
# print(all_of_it.data[0])
# modelFile = "20-news-svm.sav"



def train_svm(params):
#TODOS: pass a dictionary you nut
	try:
		all_of_it = load_files(params['dirPath'], shuffle=True, random_state=None)
		# all_of_it.target_names
		print(params['dirPath'])
		total = len(all_of_it.target)
		print(total)
		num = int(params['train_ratio'] * total)
		print("num ",num)
		train_data = all_of_it.data[:num]
		test_data = all_of_it.data[num:]
		vect = TfidfVectorizer()
		X_train_tf = vect.fit_transform(train_data)
	    # print(X_train_tf.shape)

		clf = svm.SVC(decision_function_shape="ovo", C = params['C_provided'], kernel=params['kernel_provided'], gamma = params['gamma_provided'])
		clf.fit(X_train_tf, all_of_it.target[:num])

		modelFileName = str(datetime.now()).replace(':','-').replace(' ','-').replace('.','-') + ext

		modelFilePath = os.path.join(all_models_path, modelFileName)
		iskodumpkar = {"modelFile": clf, "vectFile": vect}
		joblib.dump(iskodumpkar,modelFilePath)
		# vectFilePath = modelFilePath.split(".")[0] + ".vect"
		# joblib.dump(clf,modelFilePath)
		# joblib.dump(vect, vectFilePath)
		#TODO dict bana ke dono ek mein daal
		#ext TUPPERWARE
	except:
		print("kisine lolwa kiya!!!!!!!!!!!!!!!!!!!!!!!")
		modelFilePath = ""
		modelFileName = ""
	return modelFileName

def test_svm(saved_model, TEST_DIR):
# Baadme karna. Pehle training
	all_of_it = load_files(r"D:\kaam\AdditionalParsed", shuffle=True, random_state=None)
	# names = ["AoI", "MC"]
	# print(X_test_tf.shape)
	if not saved_model:
		all_models_that_i_have = [(os.path.getmtime(fn), fn) for fn in os.scandir(all_models_path) if fn.name.endswith(ext)]
		all_models_that_i_have.sort(reverse=True)
		saved_model = all_models_that_i_have[0][1]
	# saved_vect_file = saved_model.name.split(".")[0] + ".vect"
	# saved_vect = os.path.join(all_models_path, saved_vect_file)
	# loadedVect = joblib.load(saved_vect)
	loadedModelDict = joblib.load(saved_model)
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
