# TE_Standart_dataset
A code to create standart dataset to assess TE detection performances.
Version 1.0

-----------------
## Author : 
DECHAUD Corentin Feb-April 2017.

@E-mail : corentin.dechaud@gmail.com

-----------------
## Dependencies :
  - Python3 :
You need python3 to run those scripts. If you don't have it you can install it by running :
```
sudo apt-get install python3
```
  - Argparse module for python3 :
 You can [download](https://pypi.python.org/pypi/argparse#downloads) argparse here.
 
  - re module for python3.
  
  - R version >= 3.2.3 
  
-----------------
## Install :
First clone this repository on your computer.

```
mkdir /my/path/to/repository
cd /my/path/to/repository
git clone https://github.com/TE_Standart_dataset
cd
```
cd in the directory where you want to create the dataset.
```
/my/path/to/repository/TE_standart_dataset.sh
```

-----------------
## General description :
Assessing performances of different tools requires to compare them on the same data. Here I developped a program to create this kind of dataset allowing performances comparison.
### First step : Generating parameters
Script : `JDD.R`

Randomly picks 50 TE number per family between 1 and 100 without replacement.
Randomly picks the same number of TE sizes, TE diversity, Distances between TEs, and GC counts in biological distributions.
Writes those descriptions in `inter.csv` , `TEs.csv` , and `Assoc.csv`.

### Second Step : Generating TE dataset
Script : `TE_dataset.py`


See file : *Shemas_variations_eng.png*
  - Each length picked is associated to a TE family respecting copy number per family.
 (Ex : If family 1 has 21 copies, then the 21 first lengths would be associated to family 1.)
  - Retrieve the longest length of each family and create a random sequence. (We suppose that this is the ancestral copy)
  - Pick a random position in this length for each TE of the family.
  - Apply the divergence to the ancentral TE to create the new TE, starting at the position picked with his length.
  - Do this again for each family.

### Third step : Create the genomes
Script : `Rand_vargen.py`

Creates the genome data files :
  * Total genome files :
    * Genome with all TE insertions created. (Fasta file).
    * Genome with all TE insertions created masked. (Fasta file, masked with "N").
    * Genome annotation with all TE insertion created. (Bed file).
    * Genome description with all TE insertion created. (CSV file).
  * Depleted genome files :
    * Genome with 1 out of 2 TE insertions created. (Fasta file).
    * Genome with 1 out of 2 TE insertions created masked. (Fasta file, masked with "N").
    * Genome annotation with 1 out of 2 TE insertion created. (Bed file).
    * Genome description with 1 out of 2 TE insertion created. (CSV file). 

Genome description (CSV) :

TE Name / Start / End / Divergence / Size / Distance Before / Distance After / GC Before / GC After / CopyNumber / Family

## Known issues :
  - When running this program, due to random sampling of lengths, sometimes, TEs with negative lengths are created. It doesn't matter because they are deleted, but is too many of them are, the program can stop. It is very rare and you just have to run it again. It still can be a problem if you run it in a pipeline thousand times.

## Contacts :
DECHAUD Corentin
E-mail : corentin.dechaud@gmail.com
