# NoYAML with Section References {#sec:title1}
This is a document with no yaml metadata blocks, but it does have section references for both [@sec:title1] and

## Intended Result {#sec:results otherproperties=42}
The `markdown-crossref` program (currently [this python script](../markdown-crossref.py)) should replace all instances of `[@sec:title1]` and `[@sec:results]` (that are not escaped in this fashion) with the latex code to insert labels and references in the appropriate places, as explained in [@Sec:results]. Those with a lowercase `@sec` should use a lowercase "section" label and those with an uppercase `@Sec` should use the uppercase "Section" label.
