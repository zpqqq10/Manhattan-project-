# Manhattan-project-

How to represent an address in a file?
* Use 4 bytes (use `struct`)
* 2 bytes is for block id
* 2 bytes is for offset

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
