# Hadoop MapReduce : analyse de ventes avec Python

Analyse d'un fichier de plus de 4 millions de transactions de vente avec **MapReduce**, via **Hadoop Streaming** et des scripts **Python 3**.

Rapport de résultats : [docs/rapport.pdf](docs/rapport.pdf)

## Données

Le fichier `purchases.txt` contient une transaction par ligne, avec 6 champs séparés par des tabulations :

```
date    heure    magasin    catégorie    montant    paiement
2012-12-31    17:59    Norfolk    Toys    164.34    MasterCard
```

Le fichier est volumineux et n'est pas inclus dans ce dépôt. Place-le à la racine pour les tests locaux, ou sur HDFS pour les jobs Hadoop.

## Principe

```mermaid
flowchart LR
    A[purchases.txt] --> B[Mapper]
    B --> C[Shuffle et tri par clé]
    C --> D[Reducer]
    D --> E[Résultat]
```

Le mapper extrait une clé (magasin ou catégorie) et le montant. Hadoop regroupe les paires par clé, puis le reducer les agrège.

## Structure

```
src/
├── mapper_store.py     # magasin    <TAB> montant
├── mapper_item.py      # catégorie  <TAB> montant
├── reducer_sum.py      # somme par clé
├── reducer_max.py      # maximum par clé
└── reducer_total.py    # total des ventes et nombre de transactions
docs/
├── rapport.pdf
└── images/
```

| Analyse | Mapper | Reducer |
|---|---|---|
| Ventes par magasin | `mapper_store.py` | `reducer_sum.py` |
| Ventes par catégorie | `mapper_item.py` | `reducer_sum.py` |
| Vente maximale par magasin | `mapper_store.py` | `reducer_max.py` |
| Total général et nombre de ventes | `mapper_store.py` | `reducer_total.py` |

## Utilisation

**Test local sur un échantillon :**

```bash
head -50 purchases.txt | python3 src/mapper_store.py | sort | python3 src/reducer_sum.py
```

![Test local](docs/images/test-local.png)

**Exécution sur Hadoop :**

```bash
hdfs dfs -mkdir -p myinput
hdfs dfs -put purchases.txt myinput/

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -files src/mapper_store.py,src/reducer_sum.py \
  -mapper "python3 mapper_store.py" \
  -reducer "python3 reducer_sum.py" \
  -input myinput/purchases.txt \
  -output joboutput_store_sales

hdfs dfs -cat joboutput_store_sales/part-00000
```

Pour les autres analyses, change les scripts selon le tableau et le dossier de sortie (il ne doit pas exister). Le chemin du JAR dépend de l'installation Hadoop.

## Résultats

| Question | Résultat |
|---|---|
| Ventes du magasin de Buffalo | 10 001 941,19 |
| Ventes de la catégorie Toys | 57 463 477,11 |
| Ventes de la catégorie Consumer Electronics | 57 452 374,13 |
| Vente maximale à Reno / Toledo / Chandler | 499,99 / 499,98 / 499,98 |
| Total général des ventes | 1 034 457 953,26 |
| Nombre total de transactions | 4 138 476 |

![Ventes par catégorie](docs/images/ventes-categories.png)

![Total des ventes](docs/images/total-ventes.png)

## Limites

- Les sommes en `float` produisent des artefacts (ex. `168.70999999999998`) : utiliser `decimal.Decimal`.
- Un montant non numérique fait planter le mapper (pas de `try/except`).
- Pas de combiner, donc plus de trafic réseau lors du shuffle.
- `reducer_total.py` suppose un seul reducer.

## Auteur

Abdessamad Ait brahim, [@abdessamadaitbrahim](https://github.com/abdessamadaitbrahim)