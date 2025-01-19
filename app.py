from flask import Flask, request, jsonify
from flask_cors import CORS

from codeManager import codeManager

app = Flask(__name__)
CORS(app)

@app.route('/code/addNumsCode', methods=['POST'])
def addNumsCode():
    try:
        data = request.json
        type = str(data.get('type','qhc_a'))
        nums = int(data.get('nums', 10))

        cm = codeManager()
        result = cm.addNumsCode(nums, type)
        return jsonify(result),200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/getCode', methods=['GET'])
def getCode():
    try:
        ip = request.remote_addr
        cm = codeManager()
        user_agent = request.headers.get('User-Agent')
        print(f"User-Agent: {user_agent}")
        result = cm.getCode(user_agent)
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/buyCode', methods=['POST'])
def buyCode():
    try:
        data = request.json
        tx_hash = str(data.get('tx_hash','0x0000000000000000000000000000000000000000000000000000000000000000'))
        sender = str(data.get('sender','0x0000000000000000000000000000000000000'))
        amount = float(data.get('amount',0.001))
        print(f"hash:{tx_hash}")
        print(f"sender:{sender}")
        print(f"amount:{amount}")

        cm = codeManager()
        result = cm.buyCode(tx_hash,sender,amount)
        print(jsonify(result))
        return jsonify(result),200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/useCode', methods=['POST'])
def useCode():
    try:
        data = request.json
        code = str(data.get('code', 'ABCDE'))
        address = str(data.get('address', '0x000000000000000000000000'))

        cm = codeManager()
        result = cm.UseCode(code, address)
        return jsonify(result),200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/codeQuantity', methods=['POST'])
def codeQuantity():
    try:
        data = request.json
        code = str(data.get('code', 'ABCDE'))

        cm = codeManager()
        result = cm.getUnit(code)
        return jsonify(result),200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/useCodeOnWP', methods=['POST'])
def useCodeOnWP():
    try:
        data = request.json
        code = str(data.get('code', 'ABCDE'))
        cm = codeManager()
        result = cm.useCodeOnWP(code)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/updateCodeUsedOnWP', methods=['POST'])
def updateCodeUsedOnWP():
    try:
        data = request.json
        code = str(data.get('code', 'ABCDE'))
        order_id = str(data.get('order_id', 0000))
        user_agent = request.headers.get('User-Agent')
        cm = codeManager()
        result = cm.updateCodeUsedOnWP(code,user_agent, order_id)
        print(f"updateCodeUsedOnWP:{result}")
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/code/getWPCoupon', methods=['POST'])
def getWPCoupon():
    try:
        data = request.json
        code = str(data.get('code', 'all'))
        cm = codeManager()
        result = cm.getWPCoupon(code)
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({
            "status": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def hello():
    return "hello"

# @app.route('/test',methods=['POST'])
# def test():
#     try:
#         data = request.json
#         amount = float(data.get('amount', 0.1))
#         cm = codeManager()
#         result = cm.getQHCPerVNDPrice(amount)
#         return jsonify(result), 200
#     except Exception as e:
#         print(e)
#         return jsonify({
#             "status": False,
#             "error": str(e)
#         }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)