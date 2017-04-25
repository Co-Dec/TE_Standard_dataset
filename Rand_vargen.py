#!/usr/bin/python3
# -*- coding: Utf-8 -*-
import random 
import argparse 
import re
import os

parser = argparse.ArgumentParser(description="Create a genome dataset to assess TE detecting performances.")
parser.add_argument("-TE",help="TE fasta file. (FASTA)",required=True)
parser.add_argument("-Inter",help="Dist and GC. (CSV)",required=True)
parser.add_argument("-out",help="Output genome with all TEs. (FASTA)",default="Out.fasta")
parser.add_argument("-mask",help="Output masked genome with all TEs. (FASTA)",default="masked.fasta")
parser.add_argument("-bedout",help="Output annotation of total genome. (BED)",default="out.bed")
parser.add_argument("-Anot",help="Output description of total genome. (CSV)",default="Anot.csv")

parser.add_argument("-outDel",help="Output genome with 1 out of 2 insertions. (FASTA)",default="OutDel.fasta")
parser.add_argument("-maskDel",help="Output masked genome with 1 out of 2 insertions. (FASTA)",default="maskedDel.fasta")
parser.add_argument("-bedoutDel",help="Output annotation of 1 out of 2 genome. (BED)",default="outDel.bed")
parser.add_argument("-anotDel",help="Output description of 1 out of 2 genome. (CSV)",default="AnotDel.csv")

args = parser.parse_args()


def pick_nt(GC):
	"""
	Pick a random nucleotide depending on GC content
	"""
	RGC = random.random()
	if GC < RGC :
		if random.randint(0,1) == 0 :
			return ("A")
		else :
			return ("T")
	else :
		if random.randint(0,1) == 0 :
			return ("G")
		else :
			return ("C")

class intervale(object):
	"""
	Intervale object :
		- Distance
		- GC content
	"""
	def __init__(self,Dist,GC):
		
		self.Dist=int(Dist)
		self.GC=float(GC)/100
	
	def __str__(self):
		return ("Dist = " + str(self.Dist) + "\nGC = " + str(self.GC))
		
	def genere_seq(self):
		"""
		Create the genomic locus sequence.
		"""
		seq=[]
		pos=0
		for i in range(self.Dist):
			pos+=1
			nt = pick_nt(self.GC)
			seq.append(nt)
			if pos % 80 ==0:
				seq.append("\n")
		self.seq = "".join(seq)
	
	
class TE_post_inser(object):
	"""
	TE object :
		- Size
		- Copy number
		- Diversity
		- Family
		- FBti
	"""
	def __init__(self,Size,Cp,Div,Fam,FBti):
		self.Size=Size
		self.Cp=Cp
		self.Div=Div
		self.Fam=Fam
		self.FBti=FBti
	
		
def main():
	# For each interTE region :
	Inters = open(args.Inter,"r")
	Liste_Inters=[]
	for line in Inters :
		Loc = line.split("\t")
		if Loc[0] != "Dist":
			# Create interval object :
			MyInter = intervale(Loc[0],Loc[1].replace("\n",""))
			# Generate his sequence :
			MyInter.genere_seq()
			#Add to the list :
			Liste_Inters.append(MyInter)
	# Now we have a interTE list.
	
	
	
	
	# write headers in outputs :
	out = open(args.out,"w")
	out.write(">3R\n")
	mask=open(args.mask,"w")
	mask.write(">3R\n")
	
	#Delted genome
	outDel=open(args.outDel,"w")
	outDel.write(">3R\n")
	maskDel=open(args.maskDel,"w")
	maskDel.write(">3R\n")
	
	# Open TE FASTA for reading  and for each TE :
	TE=open(args.TE,"r")
	
	Cptr=0
	for line in TE :
		if line[0] == ">" : # If I find a new TE : write an interTE region
			if len(Liste_Inters[Cptr].seq.replace("\n","")) % 80 == 0 :
				out.write(Liste_Inters[Cptr].seq)
				mask.write(Liste_Inters[Cptr].seq)
				outDel.write(Liste_Inters[Cptr].seq)
				maskDel.write(Liste_Inters[Cptr].seq)
			else :
				
				out.write(Liste_Inters[Cptr].seq+"\n")
				mask.write(Liste_Inters[Cptr].seq+"\n")
				outDel.write(Liste_Inters[Cptr].seq+"\n")
				maskDel.write(Liste_Inters[Cptr].seq+"\n")
					
			Cptr+=1
		else : # Else write a TE or a masked TE :
			out.write(line)
			mask.write(line.replace("A","N").replace("T","N").replace("G","N").replace("C","N"))
			if Cptr % 2 == 1 : # Only 1 out of 2 for deleted files :
				outDel.write(line)
				maskDel.write(line.replace("A","N").replace("T","N").replace("G","N").replace("C","N"))
	
	# When all of the TEs are done write the last interTE region :	
	out.write(Liste_Inters[Cptr].seq)
	mask.write(Liste_Inters[Cptr].seq)
	outDel.write(Liste_Inters[Cptr].seq)
	maskDel.write(Liste_Inters[Cptr].seq)
	out.close()
	mask.close()
	TE.close()
	Inters.close()
	
	
	# Read the TEs again but to write the annotation and description files :
	TE=open(args.TE,"r")
	bed=open(args.bedout,"w")
	anot=open(args.Anot,"w")
	anot.write("FBti\tStart\tEnd\tDiv\tSize\tDist1\tDist2\tGC1\tGC2\tCopyN\tFam\n")
	
	bedDel=open(args.bedoutDel,"w")
	anotDel=open(args.anotDel,"w")
	anotDel.write("FBti\tStart\tEnd\tDiv\tSize\tDist1\tDist2\tGC1\tGC2\tCopyN\tFam\n")
	
	refdelnew=open("refdel.new.bed","w")
	
	TidalDel=open("tidaldel.specbed","w")
	TidalTot=open("tidaltot.specbed","w")
	
	InterNum=0
	Disttot=0
	DistDel=0
	for line in TE :
		if line[0] == ">" :
			# Retrieve the TE caracteristics present in the title line !
			regex=re.compile('; length=(.*); div=',re.I)
			match=regex.search(line)
			Size =  match.group(1) # OK
			
			regex=re.compile('; nbcop=(.*);',re.I)
			match=regex.search(line)
			Copy =  match.group(1)	# OK
			
			regex=re.compile('; div=(.*); nbcop=',re.I)
			match=regex.search(line)
			Div =  match.group(1)# OK
			
			regex=re.compile('; name=(.*){}; dbxref=',re.I)
			match=regex.search(line)
			Fam =  match.group(1)# OK
			
			regex=re.compile('>(.*) type=transposable_element;',re.I)
			match=regex.search(line)
			FBti =  match.group(1)# OK
			
			regex=re.compile('; loc=(.*):',re.I)
			match=regex.search(line)
			Chr =  match.group(1)# OK
			
			## Write the caracteristics in the outputs :
			
			# Distance before and after the TE :
			DistPrec=Liste_Inters[InterNum].Dist
			DistAp=Liste_Inters[InterNum+1].Dist
			
			# GC before and after the TE :
			GCPrec=Liste_Inters[InterNum].GC
			GCAp=Liste_Inters[InterNum+1].GC
			
			# Distance from the begining :
			Disttot+=DistPrec
			
			# Add a line to the bedfile for this TE :
			bed.write(Chr+"\t"+str(Disttot+1)+"\t"+str(int(Disttot)+int(Size))+"\t"+FBti+"|"+Fam+"\n")
			
			# Special bedfile for tidal :
			TidalTot.write(Chr+"\t"+str(Disttot+1)+"\t"+str(int(Disttot)+int(Size))+"\t"+FBti+"\t"+Fam+"\t"+"LaFamille\n")
			
			# Genome description :
			anot.write(str(FBti)+"\t"+str(Disttot+1)+"\t"+str(int(Disttot)+int(Size))+"\t"+str(Div)+"\t"+str(Size)+"\t"+str(DistPrec)+"\t"+str(DistAp)+"\t"+str(GCPrec)+"\t"+str(GCAp)+"\t"+str(Copy)+"\t"+str(Fam)+"\n")
			
			DistDel+=DistPrec
			
			# write her only for 1 out of 2 TEs :
			if InterNum % 2 == 0 :
				TidalDel.write(Chr+"\t"+str(DistDel+1)+"\t"+str(int(DistDel)+int(Size))+"\t"+FBti+"\t"+Fam+"\t"+"LaFamille\n")
				bedDel.write(Chr+"\t"+str(DistDel+1)+"\t"+str(int(DistDel)+int(Size))+"\t"+FBti+"|"+Fam+"\n")
				refdelnew.write(Chr+"\t"+str(DistDel+1)+"\t"+str(int(DistDel)+int(Size))+"\t"+FBti+"|"+Fam+"\n")
				anotDel.write(str(FBti)+"\t"+str(DistDel+1)+"\t"+str(int(DistDel)+int(Size))+"\t"+str(Div)+"\t"+str(Size)+"\t"+str(DistPrec)+"\t"+str(DistAp)+"\t"+str(GCPrec)+"\t"+str(GCAp)+"\t"+str(Copy)+"\t"+str(Fam)+"\n")
				DistDel+=int(Size)
			else :
				refdelnew.write(Chr+"\t"+str(DistDel-99)+"\t"+str(DistDel+100)+"\t"+FBti+"|"+Fam+"\n")
			
			Disttot+=int(Size)
			InterNum+=1
			
			
			
	bed.close()
	TE.close()
	anot.close()
	TidalDel.close()
	TidalTot.close()
if __name__ == "__main__":
    main()
