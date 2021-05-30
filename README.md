# Manhattan-project-
for minisql 

How to represent an address in a file?
* Use 3 bytes
* The highest 12 bits is block id (0 to 4095)
* The lowest 9 bits is offset (8-bit-padding, 0 to 511)
* The 3 bits in the middle is left for extra functions

Some points: 
* The records in a record file need not to be sorted. The pointers in a index file need to be sorted.  
* The index file is named as *xxx.index*
* The record file is named as *xxx.rec*
* The catalog contains *table_catalog* and *index_catalog*
