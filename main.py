import os
import requests
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

from keras.models import load_model
from keras.backend import clear_session

import tensorflowjs as tfjs


classes = [
	'Abomasnow', 'Abomasnow(Mega)', 'Abra', 'Absol', 'Absol(Mega)', 'Accelgor', 'Aegislash', 'Aerodactyl', 'Aerodactyl(Mega)', 'Aggron', 'Aggron(Mega)', 'Aipom', 'Alakazam', 'Alakazam(Mega)', 'Alomomola', 'Altaria', 'Altaria(Mega)', 'Amaura', 'Ambipom', 'Amoonguss', 'Ampharos', 'Ampharos(Mega)', 'Anorith', 'Araquanid', 'Arbok', 'Arcanine', 'Arceus', 'Archen', 'Archeops', 'Ariados', 'Armaldo', 'Aromatisse', 'Aron', 'Articuno', 'Audino', 'Audino(Mega)', 'Aurorus', 'Avalugg', 'Axew', 'Azelf', 'Azumarill', 'Azurill', 'Bagon', 'Baltoy', 'Banette', 'Banette(Mega)', 'Barbaracle', 'Barboach', 'Basculin(Blue-Striped)', 'Basculin(Red-Striped)', 'Bastiodon', 'Bayleef', 'Beartic', 'Beautifly', 'Beedrill', 'Beedrill(Mega)', 'Beheeyem', 'Beldum', 'Bellossom', 'Bellsprout', 'Bergmite', 'Bewear', 'Bibarel', 'Bidoof', 'Binacle', 'Bisharp', 'Blacephalon', 'Blastoise', 'Blastoise(Mega)', 'Blaziken', 'Blaziken(Mega)', 'Blissey', 'Blitzle', 'Boldore', 'Bonsly', 'Bouffalant', 'Bounsweet', 'Braixen', 'Braviary', 'Breloom', 'Brionne', 'Bronzong', 'Bronzor', 'Bruxish', 'Budew', 'Buizel', 'Bulbasaur', 'Buneary', 'Bunnelby', 'Burmy(Plant)', 'Burmy(Sandy)', 'Burmy(Trash)', 'Butterfree', 'Buzzwole', 'Cacnea', 'Cacturne', 'Camerupt', 'Camerupt(Mega)', 'Carbink', 'Carnivine', 'Carracosta', 'Carvanha', 'Cascoon', 'Castform', 'Castform(Rain)', 'Castform(Snowy)', 'Castform(Sunny)', 'Caterpie', 'Celebi', 'Celesteela', 'Chandelure', 'Chansey', 'Charizard', 'Charizard(Mega X)', 'Charizard(Mega Y)', 'Charjabug', 'Charmander', 'Charmeleon', 'Chatot', 'Cherrim(Overcast)', 'Cherrim(Sunshine)', 'Cherubi', 'Chesnaught', 'Chespin', 'Chikorita', 'Chimchar', 'Chimecho', 'Chinchou', 'Chingling', 'Cinccino', 'Clamperl', 'Clauncher', 'Clawitzer', 'Claydol', 'Clefable', 'Clefairy', 'Cleffa', 'Cloyster', 'Cobalion', 'Cofagrigus', 'Combee', 'Combusken', 'Comfey', 'Conkeldurr', 'Corphish', 'Corsola', 'Cosmoem', 'Cosmog', 'Cottonee', 'Crabominable', 'Crabrawler', 'Cradily', 'Cranidos', 'Crawdaunt', 'Cresselia', 'Croagunk', 'Crobat', 'Croconaw', 'Crustle', 'Cryogonal', 'Cubchoo', 'Cubone', 'Cutiefly', 'Cyndaquil', 'Darkrai', 'Darmanitan(Standard)', 'Darmanitan(Zen)', 'Dartrix', 'Darumaka', 'Decidueye', 'Dedenne', 'Deerling(Autumn)', 'Deerling(Spring)', 'Deerling(Summer)', 'Deerling(Winter)', 'Deino', 'Delcatty', 'Delibird', 'Delphox', 'Deoxys', 'Dewgong', 'Dewott', 'Dewpider', 'Dhelmise', 'Dialga', 'Diancie', 'Diancie(Mega)', 'Diggersby', 'Diglett', 'Diglett(Alola)', 'Ditto', 'Dodrio', 'Doduo', 'Donphan', 'Doublade', 'Dragalge', 'Dragonair', 'Dragonite', 'Drampa', 'Drapion', 'Dratini', 'Drifblim', 'Drifloon', 'Drilbur', 'Drowzee', 'Druddigon', 'Ducklett', 'Dugtrio', 'Dugtrio(Alola)', 'Dunsparce', 'Duosion', 'Durant', 'Dusclops', 'Dusknoir', 'Duskull', 'Dustox', 'Dwebble', 'Eelektrik', 'Eelektross', 'Eevee', 'Ekans', 'Electabuzz', 'Electivire', 'Electrike', 'Electrode', 'Elekid', 'Elgyem', 'Emboar', 'Emolga', 'Empoleon', 'Entei', 'Escavalier', 'Espeon', 'Espurr', 'Excadrill', 'Exeggcute', 'Exeggutor', 'Exeggutor(Alola)', 'Exploud', '"Farfetchd"', 'Fearow', 'Feebas', 'Fennekin', 'Feraligatr', 'Ferroseed', 'Ferrothorn', 'Finneon', 'Flaaffy', 'FlabВbВ', 'Flareon', 'Fletchinder', 'Fletchling', 'Floatzel', 'Floette', 'Florges', 'Flygon', 'Fomantis', 'Foongus', 'Forretress', 'Fraxure', 'Frillish(Female)', 'Frillish(Male)', 'Froakie', 'Frogadier', 'Froslass', 'Furfrou', 'Furret', 'Gabite', 'Gallade', 'Gallade(Mega)', 'Galvantula', 'Garbodor', 'Garchomp', 'Garchomp(Mega)', 'Gardevoir', 'Gardevoir(Mega)', 'Gastly', 'Gastrodon(East)', 'Gastrodon(West)', 'Genesect', 'Gengar', 'Gengar(Mega)', 'Geodude', 'Geodude(Alola)', 'Gible', 'Gigalith', 'Girafarig', 'Giratina(Altered)', 'Giratina(Origin)', 'Glaceon', 'Glalie', 'Glalie(Mega)', 'Glameow', 'Gligar', 'Gliscor', 'Gloom', 'Gogoat', 'Golbat', 'Goldeen', 'Golduck', 'Golem', 'Golem(Alola)', 'Golett', 'Golisopod', 'Golurk', 'Goodra', 'Goomy', 'Gorebyss', 'Gothita', 'Gothitelle', 'Gothorita', 'Gourgeist', 'Granbull', 'Graveler', 'Graveler(Alola)', 'Greninja', 'Greninja(Ash)', 'Grimer', 'Grimer(Alola)', 'Grotle', 'Groudon', 'Groudon(Primal)', 'Grovyle', 'Growlithe', 'Grubbin', 'Grumpig', 'Gulpin', 'Gumshoos', 'Gurdurr', 'Guzzlord', 'Gyarados', 'Gyarados(Mega)', 'Hakamo-o', 'Happiny', 'Hariyama', 'Haunter', 'Hawlucha', 'Haxorus', 'Heatmor', 'Heatran', 'Heliolisk', 'Helioptile', 'Heracross', 'Heracross(Mega)', 'Herdier', 'Hippopotas', 'Hippowdon', 'Hitmonchan', 'Hitmonlee', 'Hitmontop', 'Ho-Oh', 'Honchkrow', 'Honedge', 'Hoopa(Confined)', 'Hoopa(Unbound)', 'Hoothoot', 'Hoppip', 'Horsea', 'Houndoom', 'Houndoom(Mega)', 'Houndour', 'Huntail', 'Hydreigon', 'Hypno', 'Igglybuff', 'Illumise', 'Incineroar', 'Infernape', 'Inkay', 'Ivysaur', 'Jangmo-o', 'Jellicent(Female)', 'Jellicent(Male)', 'Jigglypuff', 'Jirachi', 'Jolteon', 'Joltik', 'Jumpluff', 'Jynx', 'Kabuto', 'Kabutops', 'Kadabra', 'Kakuna', 'Kangaskhan', 'Kangaskhan(Mega)', 'Karrablast', 'Kartana', 'Kecleon', 'Keldeo(Ordinary)', 'Keldeo(Resolute)', 'Kingdra', 'Kingler', 'Kirlia', 'Klang', 'Klefki', 'Klink', 'Klinklang', 'Koffing', 'Komala', 'Kommo-o', 'Krabby', 'Kricketot', 'Kricketune', 'Krokorok', 'Krookodile', 'Kyogre', 'Kyogre(Primal)', 'Kyurem', 'Kyurem(Black)', 'Kyurem(White)', 'Lairon', 'Lampent', 'Landorus(Incarnate)', 'Landorus(Therian)', 'Lanturn', 'Lapras', 'Larvesta', 'Larvitar', 'Latias', 'Latias(Mega)', 'Latios', 'Latios(Mega)', 'Leafeon', 'Leavanny', 'Ledian', 'Ledyba', 'Lickilicky', 'Lickitung', 'Liepard', 'Lileep', 'Lilligant', 'Lillipup', 'Linoone', 'Litleo', 'Litten', 'Litwick', 'Lombre', 'Lopunny', 'Lopunny(Mega)', 'Lotad', 'Loudred', 'Lucario', 'Lucario(Mega)', 'Ludicolo', 'Lugia', 'Lumineon', 'Lunala', 'Lunatone', 'Lurantis', 'Luvdisc', 'Luxio', 'Luxray', 'Lycanroc(Dusk)', 'Lycanroc(Midday)', 'Lycanroc(Midnight)', 'Machamp', 'Machoke', 'Machop', 'Magby', 'Magcargo', 'Magearna', 'Magikarp', 'Magmar', 'Magmortar', 'Magnemite', 'Magneton', 'Magnezone', 'Makuhita', 'Malamar', 'Mamoswine', 'Manaphy', 'Mandibuzz', 'Manectric', 'Manectric(Mega)', 'Mankey', 'Mantine', 'Mantyke', 'Maractus', 'Mareanie', 'Mareep', 'Marill', 'Marowak', 'Marowak(Alola)', 'Marshadow', 'Marshtomp', 'Masquerain', 'Mawile', 'Mawile(Mega)', 'Medicham', 'Medicham(Mega)', 'Meditite', 'Meganium', 'Melmetal', 'Meloetta(Aria)', 'Meloetta(Pirouette)', 'Meltan', 'Meowstic(Female)', 'Meowstic(Male)', 'Meowth', 'Meowth(Alolan)', 'Mesprit', 'Metagross', 'Metagross(Mega)', 'Metang', 'Metapod', 'Mew', 'Mewtwo', 'Mewtwo_X(Mega)', 'Mewtwo_Y(Mega)', 'Mienfoo', 'Mienshao', 'Mightyena', 'Milotic', 'Miltank', 'Mime_Jr', 'Mimikyu', 'Minccino', 'Minior(Core)', 'Minior(Meteor)', 'Minun', 'Misdreavus', 'Mismagius', 'Moltres', 'Monferno', 'Morelull', 'Mothim', 'Mr.Mime', 'Mudbray', 'Mudkip', 'Mudsdale', 'Muk', 'Muk(Alola)', 'Munchlax', 'Munna', 'Murkrow', 'Musharna', 'Naganadel', 'Natu', 'Necrozma', 'Necrozma(Dawn)', 'Necrozma(Dusk)', 'Necrozma(Ultra)', 'Nidoking', 'Nidoqueen', 'Nidoran(Female)', 'Nidoran(Male)', 'Nidorina', 'Nidorino', 'Nihilego', 'Nincada', 'Ninetales', 'Ninetales(Alola)', 'Ninjask', 'Noctowl', 'Noibat', 'Noivern', 'Nosepass', 'Numel', 'Nuzleaf', 'Octillery', 'Oddish', 'Omanyte', 'Omastar', 'Onix', 'Oranguru', 'Oricorio(Baile)', '"Oricorio(Pau)"', 'Oricorio(Pom-Pom)', 'Oricorio(Sensu)', 'Oshawott', 'Pachirisu', 'Palkia', 'Palossand', 'Palpitoad', 'Pancham', 'Pangoro', 'Panpour', 'Pansage', 'Pansear', 'Paras', 'Parasect', 'Passimian', 'Patrat', 'Pawniard', 'Pelipper', 'Persian', 'Persian(Alolan)', 'Petilil', 'Phanpy', 'Phantump', 'Pheromosa', 'Phione', 'Pichu', 'Pidgeot', 'Pidgeot(Mega)', 'Pidgeotto', 'Pidgey', 'Pidove', 'Pignite', 'Pikachu', 'Pikipek', 'Piloswine', 'Pineco', 'Pinsir', 'Pinsir(Mega)', 'Piplup', 'Plusle', 'Poipole', 'Politoed', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Ponyta', 'Poochyena', 'Popplio', 'Porygon', 'Porygon-Z', 'Porygon2', 'Primarina', 'Primeape', 'Prinplup', 'Probopass', 'Psyduck', 'Pumpkaboo', 'Pupitar', 'Purrloin', 'Purugly', 'Pyroar(Female)', 'Pyroar(Male)', 'Pyukumuku', 'Quagsire', 'Quilava', 'Quilladin', 'Qwilfish', 'Raichu', 'Raichu(Alola)', 'Raikou', 'Ralts', 'Rampardos', 'Rapidash', 'Raticate', 'Raticate(Alolan)', 'Rattata', 'Rattata(Alolan)', 'Rayquaza', 'Rayquaza(Mega)', 'Regice', 'Regigigas', 'Regirock', 'Registeel', 'Relicanth', 'Remoraid', 'Reshiram', 'Reuniclus', 'Rhydon', 'Rhyhorn', 'Rhyperior', 'Ribombee', 'Riolu', 'Rockruff', 'Roggenrola', 'Roselia', 'Roserade', 'Rotom', 'Rotom(Fan)', 'Rotom(Frost)', 'Rotom(Heat)', 'Rotom(Mow)', 'Rotom(Wash)', 'Rowlet', 'Rufflet', 'Sableye', 'Sableye(Mega)', 'Salamence', 'Salamence(Mega)', 'Salandit', 'Salazzle', 'Samurott', 'Sandile', 'Sandshrew', 'Sandshrew(Alola)', 'Sandslash', 'Sandslash(Alola)', 'Sandygast', 'Sawk', 'Sawsbuck(Autumn)', 'Sawsbuck(Spring)', 'Sawsbuck(Summer)', 'Sawsbuck(Winter)', 'Scatterbug', 'Sceptile', 'Sceptile(Mega)', 'Scizor', 'Scizor(Mega)', 'Scolipede', 'Scrafty', 'Scraggy', 'Scyther', 'Seadra', 'Seaking', 'Sealeo', 'Seedot', 'Seel', 'Seismitoad', 'Sentret', 'Serperior', 'Servine', 'Seviper', 'Sewaddle', 'Sharpedo', 'Sharpedo(Mega)', 'Shaymin(Land)', 'Shaymin(Sky)', 'Shedinja', 'Shelgon', 'Shellder', 'Shellos(East)', 'Shellos(West)', 'Shelmet', 'Shieldon', 'Shiftry', 'Shiinotic', 'Shinx', 'Shroomish', 'Shuckle', 'Shuppet', 'Sigilyph', 'Silcoon', 'Silvally', 'Simipour', 'Simisage', 'Simisear', 'Skarmory', 'Skiddo', 'Skiploom', 'Skitty', 'Skorupi', 'Skrelp', 'Skuntank', 'Slaking', 'Slakoth', 'Sliggoo', 'Slowbro', 'Slowbro(Mega)', 'Slowking', 'Slowpoke', 'Slugma', 'Slurpuff', 'Smeargle', 'Smoochum', 'Sneasel', 'Snivy', 'Snorlax', 'Snorunt', 'Snover', 'Snubbull', 'Solgaleo', 'Solosis', 'Solrock', 'Spearow', 'Spewpa', 'Spheal', 'Spinarak', 'Spinda', 'Spiritomb', 'Spoink', 'Spritzee', 'Squirtle', 'Stakataka', 'Stantler', 'Staraptor', 'Staravia', 'Starly', 'Starmie', 'Staryu', 'Steelix', 'Steelix(Mega)', 'Steenee', 'Stoutland', 'Stufful', 'Stunfisk', 'Stunky', 'Sudowoodo', 'Suicune', 'Sunflora', 'Sunkern', 'Surskit', 'Swablu', 'Swadloon', 'Swalot', 'Swampert', 'Swampert(Mega)', 'Swanna', 'Swellow', 'Swinub', 'Swirlix', 'Swoobat', 'Sylveon', 'Taillow', 'Talonflame', 'Tangela', 'Tangrowth', 'Tapu_Bulu', 'Tapu_Fini', 'Tapu_Koko', 'Tapu_Lele', 'Tauros', 'Teddiursa', 'Tentacool', 'Tentacruel', 'Tepig', 'Terrakion', 'Throh', 'Thundurus(Incarnate)', 'Thundurus(Therian)', 'Timburr', 'Tirtouga', 'Togedemaru', 'Togekiss', 'Togepi', 'Togetic', 'Torchic', 'Torkoal', 'Tornadus(Incarnate)', 'Tornadus(Therian)', 'Torracat', 'Torterra', 'Totodile', 'Toucannon', 'Toxapex', 'Toxicroak', 'Tranquill', 'Trapinch', 'Treecko', 'Trevenant', 'Tropius', 'Trubbish', 'Trumbeak', 'Tsareena', 'Turtonator', 'Turtwig', 'Tympole', 'Tynamo', 'Type_Null', 'Typhlosion', 'Tyranitar', 'Tyranitar(Mega)', 'Tyrantrum', 'Tyrogue', 'Tyrunt', 'Umbreon', 'Unfezant(Female)', 'Unfezant(Male)', 'Unown', 'Ursaring', 'Uxie', 'Vanillish', 'Vanillite', 'Vanilluxe', 'Vaporeon', 'Venipede', 'Venomoth', 'Venonat', 'Venusaur', 'Venusaur(Mega)', 'Vespiquen', 'Vibrava', 'Victini', 'Victreebel', 'Vigoroth', 'Vikavolt', 'Vileplume', 'Virizion', 'Vivillon', 'Volbeat', 'Volcanion', 'Volcarona', 'Voltorb', 'Vullaby', 'Vulpix', 'Vulpix(Alola)', 'Wailmer', 'Wailord', 'Walrein', 'Wartortle', 'Watchog', 'Weavile', 'Weedle', 'Weepinbell', 'Weezing', 'Whimsicott', 'Whirlipede', 'Whiscash', 'Whismur', 'Wigglytuff', 'Wimpod', 'Wingull', 'Wishiwashi', 'Wishiwashi(School)', 'Wobbuffet', 'Woobat', 'Wooper', 'Wormadam(Plant)', 'Wormadam(Sandy)', 'Wormadam(Trash)', 'Wurmple', 'Wynaut', 'Xatu', 'Xerneas', 'Xurkitree', 'Yamask', 'Yanma', 'Yanmega', 'Yungoos', 'Yveltal', 'Zangoose', 'Zapdos', 'Zebstrika', 'Zekrom', 'Zeraora', 'Zigzagoon', 'Zoroark', 'Zorua', 'Zubat', 'Zweilous', 'Zygarde(10%)', 'Zygarde(100%)', 'Zygarde(50%)'
]

# clear_session() # this resets the session containing the stale, not-best version of the model 

# Model Source:
# https://www.kaggle.com/kwisatzhaderach/neural-networks-with-pokemon/
model = load_model('baseModel/InceptionV3_Pokemon.h5', compile=False)
# preprocessing and predicting function for test images:
def predict_this(this_img):
	if this_img.mode != 'RGB':
		# print('converting to rgb')
		temp_img = Image.new("RGB", this_img.size, (255, 255, 255))
		temp_img.paste(this_img, mask = this_img.split()[3])
		temp_img.save("temp/temp.jpg", "JPEG", quality=100)
		this_img = Image.open('temp/temp.jpg')
		# print(this_img.mode)
	im = this_img.resize((160,160)) # size expected by network
	img_array = np.array(im)
	img_array = img_array/255 # rescale pixel intensity as expected by network
	img_array = np.expand_dims(img_array, axis=0) # reshape from (160,160,3) to (1,160,160,3)
	pred = model.predict(img_array)
	return np.argmax(pred, axis=1).tolist()[0]

def guessPokemon(url, debug=False):
	response = requests.get(url)
	img = Image.open(BytesIO(response.content))
	idx = predict_this(img)
	pkmn = classes[idx]

	if debug:
		print('idx:', idx, '; pkmn:', pkmn)
	else:
		print("A wild {} appears!".format(pkmn))

	return pkmn


# guessPokemon('https://assets.pokemon.com/assets/cms2/img/pokedex/full/809.png')





import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '''
	<h1>pokemon and friends</h1>
	<p>An API for Guessing Pokemon </p>
	'''
	
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/pokemon', methods=['GET'])
def api_filter():
    query_parameters = request.args

    url = query_parameters.get('url')

    if not (url):
        return page_not_found(404)

    return jsonify(
		pokemon=guessPokemon(url)
	)

app.run('0.0.0.0',8080)