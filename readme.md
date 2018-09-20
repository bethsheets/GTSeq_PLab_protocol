## GTSeq protocol for the Palumbi Lab

### This is a modified pipeline from Campbell et al.'s 2014 Genotypying-in-Thousands by Sequencing
Reference: http://onlinelibrary.wiley.com/doi/10.1111/1755-0998.12357/full

Campbell's github: https://github.com/GTseq/GTseq-Pipeline
 
### Create Primer3 input file

 1) Generate a text file of your SNPs of interest with two tab delimited columns (Contig SNP)

- for ex: 
`Contig1 3`
- I refer to this file as contigs-snps.txt in the protocol.
 	
2) Grab your contigs of interest from your assembly. 

- You can generate a list of contigs from the contigs-snps.txt file above
`awk '{print $1}' contigs-snps.txt > contig_names.txt`

- If you have multiple SNPs from the same contig, keep these duplicate contig IDs.
 
- Grab contigs from your assembly with:
`python extract_multiple_contigs_by_name.py assembly.fa contig_names.txt single`

- outputs all contigs into a single file (alternatively, you could use multiple to get a different file for each contig).
- This outputs "contigs.fasta"

IMPORTANT: If you have TRINITY contig name formats in your file, you need to do some extra editing before moving on:

- remove extra information from header
`awk '{print $1}' contigs.fasta > contigs2.fasta` 

3) Reformat contigs2.fasta to be a single line fasta file

`awk '/^>/ {printf("%s%s\t",(N>0?"\n":""),$0);N++;next;} {printf("%s",$0);} END {printf("\n");}' < contigs2.fasta > contigs_oneline.txt`

4) Reformat fasta headers to be what the GTseq pipeline likes (i.e. Species_contig-SNP)

- use your contigs-snps.txt file from above
- Your contigs-snps.txt and contigs2.fasta files MUST be in the same order.
- Reformat contigs-snps.txt to be Species_Contig-SNP:  

If you have Contig & TRINITY names:
`awk '{print $1,$2}' contigs-snps.txt | sed 's/Contig/>YourSpeciesName_Contig/g' | sed 's/TRINITY/>YourSpeciesName_TRINITY/g' | sed 's/ /-/g' > GTSeq_names.txt`

If you have only Contig names:
`awk '{print $1,$2}' contig-snps.txt | sed 's/Contig/>YourSpeciesName_Contig/g' | sed 's/ /-/g' > GTSeq_names.txt`

5) Replace headers with GTseq names in your contigs_oneline.txt and return to fasta format

`paste GTSeq_names.txt contigs_oneline.txt | awk '{print $1"\n"$3}' > Primer3_input.fasta`

### Run Primer3
 ` perl Primer3_format_small.pl Primer3_input.fasta | primer3_core -format_output | grep 'PRIMER' | grep -A1 -B1 'LEFT' | grep -v '^--$' > Primer3_output.txt`

### Export Primer3 output into a spreadsheet 

- This takes native output from primer3 and formats for ordering primers from IDT in 96w format. Also, adds read1 seq tag to fwd sequence and read2 seq tag to rev sequence.

`perl P3toSpreadsheet_eas.pl Primer3_output.txt Species_ > GTseq_primers.txt`

### Create primer order sheet from Primer3 output
 ` perl P3toIDT_eas.pl GTseq_primers Species_ > GTseq_primer_order.txt`
 
### More coming... 