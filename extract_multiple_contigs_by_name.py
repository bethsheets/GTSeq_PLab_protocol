#!/usr/bin/env python

''' Script to extract multiple full contigs, based on names specified
    in input contig_names file

    If you want all of your contigs in a single file, use the following:
    usage: ./extract_contig_by_name.py seq_file.fasta contig_names.txt single 

    If you want your contigs in their own, individual files, use the following:
    usage: ./extract_multiple_contigs_by_name.py seq_file.fasta contig_names.txt multiple

    CYP -- 12/18/2017
'''

import sys
import re

''' Use this function if you want several
    files, each containing only one contig
    >> Called when option "multiple" is used
'''
def output_indv_files(names_list):
  print("You selected: multiple")
  # find each contig name individually
  for seq_name in names_list:
    found = False
    with open(sys.argv[1], 'r') as f:
      for line in f: 
        # loop through every line in fasta,
        # check each for a ">" header
        if re.search(">", line):
          # if you come up on another ">"
          # after finding contig, you've 
          # reached the end of that contig's
          # seq, so break
          if found: 
            out.close()
            break
          # if a header found, check name
          if re.search(seq_name, line):
            found = True
            # create output file for contig
            filename = seq_name+'.fasta'
            out = open(filename, 'w')
        # begin writing contig lines if 
        # correct header was found
        if found: out.write(line)


''' Use this function if you want a single file
    containing all of the desired contigs 
    >> Called when option "single" is used
'''
def output_single_file(names_list):
  print("You selected: single")
  # specify output file
  out = open('contigs.fasta', 'w')
  for seq_name in names_list:
    found = False
    with open(sys.argv[1], 'r') as f:
      # loop through every line in fasta,
      # check each for a ">" header
      for line in f: 
        if re.search(">", line):
          if found: 
            break
          # if header found, check name
          if re.search(seq_name, line):
            found = True
        # begin writing contig lines if
        # correct header was found
        if found: out.write(line)


### MAIN ###

# if there are less than 4 arguments in command,
# throw error
if len(sys.argv) != 4:
  print("HOLD UP, not enough arguments: \
      \n\tPlease include fasta file, \
      \n\tcontig names file, and \
      \n\tsingle/multiple option in your command")
  quit() 

# record output file option
file_option = sys.argv[3]

# collect all contig names from names.txt file
with open(sys.argv[2], 'r') as names:
  names_list = [x.strip() for x in names.readlines()]

# Based on specified output file option, output contigs
if file_option == "multiple":
  output_indv_files(names_list)
elif file_option == "single":
  output_single_file(names_list)
else:
  print("HOLD UP, please use a valid file_option: \
         \n\tsingle = one file for all contigs \
         \n\tmultiple = one file per contig")

print("Yay, all done!")
