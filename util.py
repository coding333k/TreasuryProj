from flask import Flask, jsonify
import json
import pickle

def get_yield_data_test():
    return ' is it working'

def get_yield_data():

    with open('yield_curves.json', 'r') as f:
        data = json.load(f)

        return jsonify(data)

    