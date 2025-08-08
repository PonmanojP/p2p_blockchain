from flask import Flask, jsonify, request, render_template, redirect, url_for
import requests
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def index():
    return render_template('index.html', chain=blockchain.chain, peers=blockchain.nodes)

@app.route('/mine_block')
def mine_block():
    previous = blockchain.last_block
    proof = blockchain.proof_of_work(previous['proof'])
    blockchain.add_transaction(sender='network', receiver='you', amount=1)
    blockchain.create_block(proof, blockchain.hash(previous))
    return redirect(url_for('index'))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']
    blockchain.add_transaction(sender, receiver, int(amount))
    return redirect(url_for('index'))

@app.route('/connect_node', methods=['POST'])
def connect_node():
    address = request.form['peer']
    blockchain.register_node(address)
    return redirect(url_for('index'))

@app.route('/replace_chain')
def replace_chain():
    blockchain.replace_chain(requests.get)
    return redirect(url_for('index'))

@app.route('/get_chain')
def get_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

if __name__ == '__main__':
    app.run(port=5001)
