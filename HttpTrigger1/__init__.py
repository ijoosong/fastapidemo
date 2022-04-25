import logging
import azure.functions as func
import nest_asyncio
import requests
import ast
from app_api import app  # Main API application
from asgi import AsgiMiddleware

nest_asyncio.apply()

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
    return func.HttpResponse(f"{output}")

  return {
      "name": pokemon,}

async def main(req: func.HttpRequest, context: func.Context, doc: func.Out[func.Document]) -> func.HttpResponse:
  # If you want to use the native func.AsgiMiddleware make sure to uncomment the line below and to remove or comment out the line below it.
  # Make sure you have an updated func core tools v3 or v4 minimum. Otherwise, use the hardcoded middleware.
  #  output = func.AsgiMiddleware(app).handle(req, context)
  output = AsgiMiddleware(app).handle(req, context)
  body = output.get_body()
  if body.startswith(b'{"_HttpResponse__status_code":200'):
    dict_str = body.decode("UTF-8")
    data = ast.literal_eval(dict_str)
    pokemon = ast.literal_eval(data['_HttpResponse__body'])

    if pokemon:
      doc.set(func.Document.from_dict(pokemon))
  
  #b'{"_HttpResponse__status_code":200,"_HttpResponse__mimetype":"text/plain","_HttpResponse__charset":"utf-8","_HttpResponse__headers":{},"_HttpResponse__body":"{\'name\': \'bulbasaur\', \'weaknesses\': [\'flying\', \'ice\', \'fire\', \'psychic\'], \'resistances\': [\'poison\', \'water\', \'bug\', \'ground\', \'fairy\', \'electric\', \'fighting\', \'grass\'], \'no_damage_from\': []}"}'
  return output
