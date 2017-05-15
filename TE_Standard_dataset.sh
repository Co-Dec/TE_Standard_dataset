#!/bin/bash
BASEDIR=$(dirname "$0")


# Version 1.0
#Vars:
TE_Fasta=MyTEs.fasta			# FASTA File of the TEs.
Tot_Fasta=GenTot.fasta			# Generated genome with all of the insertions. FASTA Format.
Tot_Mask=GenMask.fasta			# Masked generated genome with all of the insertions. FASTA Format.
Tot_Bed=BedTot.bed				# Annotation of the generated genome. BED Format.
Tot_anot=AnotTot.csv			# Insertion description. CSV Format.

Del_Fasta=GenDel.fasta			# Generated genome with 1 out of 2 insertion. FASTA Format.
Del_Mask=DelMask.fasta			# Masked generated genome with 1 out of 2 insertion. FASTA Format.
Del_Bed=BedDel.bed				# Annotation of the 1 out of 2 genome. BED Format.
Del_anot=AnotDel.csv			# Insertion description. CSV Format.

# Run caracteristics generation :
Rscript $BASEDIR/JDD.R
# 3 Files are generated :
# 	- TEs.csv : Diversity / Length / Family of each TE.
#	- Inter.csv : Distance / GC Count of each genomic region between 2 TE.
#	- Assoc.csv : Family name / Frequency / Longest TE in the family.

# Generate the TE datasets :
$BASEDIR/TE_dataset.py -TE TEs.csv -Assoc Assoc.csv -out $TE_Fasta

# Shuffle step : Shuffle the TE generated not to have the same family together.

# Retrieve the fasta headers :
grep '^>' $TE_Fasta > Headers.fa

# How many sequences :
Co=`grep -c '^>' Headers.fa`

# Shuffle the headers :
shuf -n $Co Headers.fa > Rand_Headers.fa

# Delete the ">" + Replace the blanks by a special caracter never used elsewhere in the headers and the original file.
sed -i -e "s/>//g" Rand_Headers.fa
sed -i -e "s/ /FrodoBagginsMyFriend/g" Rand_Headers.fa
sed -i -e "s/ /FrodoBagginsMyFriend/g" $TE_Fasta

# Retrieve the sequences if the TE file corresponding to the randomly moved headers :
cat Rand_Headers.fa | xargs -n 1 samtools faidx $TE_Fasta > tmp
mv tmp $TE_Fasta

# Change the special caracter to a blank again :
sed -i -e "s/FrodoBagginsMyFriend/ /g" $TE_Fasta
rm *.fai
rm Headers*
rm Rand_Headers*

# Run génération génome et anots:
$BASEDIR/Rand_vargen.py -TE $TE_Fasta -Inter Inter.csv -out $Tot_Fasta -mask $Tot_Mask -bedout $Tot_Bed -Anot $Tot_anot -outDel $Del_Fasta -maskDel $Del_Mask -bedoutDel $Del_Bed -anotDel $Del_anot
