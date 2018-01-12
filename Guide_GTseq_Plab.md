##GTSeq protocol, Palumbi Lab edition

### Select SNPs of interest
 - create file with 2 columns: contig name, SNP location
 
### Create input file
 1) make file of contigs of interest (if you have duplicate contigs, keep them as duplicates)
 	
 2) Grab contigs of interest from assembly
	- extract_multiple_contigs_by_name.py assembly.fa contigs.txt single
	- outputs "contigs.fasta"

3) reformat as single line fasta file

`perl -pe '/^>/ ? print "\n" : chomp' contigs.fasta | tail -n +2 > contigs_oneline.fasta`


4) reformat contig name to be: species_contig-SNP

- from a text file with two columns: Contigname snp
`awk '{print $1,$2}' contig-snps.txt | sed 's/Contig/>Balanus_Contig/g' | sed ’s/TRINITY/>Balanus_TRINITY/g’ | sed 's/ /-/g' > contig-snps2.txt`

5) Make your fasta file into a single line
`awk '/^>/ {printf("%s%s\t",(N>0?"\n":""),$0);N++;next;} {printf("%s",$0);} END {printf("\n");}' < test.fasta > test_oneline.fasta`

6) Replace names and return to fasta format
`paste test_mod.txt test_oneline.fasta | awk '{print $1"\n"$3}' `

### Run Primer 3
 ` perl Primer3\_format_small.py GTseqinput.fasta | primer3_core -format_output | grep 'PRIMER' | grep -A1 -B1 'LEFT' | grep -v '^--$' > Species_primer3_output.txt
`

### Put Primer3 output into a spreadsheet 
`perl P3toSpreadsheet_eas.pl Primer3_output.txt Species_ > Species_GTseq_primers.txt`

### Create primer order sheet from Primer3 output
 