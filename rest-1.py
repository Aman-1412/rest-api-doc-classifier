from flask import Flask, jsonify, make_response, request, render_template, redirect, url_for
from classifier import train_svm, test_svm
app = Flask(__name__)


#Declare some properties

default_train_dir_path = "D:\kaam\AdditionalParsed"
default_test_dir_path = r"D:\kaam\AdditionalParsedTest"

@app.route('/document-classifier/api/v1/train', methods = ['GET','POST'])
def trainme():

	dirPath = request.args.get("train_path") or default_train_dir_path
	train_ratio = float(request.args.get("train_ratio")) if request.args.get("train_ratio") else  0.8
	# test_ratio = float(f'{1 - train_ratio:.4f}')
	test_ratio = round(1 - train_ratio,2)
	print("Values aa gayi(GET)")
	params = {"dirPath" : dirPath,"train_ratio": train_ratio,"kernel_provided" : "rbf", "C_provided": 10000.0,"gamma_provided" : 0.6}
	print("bhej raha hu")
	modelFilePath = train_svm(params)
	print(modelFilePath+ " bhangar wala\n")
	modelFilePath = modelFilePath.replace("\\",'/')
	print(modelFilePath+ " result aaya")
	return (jsonify({"modelStoredAt" : modelFilePath}))

@app.route('/document-classifier/api/v1/test', methods = ['GET','POST'])
def testme():
	test_document_path = request.args.get("test_document_path") or default_test_dir_path
	saved_model_path = request.args.get("saved_model_path") # if request.args.get("saved_model_path") else "/default/path/here.sav"
	# test_document_raw = request.form['test_document_raw']
	# with open("D:\kaam\AdditionalParsedTest\AoI1.txt") as f:
	# 	test_document_raw = request.args.get("test_document_raw") if request.args.get("test_document_path") else f.read()

	result = test_svm(saved_model_path, test_document_path)
	print(result)
	return jsonify(result)


@app.route('/document-classifier/api/badcall')
def nomasti():
	return jsonify({"isError" : "True"})

@app.route('/')
def index():
    return("Hola! Secret api services available here on request")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
