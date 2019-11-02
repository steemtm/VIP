# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from beem import Steem
from beem.comment import Comment
from beem.nodelist import NodeList
from steemengine.api import Api
import time


if __name__ == "__main__":
    nodelist = NodeList()
    nodelist.update_nodes()
    stm = Steem(node=nodelist.get_nodes())
    api = Api()
    
    # edit here
    upvote_account = "ufm.pay"
    upvote_token = "UFM"
    token_weight_factor = 1 # multiply token amount to get weight
    min_token_amount = 1.00
    whitelist = []
    stm.wallet.unlock("wallet-passwd")
    last_steem_block = 1950 # It is a good idea to store this block, otherwise all transfers will be checked again
    while True:
        history = api.get_history(upvote_account, upvote_token, limit=1000, offset=0, histtype='user')
        for h in history:
            if int(h["block"]) <= last_steem_block:
                continue
            if h["to"] != upvote_account:
                continue
            last_steem_block = int(h["block"])
            if len(whitelist) > 0 and h["from"] not in whitelist:
                print("%s is not in the whitelist, skipping" % h["from"])
                continue
            if float(h["quantity"]) < min_token_amount:
                print("Below min token amount skipping...")
                continue 
