
import json
import os

import pandas as pd
import requests

from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)

SETS_URL = 'https://api.pokemontcg.io/v2/sets'


@asset
def pokemon_tcg_sets_summary() -> MaterializeResult:
    query_params = {
        'selected': 'id,name,releaseDate',
        'orderBy': 'releaseDate'
    }

    more_pages = True
    page = 1
    sets = []
    while more_pages:
        response = requests.get(
            SETS_URL, params={**query_params, 'page': page})
        response.raise_for_status()
        data = response.json()
        sets.extend(data['data'])
        more_pages = data['page'] * data['pageSize'] < data['totalCount']
        page += 1

    os.makedirs("data", exist_ok=True)
    with open("data/pokemon_tcg_sets.json", "w") as f:
        json.dump(sets, f)

    return MaterializeResult(
        metadata={
            "num_records": len(sets),
            "preview": MetadataValue.md(pd.DataFrame(sets).head().to_markdown())
        }
    )


@asset(deps=[pokemon_tcg_sets_summary])
def pokemon_tcg_sets(context: AssetExecutionContext) -> None:
    with open("data/pokemon_tcg_sets.json") as f:
        sets_summary = json.load(f)

    sets = []
    for set_summary in sets_summary[:10]:
        response = requests.get(f"{SETS_URL}/{set_summary['id']}")
        response.raise_for_status()
        set_data = response.json()['data']
        sets.append(set_data)
        context.log.info(f"Loaded set {set_data['name']}")

    df = pd.DataFrame(sets)
    df.to_csv("data/pokemon_tcg_sets.csv", index=False)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )


@asset(deps=[pokemon_tcg_sets])
def pokemon_tcg_sets_images(context: AssetExecutionContext) -> None:
    with open("data/pokemon_tcg_sets.csv") as f:
        sets = pd.read_csv(f)

    #  subset to 1 rows
    sets = sets.head(1)

    os.makedirs("data/images", exist_ok=True)
    for index, row in sets.iterrows():
        context.log.info(row)
        context.log.info(eval(row['images'])['logo'])
        response = requests.get(eval(row['images'])['logo'])
        response.raise_for_status()
        with open(f"data/images/{row['id']}.png", "wb") as f:
            f.write(response.content)
        context.log.info(f"Downloaded image for set {row['name']}")

    import base64
    return MaterializeResult(
        metadata={
            "plot": MetadataValue.md(f"![img](data:image/png;base64,{base64.b64encode(response.content).decode('utf-8')})")
        }
    )
