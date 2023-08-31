# Extract Bibliographic Data

> **Problem statement:** Bibliographic citations in manuscripts are structured data that exist in an unstructured form at the manuscript stage.

```
Aldred, Cyril. 1970. “Some royal portraits of the Middle Kingdom in ancient Egypt.” Metropolitan Museum Journal 3: 27-50.

Allen, Thomas George. 1923. A Handbook of the Egyptian Collection. Chicago: The Art Institute of Chicago.
```

> **Objective:** Automate the process of converting bibliographic references in Microsoft Word documents into a structured data format. 

```yaml
- authors: Aldred, Cyril
  title: Some royal portraits of the Middle Kingdom in ancient Egypt.
  year: '1970'
- authors: Allen, Thomas George
  title: A Handbook of the Egyptian Collection
  year: '1923'
```