'''
Converts key values from scraped data from https://lifestyle.sapo.pt/sabores to the ones used in
the firestore database, and adds key 'vegan', to indentify if recipe is vegan or not.

Requires one or more file(s) with .jsonl extension and outputs to final/recipes.jsonl.

--Changes:

quantities -> quantidade
preparation -> preparação
Tempo -> tempo
Doses -> porção

+ vegan
'''


import os, json
import datetime

finalJson = 'final/recipes.jsonl'

total=0
with open(finalJson, 'a') as result:
    for filename in os.listdir(os.curdir):
        if filename.endswith(".jsonl") and filename is not finalJson: 
            print("Currently on: ")
            print(os.path.join(os.curdir, filename))

            with open(os.path.join(os.curdir, filename)) as f:
                i=1
                for line in f.readlines():
                    recipe = json.loads(line)

                    # Replace en keys by pt keys
                    try:
                        recipe['quantidade'] = recipe['quantities']
                        del recipe['quantities']
                    except:
                        pass

                    try:
                        recipe['preparação'] = recipe['preparation']
                        del recipe['preparation']
                    except:
                        pass

                    try:
                        recipe['tempo'] = recipe['Tempo']
                        del recipe['Tempo']
                    except:
                        pass

                    # Replace 'Doses' by 'porção
                    try:
                        recipe['porção'] = recipe['Doses']
                        del recipe['Doses']
                    except:
                        pass

                    # Add timestamp
                    #recipe['timestamp'] = datetime.datetime.now().strftime()

                    if 'Gastronomia' in recipe and 'Tipo de prato' in recipe:
                        if recipe['Gastronomia'] in "Vegetariana" or recipe['Tipo de prato'] in "Vegetariano":
                            recipe['vegan'] = True
                        else:
                            recipe['vegan'] = False

                    elif 'Gastronomia' in recipe:
                        if recipe['Gastronomia'] in "Vegetariana":
                            recipe['vegan'] = True
                        else:
                            recipe['vegan'] = False
                    
                    elif 'Tipo de prato' in recipe:
                        if recipe['Tipo de prato'] in "Vegetariano":
                            recipe['vegan'] = True
                        else:
                            recipe['vegan'] = False

                    else:
                        recipe['vegan'] = False

                    #print(json.dumps(recipe, ensure_ascii=False))

                    result.write(json.dumps(recipe, ensure_ascii=False)+"\n")
                    print("Done " + str(i))
                    i+=1
                    total+=1



            continue
        else:
            continue

print("Parsed " + str(total) + " recipes")