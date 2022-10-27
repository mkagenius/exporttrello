import requests as req
import json
from time import sleep
key = <get key from trello settings>
token = <get token from trello settings>


org_url = "https://api.trello.com/1/members/me/organizations"
board_url = "https://api.trello.com/1/members/me/boards"
card_url = "https://api.trello.com/1/boards/{id}/cards"
ind_card_url = "https://api.trello.com/1/boards/{id}/cards/{idCard}"
comments_url = "https://api.trello.com/1/cards/{card_Id}/actions?filter=commentCard"

org_resp = req.get(org_url + "?key=" + key + "&token=" + token)
org_json = json.loads(org_resp.text)

board_resp = req.get(board_url + "?key=" + key + "&token=" + token)

board_json = json.loads(board_resp.text)

exclude_orgs = []

orgid2name = {} # org id to name
org2boards = {} # org_id -> [] array of board ids
board2cards = {} # board_id -> [] array of card id, name tuple

for i in org_json:
	orgid2name[i["id"]] = i["displayName"]

print(orgid2name)
for i in org_json:
	org2boards[i["id"]] = i["idBoards"]

for i in board_json:
	board2cards[i["id"]] = []
	print("fetching board id: " + i["id"] + "...")
	cards_resp = req.get("https://api.trello.com/1/boards/"+i["id"]+"/cards" + "?key=" + key + "&token=" + token)
	cards_json = json.loads(cards_resp.text)
	for j in cards_json:
		comments_url = "https://api.trello.com/1/cards/"+j["id"]+"/actions?filter=commentCard" +  "&key=" + key + "&token=" + token
		sleep(0.1)
		comments_resp = req.get(comments_url)
		comments_json = json.loads(comments_resp.text)
		comments = []
		for c in comments_json:
			comments.append(c["data"]["text"])
		board2cards[i["id"]].append((j["id"], j["name"], comments))
	print("[done]")




org_list = orgid2name.keys()

for o in org_list:
	if o in exclude_orgs:
		continue
	boards = org2boards[o]
	print("=============================================================")
	print(orgid2name[o])
	print("=============================================================\n\n\n")
	for b in boards:
		if b not in board2cards:
			continue
		for t in board2cards[b]:
			print("----------------------------------------")
			print("Title: " + t[1])
			print("----------------------------------------\n")
			idx = 0
			for c in t[2]:
				idx+=1
				print("Comment #"+ str(idx) + ": \n" + c)
				print("\n\n\n\n")



