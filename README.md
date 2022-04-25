# README

## Functions FastAPI

This is a quick and easy demo application using FastAPI, Azure Functions, and CosmosDB
In order to get this working (assuming you're using VSCode):

1. Clone the repo! Use whatever git client you want.
2. Make sure you have an updated coretools (v3 or v4)
3. You'll notice in function.json in HttpTrigger1 has this:
     "type": "cosmosDB",
      "direction": "out",
      "name": "doc",
      "databaseName": "pokemondb",
      "collectionName": "data",
      "createIfNotExists": "true",
      "connectionStringSetting": "AzureCosmosDBConnectionString"
    - Make a CosmosDB account (any name can go here)
    - Make a db in that account (here, it's called pokemondb)
    - Find out what the "AzureCosmosDBConnectionString" is by going to Keys (you'll see it on the left hand side under *Settings*)
    - Copy the PRIMARY CONNECTION STRING
4. Create a file called "local.settings.json"
5. Insert in it something like this:
{
    "IsEncrypted": false,
    "Values": {
        "AzureWebJobsStorage": "",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "AzureCosmosDBConnectionString": "This is where your connection string you copied above goes."
    }
}

Try running it now with F5!  You might need to configure your .venv (on pc, ./.venv/scripts/activate and on mac ./.venv/source/activate (or something like that))
If you want to deploy it to Azure, use the functions extension :)

## Standalone FastAPI

1. This is much easier! First make sure you are in a venv
2. Do a pip install -r requirements.txt
3. CD into /fastapiapp
4. Run the command "uvicorn main:app --reload"
5. Check out localhost:8000/