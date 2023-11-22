import requests
from Bio import Entrez
import time

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
api_key = '555d4ea04b06001e8407ed6607b25df63508'  # Tu API key
email = 'owo.xd.owo@gmail.com'  # Tu email

# Primera consulta para obtener el número total de IDs
initial_search_url = f"{base_url}esearch.fcgi?db=pubmed&term='plant metabolites'&retmax=0&retmode=json&api_key={api_key}"
initial_response = requests.get(initial_search_url).json()
total_ids = int(initial_response["esearchresult"]["count"])  # Número total de IDs disponibles

print(f"Total de IDs disponibles: {total_ids}")

all_ids = []
retmax = 1000  # Número de IDs a recuperar en cada lote

# Ajuste del bucle para recoger todos los IDs
for retstart in range(0, total_ids, retmax):
    search_url = f"{base_url}esearch.fcgi?db=pubmed&term='plant metabolites'&retmax={retmax}&retstart={retstart}&retmode=json&api_key={api_key}"
    
    search_response = requests.get(search_url).json()

    if "ERROR" in search_response["esearchresult"]:
        print(search_response["esearchresult"]["ERROR"])
        break

    current_ids = search_response["esearchresult"]["idlist"]
    all_ids.extend(current_ids)

    if len(current_ids) < retmax:
        break

print(len(all_ids), "IDs retrieved")

Entrez.email = email

# El resto del código para recopilar y procesar los abstracts sigue igual


def fetch_abstracts(pubmed_ids):
    details = {}
    batch_size = 10  # Tamaño del lote para la prueba

    for i in range(0, len(pubmed_ids), batch_size):
        handle = Entrez.efetch(db="pubmed", id=','.join(map(str, pubmed_ids[i:i+batch_size])), retmode="xml")
        records = Entrez.read(handle)
        
        for record in records['PubmedArticle']:
            article = record['MedlineCitation']['Article']
            pmid = record['MedlineCitation']['PMID']

            # Title
            title = article.get('ArticleTitle', 'No title available')
            
            # Year
            year = article['Journal']['JournalIssue']['PubDate'].get('Year', 'N/A')
            
            # Abstract
            abstract_text = article['Abstract']['AbstractText'][0] if 'Abstract' in article else "No abstract available."
            
            # Author Affiliations
            affiliations = []
            if 'AuthorList' in article:
                for author in article['AuthorList']:
                    if 'AffiliationInfo' in author:
                        affiliations.extend([info['Affiliation'] for info in author['AffiliationInfo']])
            affiliations = '; '.join(affiliations)
            
            details[pmid] = {
                'title': title,
                'year': year,
                'abstract': abstract_text,
                'affiliations': affiliations
            }

        time.sleep(5)  # Pausa entre cada lote

    return details

# Procesamiento por lotes de abstracts
abstracts = fetch_abstracts(all_ids)

with open("pubmed_results_test.txt", "w", encoding="utf-8") as f:
    for pmid, detail in abstracts.items():
        f.write(f"PMID: {pmid}\n")
        f.write(f"Title: {detail['title']}\n")
        f.write(f"Year: {detail['year']}\n")
        f.write(f"Abstract: {detail['abstract']}\n")
        f.write(f"Affiliations: {detail['affiliations']}\n")
        f.write("-" * 50 + "\n")
