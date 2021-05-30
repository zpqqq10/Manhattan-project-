# Manhattan-project-
for minisql 

How to represent an address in a file?
* Use 3 bytes
* The highest 12 bits is block id (0 to 4095)
* The lowest 9 bits is offset (8-byte-padding, 0 to 511)
* The 3 bits in the middle is left for extra functions

Some points: 
* The records in a record file need not to be sorted. The pointers in a index file need to be sorted.  
* The index file is named as *xxx.index*
* The record file is named as *xxx.rec*, storing metadata. The beginning 3 bytes of a record file is the header of the **freelist**
* The catalog contains *table_catalog* and *index_catalog*

We agree； 
* 8-byte-padding
* a *double* variable occupies 8 bytes 
* an *int* variable occupies 8 bytes
* The length of a record is determind once all the attributes have been determined. 
