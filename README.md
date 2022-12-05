# Assembler.hack
Assembler.hack is a 16-bit machine language assembler for the 16-bit Hack Assembly Language.
This was done as part of building a complete 16-bit computer from the grounds up through the book,
and MOOC, Elementes of Computing Systems, which is informally known as nand2tetris https://www.nand2tetris.org/. Hack is also the name of the computer.

# Description
The Assembling process is implemented in two passes. The first pass scans the whole program, registering the labels only in the Symbol Table. The second pass scans the whole program again, registering all variables in the Symbol Table, substituting the symbols with their respective memory and/or instruction addresses from the Symbol Table, generating binary machine code and then writing the assembled machine code to the new .hack text file.

Source code is organized into several components, the decisions for their names, interfaces and APIs were already specified in the book as sort of a specification-implementation contract. All components of the Assembler reside in the /Assembler directory, as follows:

1. **Assembler.py**: Main module. Implements the two passes and glues the other components together.
2. **Parser.py**: Simple Parser. Parses the instructions by looking ahead 1 character to determine their types and structures.
3. **Code.py**: Generates binary machine code for instructions. For C-Instructions, it generates machine code for its constituting parts and then merges them back altogether.
