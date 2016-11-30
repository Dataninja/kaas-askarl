#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, uuid, random, pickle, sys
from flask import Flask, Response, request, redirect

version = "1.0.3"
repo_url = "https://github.com/Dataninja/kaas-askarl"
file_db = "./users.db"
bots = {
    "karl": {
        "id": "karl",
        "name": "Carlo Romagnoli",
        "twitter": "@karlettin",
        "handler": "/to/karl"
    }
}
responses = {
    "karl": [
        "E che te lo dico a fare... 'a Banca Mondiale, c'hanno tutto!",
        "Eurostat... stacce!",
        "Po esse' che all'Istat ce ricavi quarcosa, se nun te perdi...",
        "Eh, ma questa è tosta, te devo trova' du' dati appizzati...",
        "Eh, ieri 'a sapevo...",
        "No, guarda, io 'sti dati nun li tocco, se li voi prende' da te, ma io nun li vojo manco vede'!",
        "Mo' chiamo st'amico mio e te li rimedio, tranqui proprio..."
    ]
}
methods = {
    "to": {
        "id": "to",
        "handler": "/to"
    },
    "for": {
        "id": "for",
        "handler": "/for"
    }
}
parameters = {
    "to_bot": {
        "q": {
            "id": "q",
            "name": "question",
            "type": "string",
            "description": "Question text"
        },
        "token": {
            "id": "t",
            "name": "token",
            "type": "string",
            "description": "Registered user token"
        },
        "mode": {
            "id": "m",
            "name": "mode",
            "type": "string",
            "description": "Question mode: %s" % " | ".join([
                "fast",
                "accurate",
                "fa (fast AND accurate)"
            ])
        },
        "budget": {
            "id": "b",
            "name": "budget",
            "type": "integer",
            "description": "Budget to offer in €"
        },
        "reply-to": {
            "id": "r",
            "name": "reply-to",
            "type": "string",
            "description": "Reply to method: %s" % " | ".join([
                "now (wait for response)",
                "yourmail@yourdomain.com (send to email)",
                "http://your.domain.com/callback (webhook)"
            ])
        }
    },
    "for_user": {
        "token": {
            "id": "t",
            "name": "token",
            "type": "string",
            "description": "Registered user token"
        },
        "budget": {
            "id": "b",
            "name": "budget",
            "type": "integer",
            "description": "Add budget in €"
        },
        "bonus": {
            "id": "bo",
            "name": "budget",
            "type": "integer",
            "description": "Add bonus points"
        },
        "reply-to": {
            "id": "r",
            "name": "reply-to",
            "type": "string",
            "description": "Reply to method: %s" % " | ".join([
                "now (wait for response)",
                "yourmail@yourdomain.com (send to email)",
                "http://your.domain.com/callback (webhook)"
            ])
        }
    },
    "for_token": {
        "name": {
            "id": "n",
            "name": "name",
            "type": "string",
            "description": "User name"
        },
        "budget": {
            "id": "b",
            "name": "budget",
            "type": "integer",
            "description": "Budget to offer in €"
        },
        "reply-to": {
            "id": "r",
            "name": "reply-to",
            "type": "string",
            "description": "Reply to method: %s" % " | ".join([
                "now (wait for response)",
                "yourmail@yourdomain.com (send to email)",
                "http://your.domain.com/callback (webhook)"
            ])
        }
    },
    "for_remove": {
        "token": {
            "id": "t",
            "name": "token",
            "type": "string",
            "description": "Registered user token"
        }
    }
}
try:
    with open(file_db) as f:
        users = pickle.load(f)
except Exception, e:
    users = {}

app = Flask(__name__)

def to_num(s):
    try:
        if 'k' in s:
            return int(s.replace('k',''))*1000
        if 'm' in s:
            return int(s.replace('m',''))*1000*1000
        return int(s)
    except Exception, e:
        return 0

def add_url(obj, base_url = "", from_key = "handler", to_key = "url"):
    obj[to_key] = base_url + obj[from_key]
    return obj

@app.route("/")
def main():
    received = int(time.time())
    base_url = request.url_root[0:-1]

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "response": "You Know, for Ask! See %s/releases/tag/v%s" % (repo_url,version),
            "methods": map(lambda x: add_url(x, base_url), methods.values())
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

@app.route("/to")
def rto():
    received = int(time.time())
    base_url = request.url_root[0:-1]

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "methods": map(lambda x: add_url(x, base_url), bots.values())
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

@app.route("/to/<bot>")
def to_bot(bot = ""):
    received = int(time.time())

    args = request.args
    question = args.get("q",args.get("question",""))
    token = args.get("t",args.get("token",""))
    mode = args.get("m",args.get("mode","fast"))
    budget = to_num(args.get("b",args.get("budget","0")))

    if bot not in bots:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "not available",
                "question": question,
                "response": "..."
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 404,
            mimetype = "application/json"
        )

    if not question:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "malformed",
                "question": question,
                "response": "Il saggio Esti Qatsi risponde al silenzio col silenzio...",
                "thanks-to": bot,
                "parameters": parameters['to_bot']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 400,
            mimetype = "application/json"
        )

    if not token:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "forbidden",
                "question": question,
                "response": "Chi sei, che vuoi? Un fiorino!",
                "thanks-to": bot,
                "parameters": parameters['to_bot']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 403,
            mimetype = "application/json"
        )

    user = users[token]

    if not budget and not user['bonus']:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "forbidden",
                "question": question,
                "response": "Sotto i 2k, niente!",
                "thanks-to": bot,
                "parameters": parameters['to_bot']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 403,
            mimetype = "application/json"
        )

    if budget > user['budget'] and not user['bonus']:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "forbidden",
                "question": question,
                "response": "Te piaceria... nun c'hai li sordi!",
                "thanks-to": bot,
                "parameters": parameters['to_bot']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 403,
            mimetype = "application/json"
        )

    reply_to = args.get("r",args.get("reply-to",user['reply-to']))

    if reply_to == "now":
        time.sleep(random.randint(1,min(len(question.split()),10)))
        if budget > 1999:
            response = "Ao, se c'hai pure da puli' 'a machina chiamame de corsa! %s" % random.choice(responses[bot])
        elif budget > 9:
            response = "Nun so' 2k, ma bono così! %s" % random.choice(responses[bot])
        elif not user['bonus']:
            response = "Mortacci che purciaro! %s" % random.choice(responses[bot])
        else:
            response = "Tò, piglia e porta a casa! %s" % random.choice(responses[bot])
    else:
        if mode == "fast":
            response = "E mo quarcosa te trovo, intanto vatte a vede' 'a Banca Mondiale che c'ha tutto..."
        elif mode == "fa":
            response = "Se vabbè, nun t'allarga', quanno c'ho tempo..."

    if user['bonus']:
        user['bonus'] -= 1
    else:
        user['budget'] -= budget

    user['questions'].append({
        "id": str(uuid.uuid4()),
        "received": received,
        "emitted": int(time.time()),
        "question": question,
        "response": response,
        "thanks-to": bot
    })
    user['last_action'] = int(time.time())

    with open(file_db,"w") as f:
        pickle.dump(users,f)

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "question": question,
            "response": response,
            "thanks-to": bot
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )


@app.route("/for")
def rfor():
    received = int(time.time())
    base_url = request.url_root[0:-1]

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "methods": [
                {
                    "id": "user",
                    "handler": "/for/user",
                    "url": "%s/for/user" % base_url
                },
                {
                    "id": "token",
                    "handler": "/for/token",
                    "url": "%s/for/token" % base_url
                },
                {
                    "id": "remove",
                    "handler": "/for/remove",
                    "url": "%s/for/remove" % base_url
                }
            ]
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

@app.route("/for/user")
def for_user():
    received = int(time.time())

    args = request.args
    token = args.get("t",args.get("token",""))
    budget = to_num(args.get("b",args.get("budget","0")))
    bonus = to_num(args.get("bo",args.get("bonus","0")))

    if token not in users:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "forbidden",
                "response": "Chi sei, che vuoi? Un fiorino!",
                "parameters": parameters['for_user']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 403,
            mimetype = "application/json"
        )

    user = users[token]

    if budget:
        user['budget'] += budget
        user['last_update'] = int(time.time())

    if bonus:
        user['bonus'] += bonus
        user['last_update'] = int(time.time())

    user['last_action'] = int(time.time())

    with open(file_db,"w") as f:
        pickle.dump(users,f)

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "response": user
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

@app.route("/for/token")
def for_token():
    received = int(time.time())

    args = request.args
    name = args.get("n",args.get("name",""))
    budget = to_num(args.get("b",args.get("budget","0")))
    reply_to = args.get("r",args.get("reply-to","now"))

    if not name:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "malformed",
                "response": "Il saggio Esti Qatsi non parla con gli sconosciuti...",
                "parameters": parameters['for_token']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 400,
            mimetype = "application/json"
        )

    token = str(uuid.uuid4())
    users[token] = {
        "id": token,
        "token": token,
        "name": name,
        "budget": budget,
        "reply-to": reply_to,
        "created_at": int(time.time()),
        "last_update": int(time.time()),
        "last_action": int(time.time()),
        "questions": [],
        "bonus": 0
    }

    with open(file_db,"w") as f:
        pickle.dump(users,f)

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "response": users[token]
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

@app.route("/for/users")
def for_users():
    received = int(time.time())

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "response": users
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

@app.route("/for/remove")
def for_remove():
    received = int(time.time())

    args = request.args
    token = args.get("t",args.get("token",""))

    if not token:
        return Response(
            response = json.dumps({
                "received": received,
                "emitted": int(time.time()),
                "status": "forbidden",
                "response": "Chi sei, che vuoi? Un fiorino!",
                "parameters": parameters['for_remove']
            }, sort_keys=True, indent=4, separators=(',', ': ')),
            status = 403,
            mimetype = "application/json"
        )

    del users[token]

    with open(file_db,"w") as f:
        pickle.dump(users,f)

    return Response(
        response = json.dumps({
            "received": received,
            "emitted": int(time.time()),
            "status": "ok",
            "response": {}
        }, sort_keys=True, indent=4, separators=(',', ': ')),
        status = 200,
        mimetype = "application/json"
    )

if __name__ == "__main__":

    print "Up and running!"

    ports = {
        "dev": 51346,
        "prod": 51345
    }

    if len(sys.argv) > 1:
        if sys.argv[1].isdigit():
            debug = False
            port = int(sys.argv[1])
        elif sys.argv[1] in ports:
            debug = sys.argv[1] == "dev"
            port = ports[sys.argv[1]]
        else:
            debug = False
            port = ports["prod"]
    else:
        debug = False
        port = ports["prod"]

    app.run(port = port, debug = debug)

    with open(file_db,"w") as f:
        pickle.dump(users,f)

    print "Bye!"

