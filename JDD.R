# Dataset generation :

# Copy Number per family :
Size=50 # Number of different families (DO NOT CHANGE IT)
Fams <- sample(x = seq(1:100),size=Size,replace=F) # Choose 50 families among 1 to 100 copies per family. 2 Families can't have the same CopyNumber.
Tot <- sum(Fams) # Total number of TE in the dataset created.

# Now choose the TE length of the dataset :
TEL=rexp(5000,0.0005) # Generate 5k TE lengths in an exponential law of parameter 0.0005.

trie <- function(Distr,min){
  
  while (min(Distr) <= min) {
    Distr <- setdiff(Distr,min(Distr))
  }
  return (Distr)
} # Function that delete all values inferior to a threshold of min in Distr.

trieMax <- function(Distr,max){
  
  while (max(Distr) >= max) {
    Distr <- setdiff(Distr,max(Distr))
  }
  return (Distr)
} # Function that delete all values superior to a threshold of max in Distr.

TEL <- trie(TEL,100)  # Delete all TE lengths below 100bp.
TEL <- setdiff(TEL,200) # Delete TE lengths of 200bp. For easier detection of New insertions later, not because of biological reasons.
TEL <- trieMax(TEL,15000) # Delete TE lengths over 15k bp.
### Now we have a set of lengths biologically correct.

# Pick a set of distances :
Dist=rexp(5000,0.0005) # Pick genomic distances between TEs in an exponential law of parameter 0.0005.

# Pick a set of divergences :
Div <- rnorm(n = 5000,mean = 7,sd = 4) # Pick 5k divergences in a normal law of mean 7 and sd 4.
Div <- trie(Div,0)  # Delete Divergences below or equal to 0.

# Pick some genomic GC contents :
GC <- rnorm(n=5000,mean=50,sd=20)   # Pick 5k GC, in a normal law of mean 50 and sd 20. 
GC <- trie(GC,0) # Delete GC below 0%
GC <- trieMax(GC,100)  # And GC over 100%

TEL <- sample(TEL,Tot)  # Sample n TE length corresponding to the number of TE in the genome choosen at the begining.
Div <- sample(Div,Tot) # Same for the diversity
Dist <- sample(Dist,Tot+1) # Same for the Distance, but n+1.
GC <- sample(GC,Tot+1) # Same for the genomic GC, but n+1.
# We pick Number of TEs +1 because in the genome generated we have n TEs for n+1 distances between TEs (Genome doesn't start and doesn't ends with a TE).

# Choose some random family names (50 because we choose 50 families at the begining) :
FamilyNames <- c("the","and","will","freedom","from","ring","dream","day","that","with","let","this","have","every","one","able","together","when","nation","all","mountain","shall","faith","free","today","its","men","state","children","little","black","white","made","god","new","sing","land","last","even","live","meaning","out","true","are","brotherhood","down","former","georgia","sons","heat")

# This function creates a family name list depending on the number of TE per family :
cree_Fam <- function(Fams,FamilyNames) {
  Liste <- as.factor(c())
  j=0
  for (i in Fams){
    j=j+1
    Liste <- c(Liste,rep(FamilyNames[j],i))
    
  }
  return(Liste)
}
Lite_Fam <- cree_Fam(Fams,FamilyNames)


# Write the dataset is different files :
TEs <- data.frame(Diversity = Div, Length=round(TEL), Fam = Lite_Fam) # Dataframe with the description of the TEs
write.table(file = "TEs.csv",TEs,sep = "\t",quote = F,row.names = F) 

Inter <- data.frame(Dist = round(Dist), GCcount=GC) # Dataframe with the description of the "genomic" regions.
write.table(file = "Inter.csv",Inter,sep = "\t",quote = F,row.names = F)

maxf <- c()
vus <- c()
# Retrieve the longest TE in each family :
for (i in FamilyNames){
  if (!(i %in% vus)){
    Ma <- max(TEs[TEs[,"Fam"]==i,"Length"])
    maxf<- rbind(maxf,c(Ma,i))
    vus <- c(vus,i)
  }
}
maxf <- as.data.frame(maxf) # Creaate a frame
maxf <- maxf[order(maxf[,2],decreasing=F), ]  # Class the TE insertions by name.
Totalet <- as.numeric(as.vector(maxf[,1]))
Assoc <- cbind(as.data.frame(table(Lite_Fam)),Totalet)  # Create a dataframe with Family / CopyNumber / longest TE.
write.table(file= "Assoc.csv",Assoc,sep="\t",quote=F,row.names=F)

### Bug report :
# If Tot > Number of TE for biological caracteristics.