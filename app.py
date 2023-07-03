import requests
import time
from datetime import datetime
from operator import itemgetter
import json


def get_collection(slug):
    url = "https://api.opensea.io/api/v1/collection/%s" % slug
    
    r = requests.get(url).json()['collection']    
    tot_supply = r['stats']['count']
    
    return tot_supply
    

def get_nfts(slug, tot_supply):

    
    headers = {
        "Accept": "application/json",
        "X-API-KEY": ""#<===INSERT HERE YOUR API KEY
    }

    tot_loop = tot_supply/30
    n = 1

    url = "https://api.opensea.io/api/v1/assets?collection=%s" % slug
    nfts = []
    
    #divide supply by 30 max no. of iter available
    for x in range(int(tot_loop)):

        for y in range(n, n+30):
            url = url+'&token_ids='+str(y)

        assets = requests.get(url, headers=headers).json()

        #ASSET 
        for asset in assets['assets']:
            traits = []
            rarity_score = []
            
            token_id = asset['token_id']
            image_url = asset['image_original_url']

            if len(asset['traits']) == 0:
                rarity_score = None
                traits = None
                
            else:            
                for trait in asset['traits']:
                    #TYPE-VALUE-N.T,OTHER TRAIT
                    try:
                        traits.append({'trait_type': trait['trait_type'], 'value': trait['value'], 'trait_rarity': 1/(trait['trait_count']/tot_supply)})
                        rarity_score.append(1/(trait['trait_count']/tot_supply))
                    except Exception as e:
                        print(e)
                        continue
                    

            nft = {
                'token_id': token_id,
                'image_url': image_url,
                'traits': traits,
                'rarity_score': sum(rarity_score),
                }

            nfts.append(nft)
            
            
        n = n+30
        url = "https://api.opensea.io/api/v1/assets?collection=%s" % slug
        time.sleep(0.05)
        
    return sorted(nfts, key=itemgetter('rarity_score'))[::-1]

def rarity_score():
    slug = input("***Welcome to the software developed by Astrid for joe.eth*** \nPlease insert the collection slug: ")
    tot_supply = get_collection(slug)
    start = datetime.now()


    nfts = get_nfts(slug, tot_supply)
    data = {'data': nfts}
    
    with open(slug+'-rarity-data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
        
    end = datetime.now()
    print('Json succesfully created.\n\nSTATS\n')
    print('Total time required: '+str(end-start)+'\n')
    print('Time required for each NFT: '+str((end-start)/len(nfts))+'\n')

rarity_score()
