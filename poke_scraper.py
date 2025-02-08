import requests
from bs4 import BeautifulSoup
import os
import csv


pokemons = []
current_url = 'https://pokemondb.net/pokedex/bulbasaur'
os.makedirs('poke_csv', exist_ok=True)
csv_file_path = os.path.join('poke_csv', 'pokemon_sprites.csv')
poke_id = 0

 
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Id', 'Name', 'Sprite URL', 'Type', 'HP', 'Atk', 'Def', 'SpAtk', 'SpDef', 'Speed'])

    while True:
        r = requests.get(current_url)
        soup = BeautifulSoup(r.content, 'html.parser')

        poke_id += 1
        
        find_name = soup.find('h1',)
        poke_name = find_name.text

        find_sprite = soup.find_all('img', class_= 'img-sprite-v21')
        try:
            poke_sprite = find_sprite[0].get('src')
        except IndexError:
            try:
                find_sprite = soup.find_all('img', class_= 'img-sprite-v16')
                poke_sprite = find_sprite[0].get('src')
            except IndexError:
                try:
                    find_sprite = soup.find_all('img', class_= 'img-sprite-v13')
                    poke_sprite = find_sprite[0].get('src')
                except IndexError:
                    find_sprite = soup.find_all('img', class_= 'img-sprite-v18')
                    poke_sprite = find_sprite[0].get('src')

        poke_type = []
        find_type = soup.find_all('table', class_='vitals-table', limit=1)
        for table in find_type:
            links_with_p = table.find_all('a', class_="type-icon", recursive=True, limit=2)
            for link in links_with_p:
                poke_type.append(link.text)

        poke_stats = []
        find_stats = soup.find_all('div', class_='resp-scroll', limit=1)
        for tr in find_stats:
            find_tr_stats = tr.find_all('tr', limit=6)
            for td in find_tr_stats:
                poke_stats.append(td.find('td', class_="cell-num").text)
                
        
            
            csv_writer.writerow([poke_id, poke_name, poke_sprite, poke_type, poke_stats[0], poke_stats[1], poke_stats[2], poke_stats[3], poke_stats[4], poke_stats[5]])
            
            print(f"Added {poke_name} to CSV")
            pokemons.append(poke_name)

        next_link = soup.find('a', class_='entity-nav-next')
        
        if not next_link:
            break

        next_url = f'https://pokemondb.net{next_link["href"]}'
        current_url = next_url


print(f"\nCreated CSV with {len(pokemons)} Pokemon sprites at {csv_file_path}")
