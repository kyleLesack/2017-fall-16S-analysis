from bs4 import BeautifulSoup
import requests

# HTML Classes for LPSN Taxon Designations
STRAIN_CLASS = "genusspecies-subspecies" # Scrape strains using soup.find_all("span", class_="genusspecies-subspecies")

# CSS Selectors for LPSN Taxon Designations
SPECIES_SELECTOR = "span.genusspecies + span.genusspecies"
GENUS_SELECTOR = "br + span.genusspecies"
CANDIDATUS_SELECTOR=".candidatus-designation + .candidatus-name" # Grabs first part of Candidatus names
INVALID_SELECTOR=".genusspecies-quote + .genusspecies" # Grabs first part of Invalid Names

# Create BeautifulSoup Object
def getSoup(html):
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def getGenera(soup, selector=GENUS_SELECTOR):    # Obtain genera epithet elements from "genus species" names
    validGenusObjects = soup.select(selector)

    # Grab genera names
    genusNames = []
    for name in validGenusObjects:
        genusName = name.text.strip()
        if genusName and genusName[0].isupper(): # Genus names should be capitalized
            genusNames.append(genusName)
        else:
            print "Warning, the selected genus name " + genusName + " ignored due to likely false positive" 
    uniqueNames = getUnique(genusNames)    
    return uniqueNames

# Get species names, return a list of tuples, where each tuple is the genus species epithets
def getSpeciesSiblings(soup, selector=SPECIES_SELECTOR):
    # Obtain species epithet elements from "genus species" names
    speciesNamesObjects=soup.select(selector)

    # Grab species names
    names = [] 
    for species in speciesNamesObjects:
        speciesName = species.text.strip()
        if speciesName and speciesName[0].isupper():  # If capitalized, it is probably a genus epithet   
            print "Warning, the selected species name " + speciesName + " ignored due to likely false positive" 
        else:        
            genus = species.find_previous_sibling("span", class_="genusspecies")
            names.append((genus.text.strip(), species.text.strip()))
    uniqueSpecies = getUnique(names)
    return uniqueSpecies

# Method for Obtaining Strains, and their associated genus, species ranks
def getStrainSiblings(soup):
    strains = soup.find_all("span", class_="genusspecies-subspecies") 
    strainNames = []
    for strain in strains:
        species =  strain.find_previous_sibling("span", class_="genusspecies")
        genus = species.find_previous_sibling("span", class_="genusspecies")
        strain =  strain.find_next_sibling("span", class_="genusspecies")

        if (genus is None) or (species is None) or (strain is None):
            print "None Type found for: " + str(genusSpeciesStrain)
        else: 
            genusSpeciesStrain =  ( genus.contents, species.contents, strain.contents )

        strainNames.append(genusSpeciesStrain)
    
    return strainNames 

def getUnique(myList):
    seen = set()
    seen_add = seen.add
    return [ x for x in myList if not (x in seen or seen_add(x))]



def getCandidatus(soup,selector = CANDIDATUS_SELECTOR):  

    genus_names = [] 
    genus_species_names = []
    other_names = []

    candidatusNamesObjects = soup.select(CANDIDATUS_SELECTOR)
    for soupObj in candidatusNamesObjects:
        name = soupObj.text.encode('utf-8').strip() # Non-ascii character (zeta) in candidatus names causes a decoding error, need to encode explicitly
        splitName = name.split()
        if len(splitName) > 1: # Some candidatus genus species epithets are contained in separate elements, while others are a single space separated element
            genus_species_names.append(("Candidatus",splitName[0],splitName[1]))
        else:
            siblingCandidatus = soupObj.find_next_sibling("span", class_="candidatus-name")                
            if (siblingCandidatus):
                speciesName = siblingCandidatus.text.encode('utf-8').strip()
                genus_species_names.append(("Candidatus",name, speciesName ))
            elif name[0].isupper(): # If first letter capitalized, probably genus name           
                genus_names.append(("Candidatus",name))
            else:
                other_names.append(("Candidatus",name))

    alltogether = (genus_names, genus_species_names, other_names)
    return alltogether

def getInvalid(soup,selector = INVALID_SELECTOR):  

    genus_names = [] 
    genus_species_names = []
    other_names = []

    invalidNamesObjects = soup.select(INVALID_SELECTOR)
    for soupObj in invalidNamesObjects:
        name = soupObj.text.encode('utf-8').strip() # Non-ascii character (zeta) in candidatus names causes a decoding error, need to encode explicitly
        splitName = name.split()
        if len(splitName) > 1: # Some candidatus genus species epithets are contained in separate elements, while others are a single space separated element
            genus_species_names.append((splitName[0],splitName[1]))
        else:
            siblingInvalid = soupObj.find_next_sibling("span", class_="genusspecies")                
            if (siblingInvalid):
                speciesName = siblingInvalid.text.encode('utf-8').strip()
		if "\"" in speciesName:
		    speciesNameStripped= speciesName.strip("\"").split()[0].strip("\"")			
		    print "Warning, the species epithet contains the \" character. Epithet name: " + speciesName + "\n\n Stored name: " + speciesNameStripped
		    genus_species_names.append((name, speciesNameStripped))
		else:
                    genus_species_names.append((name, speciesName ))
            elif name[0].isupper(): # If first letter capitalized, probably genus name           
                genus_names.append(name)
            else:
                other_names.append(name)

    alltogether = (genus_names, genus_species_names, other_names)
    return alltogether


