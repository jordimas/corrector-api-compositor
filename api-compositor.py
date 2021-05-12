#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.


from __future__ import print_function
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import json
import urllib

import sys


app = Flask(__name__)
CORS(app)


def json_answer(data, status = 200):
    json_data = json.dumps(data, indent=4, separators=(',', ': '))
    resp = Response(json_data, mimetype='application/json', status = status)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def _get_lt_url(args):

    #lt = http://localhost:7001/v2/check?text=%22Hola%22&language=ca
    LT_URL = "http://localhost:7001/"
 
    url = urllib.parse.urljoin(LT_URL, "/v2/check")         
    query_string = urllib.parse.urlencode(args)      
    url = url + "?" + query_string
    print("*** " + url)
    return url

def _get_style_check_url(args):

    LT_URL = "http://localhost:8505/"
 
    url = urllib.parse.urljoin(LT_URL, "/check")         
    query_string = urllib.parse.urlencode(args)      
    url = url + "?" + query_string
    print("*** " + url)
    return url

@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@app.route('/check', methods=['GET'])
def check_api_get():
    print("GET check_api_get")
    return call_clients(request.args)

@cross_origin(origin='*',headers=['Content-Type','Authorization'])
@app.route('/check', methods=['POST'])
def check_api_post():
    return call_clients(request.form)

def call_clients(args):

    # LT
    lt_url = _get_lt_url(args)
    req = urllib.request.Request(lt_url)
    response = urllib.request.urlopen(req)

    response_text = response.read().decode(response.info().get_param('charset') or 'utf-8')
    lt_array = json.loads(response_text)



    #Style checker
    sc_url = _get_style_check_url(args)
    req = urllib.request.Request(sc_url)
    response = urllib.request.urlopen(req)

    response_text = response.read().decode(response.info().get_param('charset') or 'utf-8')
    sc_array = json.loads(response_text)

#    print("**SC Matches")
    lt_matches = lt_array["matches"]
    # Join responses
    for match in sc_array["matches"]:
        print(match)
        lt_matches.append(match)

#    print("**LT Matches")
    # Join responses
#    for match in
#        print(match)


#    print(f"Resposta: {sc_array}")
    json_data = json.dumps(lt_array, indent=4, separators=(',', ': '))
    resp = Response(json_data, mimetype='application/json', status = 200)
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

if __name__ == '__main__':
    app.debug = True
    app.run()

