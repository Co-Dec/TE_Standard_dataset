# TE_Standart_dataset
A code to create standart dataset to assess TE detection performances.
Version 1.0-2017-04

-----------------
## Author : 
DECHAUD Corentin

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
git clone https://github.com/Co-Dec/TE_Standart_dataset
cd
```

-----------------
## Create your dataset :
cd in the directory where you want to create the dataset.
```
/my/path/to/repository/TE_Standart_dataset.sh
```

-----------------
## General description :
Assessing performances of different tools requires to compare them on the same data. Here I developped a program to create this kind of dataset allowing performances comparison.

**The whole pipeline is run lauched just by running `TE_Standart_dataset.sh`**

### First step : Generating parameters
Script : `JDD.R`

Randomly picks 50 TE copy per family between 1 and 100 without replacement. Everytime you run the program you will get 50 different TE families, but without the same copy number per family everytime. For example : 

|       | Run1 | Run2 | Run3 | Run4 |
|:-----:|:----:|:----:|:----:|:----:|
|  Fam1 |  21  |  52  |  75  |   3  |
|  Fam2 |   6  |  29  |  33  |  47  |
|  ...  |  ... |  ... |  ... |  ... |
| Fam50 |  41  |  19  |   8  |   2  |
| **Total** | **2565** | **2956** | **2352** | **2413** |

Retrieves the total number of TE doing the sum for the entire family.

Randomly picks the same number of TE sizes, TE divergence, Distances between TEs, and GC counts of sequences between TEs in biological distributions.

We now have a number of TE (+/- 2500) divided in 50 TE families, for each we have a **size**, a **divergence**, a **GC count**, and a **distance**. In fact we pick N+1 distance and GC because there are N TEs and N+1 genomic regions.

Writes those descriptions in `inter.csv` , `TEs.csv` , and `Assoc.csv`.

### Second Step : Generating TE dataset
Script : `TE_dataset.py`

See file : *Shemas_variations_e.png*
  - Each TE length picked is associated to a TE family respecting copy number per family.
 (Ex : If family 1 has 21 copies, then the 21 first lengths would be associated to family 1.)
  - Retrieve the longest length of each family and create a random sequence. (We suppose that this is the ancestral copy of the family)
  - Pick a random position in this length for each TE of the family.
  - Copy the ancestral sequence in the TE we are creating from the position choosen randomly with a length equal to the size picked.
  - Apply the divergence to the sequence to create the new TE.
  - Do this again for each family.

### Third step : Create the genomes
Script : `Rand_vargen.py`

See *Rand_vargen.png*

**Creates the genome data files :**
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
  * Special files :
    * Genome annotation with 1 out of 2 TE, showing TE present in it, and where TEs deleted are supposed to be. Expected deleted TE are in 200bp intervals present in 1 out of 2 lines.
    * 2 specbed files, that can be needed to assess TIDAL software.
  
**Genome description (CSV) :**

TE Name / Start / End / Divergence / Size / Distance Before / Distance After / GC Before / GC After / CopyNumber / Family

### Fourth step : Using the dataset
See *Use.png*

* Assess *reference* insertion detection (Shared between reference and unknown genome, or deleted ones, present in the reference and absent in the unknown genome) :
  * Use the `GenTot.fasta` as a reference genome. If the software you are using needs a masked one, you can use `GenMask.fasta`.
  * Generate your reads on `GenDel.fasta`.
  * Start your program.
  * Evaluate the quality of the results using the bed files corresponding to what is expected.
  * You can check if there is a bias in the TE found or missed by the software using the description files `Anot.csv` and `AnotDel.csv`.
  
* Asses *new* insertion detection (Absent from reference, but present in the unknown genome) :
  * Use `GenDel.fasta` as a reference genome. If the software you are using needs a masked one, you can use `DelMask.fasta`.
  * Generate your reads on `GenTot.fasta`.
  * Start your program.
  * Evaluate the quality of the results using the bed files corresponding to what is expected. I recommend the use of `refdel.new.bed`. It describes the *reference* genome with half of the TE, and showing where new TE are expected.
  * You can check if there is a bias in the TE found or missed by the software using the description files `Anot.csv` and `AnotDel.csv`.
 
 **Note** :
 
 I recommend to use [art_illumina](https://www.niehs.nih.gov/research/resources/software/biostatistics/art/) to generate your reads on the artificial genomes.

Using only one genome permits to assess TE presence / absence detection or the precision of the position where the TE is found, but not TE frequence estimations. You can generate your reads on 4 `GenTot.fasta` and 1 `GenDel.fasta` to see if the frequency found is 80% for example.

-----------------
## Known issues :
  - When running this program, due to random sampling of lengths, sometimes, TEs with negative lengths are created. It doesn't matter because they are deleted, but if too many of them are, the program can stop. It is very rare and you just have to run it again. It still can be a problem if you run it in a pipeline thousand times. Will be fixed soon.

-----------------
## Contacts :
DECHAUD Corentin

E-mail : corentin.dechaud@gmail.com
