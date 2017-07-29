from flask import Flask, jsonify, make_response, request, render_template, redirect, url_for
from classifier import train_svm, test_svm
app = Flask(__name__)


# classifier="clf_svm"
# classifier = "clf_rf"
# saved_model_path="/path/to/uploaded model"
# train_ratio = 0.8
# test_ratio = 1 - train_ratio
# test_document_path=""
# test_document_raw=""

default_train_dir_path = "D:\kaam\AdditionalParsed"
default_test_dir_path = r"D:\kaam\AdditionalParsedTest"

@app.route('/document-classifier/api/v1/train', methods = ['GET','POST'])
def trainme():
	# classifier abhi mat use karna
	# classifier = request.args.get("classifier") if request.args.get("classifier") else "asdfg"
	dirPath = request.args.get("train_path") or default_train_dir_path
	train_ratio = float(request.args.get("train_ratio")) if request.args.get("train_ratio") else  0.8
	test_ratio = float(f'{1 - train_ratio:.4f}')
	print("Values aa gayi(GET)")
	params = {"dirPath" : dirPath,"train_ratio": train_ratio,"kernel_provided" : "rbf", "C_provided": 10000.0,"gamma_provided" : 0.6}
	print("bhej raha hu")
	modelFilePath = train_svm(params)
	print(modelFilePath+ " bhangar wala\n")
	modelFilePath = modelFilePath.replace("\\",'/')
	print(modelFilePath+ " result aaya")
	# if not modelFilePath:
	# 	return redirect(url_for('nomasti'))
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

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1/fornow', methods=['GET'])
def fornow():
    return jsonify({"the": "proof is in the papers"})




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
