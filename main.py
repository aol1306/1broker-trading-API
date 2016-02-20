#!/usr/bin/python
# written by 1306; aol1306.pl
# 1. load settings. if not exist - create json with default settings
# 2. l - open long position; s - short; v - show opened positions (if any)
# after opening position, take its open price and set stoploss
import json
import API1brokerlib
import time

settings = {'symbol' : "EURUSD", 'margin' : 0.01, 'leverage' : 1, 'stop_loss' : 0.001, 'take_profit' : 0.001}

def usage():
	print "Welcome to aol1306's 1broker app!"
	print "Usage: "
	print "l - open long position"
	print "s - open short position"
	print "c - close all positions"
	print "v - view opened positions"
	print "h - display this help message"
	print "t - show settings"
	print "q - quit"
	print ""

def get_settings():
	global settings
	try:
		# read settings
		fh = open("settings.json", 'r')
		settings = json.loads(fh.read())
	except:
		# write default settings
		fh = open("settings.json", 'w')
		fh.write(json.dumps(settings))

def set_stoploss_takeprofit(api):
	# check open price and direction;
	# if long, set stop loss openprice-stoplosspips/1000
	# if short, set stop loss openprice+stoplosspips/1000
	positions = api.position_list_open()
	positions = json.loads(positions)
	if positions["response"] == []:
		print "No open positions"
	else:
		for x in positions["response"]:
			direction = x["direction"]
			if direction == "long":
				sl = float(x["entry_price"])-settings["stop_loss"]
				tp = float(x["entry_price"])+settings["take_profit"]
				api.position_edit(int(x["position_id"]), stop_loss=sl, take_profit=tp)
			if direction == "short":
				sl = float(x["entry_price"])+settings["stop_loss"]
				tp = float(x["entry_price"])-settings["take_profit"]
				api.position_edit(int(x["position_id"]), stop_loss=sl, take_profit=tp)


def open_long(api):
	if(api.order_create(settings['symbol'], settings['margin'], "long", settings['leverage'], "Market")):
		set_stoploss_takeprofit(api)
		print "Position opened."
	else:
		print "Error."
	
def open_short(api):
	if(api.order_create(settings['symbol'], settings['margin'], "short", settings['leverage'], "Market")):
		set_stoploss_takeprofit(api)
		print "Position opened."
	else:
		print "Error."
		
def close_position(api):
	positions = api.position_list_open()
	positions = json.loads(positions)
	if positions["response"] == []:
		print "No open positions"
	else:
		for x in positions["response"]:
			api.position_edit(int(x["position_id"]), market_close="true")
			print "Closed position %s" % x["position_id"]
	
def view_positions(api):
	try:
		print "Press ctrl+c to exit"
		while True:
			positions = api.position_list_open()
			positions = json.loads(positions)
			if positions["response"] == []:
				print "No open positions"
			else:
				for x in positions["response"]:
					print
					print "%s %s position: (ID: %s)" % (x["symbol"], x["direction"], x["position_id"])
					print "P/L %s (%s%%), SL %s, TP %s" % (x["profit_loss"], x["profit_loss_percent"], x["stop_loss"], x["take_profit"])
					print "leverage %s, entry price %s" % (x["leverage"], x["entry_price"])
			time.sleep(3)
	except:
		print " Exited"



def main():
    # getting API token
    api_token = raw_input("Your API token: ")
    
    api = API1brokerlib.Connection(api_token)
    
    get_settings()
    usage()
    
    # main loop
    out = False
    while(out==False):
		choice = raw_input("Enter command: ")
		if choice == 'q':
			out = True
		elif choice == 'l':
			print "Please wait..."# all API calls takes time
			open_long(api)
		elif choice == 's':
			print "Please wait..."
			open_short(api)
		elif choice == 'c':
			print "Please wait..."
			close_position(api)
		elif choice == 'v':
			print "Please wait..."
			view_positions(api)
		elif choice == 't':
			print settings
		elif choice == 'h':
			usage()
		else:
			print "Unknown command."

main()
