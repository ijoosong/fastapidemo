from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
async def index():
  return {
      "info": "Try /pokemon/pikachu for a quick demo.",}

@app.get("/pokemon/{pokemon}")
async def get_types(pokemon: str,):
  pokemon_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon}')

  body = pokemon_response.json()
  types_for_pokemon = []

  for type in body['types']:
      types_for_pokemon.append(type['type']['name'])

  types_pokemon_double_damage_from = set()
  types_pokemon_half_damage_from = set()
  types_pokemon_no_damage_from = set()

  for type in types_for_pokemon:
      type_response = requests.get(f'https://pokeapi.co/api/v2/type/{type}')
      type_response_json = type_response.json()
      types_pokemon_double_damage_from.update(type['name'] for type in type_response_json['damage_relations']['double_damage_from'])
      types_pokemon_half_damage_from.update(type['name'] for type in type_response_json['damage_relations']['half_damage_from'])
      types_pokemon_no_damage_from.update(type['name'] for type in type_response_json['damage_relations']['no_damage_from'])

  types_pokemon_double_damage_from = types_pokemon_double_damage_from - types_pokemon_half_damage_from
  types_pokemon_double_damage_from = types_pokemon_double_damage_from - types_pokemon_no_damage_from
  
  output = {
      'name': pokemon,
      'weaknesses': list(types_pokemon_double_damage_from),
      'resistances': list(types_pokemon_half_damage_from),
      'no_damage_from': list(types_pokemon_no_damage_from)
  }

  if pokemon:
    return f"{output}"

  return {
      "name": pokemon,}