## GTSeq protocol for the Palumbi Lab

### This is a modified pipeline from Campbell et al.'s 2014 Genotypying-in-Thousands by Sequencing
Reference: http://onlinelibrary.wiley.com/doi/10.1111/1755-0998.12357/full

Campbell's github: https://github.com/GTseq/GTseq-Pipeline
 
### Create Primer3 input file
This is complicated! Be careful that your files are formatted correctly. 

 1) Make a text file of contigs of interest (if you have duplicate contigs, keep them as duplicates)
 	
 2) Grab these contigs of interest from your assembly
 
`extract_multiple_contigs_by_name.py assembly.fa contigs_names.txt single`

- contig_names.txt is a list of the contig names that include a SNP of interest. 
- This outputs "contigs.fasta"

2a) If you have TRINITY contig name formats in your file, you need to do some extra editing:

- remove extra information from header
`awk '{print $1}' contigs.tmp.fasta` 

3) Reformat contigs.fasta to be a single line fasta file

`awk '/^>/ {printf("%s%s\t",(N>0?"\n":""),$0);N++;next;} {printf("%s",$0);} END {printf("\n");}' < contigs.fasta > contigs_oneline.txt`

4) Reformat contig names to be what the GTseq pipeline likes (i.e. Species_contig-SNP)

4a) Generate a text file of your SNPs of interest with two tab delimited columns (Contig SNP)
- for ex: Contig1 3
- I call this file contigs-snps.txt below
- This MUST be in the same order as the contigs.fasta file you generated above!

4b) Reformat contig-snps.txt to be Species_Contig-SNP:  
If you have Contig & TRINITY names:
`awk '{print $1,$2}' contig-snps.txt | sed 's/Contig/>YourSpeciesName_Contig/g' | sed 's/TRINITY/>YourSpeciesName_TRINITY/g' | sed 's/ /-/g' > GTSeq_names.txt`

If you have only Contig names:
`awk '{print $1,$2}' contig-snps.txt | sed 's/Contig/>YourSpeciesName_Contig/g' | sed 's/ /-/g' > GTSeq_names.txt`

5) Replace with GTseq names in your contigs_oneline.txt and return to fasta format
- This is a simple paste. Your file of names and your contigs.fasta assembly file must be in the same order!

`paste GTSeq_names.txt contigs_oneline.txt | awk '{print $1"\n"$3}' > Primer3_input.fasta`

### Run Primer3
 ` perl Primer3_format_small.pl Primer3_input.fasta | primer3_core -format_output | grep 'PRIMER' | grep -A1 -B1 'LEFT' | grep -v '^--$' > Primer3_output.txt`

### Export Primer3 output into a spreadsheet 

- This takes native output from primer3 and formats for ordering primers from IDT in 96w format. Also, adds read1 seq tag to fwd sequence and read2 seq tag to rev sequence.

`perl P3toSpreadsheet_eas.pl Primer3_output.txt Species_ > GTseq_primers.txt`

### Create primer order sheet from Primer3 output
 ` perl P3toIDT_eas.pl GTseq_primers Species_ > GTseq_primer_order.txt`
 
### More coming... 