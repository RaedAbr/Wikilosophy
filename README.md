# Wikilosophy

## Project context and objectives

### Initial observation

> *Wikipedia trivia: if you take any article, click on the first link in the article text not in parentheses or italics, and then repeat, you will eventually end up at **Philosophy***

### Context

* Previous quote first appeared on the alt-text of the [xkcd webcomic #903](https://xkcd.com/903/)
* As of February 2016, 97% of all articles lead to Philosophy in this manner

### Why does this happen?

- Most pages start by describing the topic of the page
- Topics naturally get broader as they contain multiple other topics
- Eventually we reach the widest reaching pages, such as Mathematics, Science, and Philosophy

###  Objectives

- Crawl the entirety of the English Wikipedia in this manner (code should be easily adaptable to other languages)
- Calculate an up-to-date estimate of how many pages lead to Philosophy
- Calculate connected components sizes
- Estimate average distance from a random page to Philosophy
- Graph visualization if feasible

### Expected result

- A large connected component that includes most of the pages that do not lead to Philosophy

- We expect another large science-related page

- A large number of authorities linking to the Philosophy page (the graph should have a tree structure leading to Philosophy)

- A certain number of dead-ends, pages with no valid hyperlink leading to a new page

### Risks and problems

- Large graph size might make visualisations unfeasible
- Since the 2016 estimate, there are a lot more pages that do not lead to Philosophy (Based on random tests we performed)
- Group has no experience with Neo4j or Apache Commons Compress API

## Data source and treatments
### Data

- Wikipedia regularly blocks IP addresses performing excessive crawling (not viable for an entire site crawl)
- A downloadable database of all Wikipedia pages is available as XML
- Contains an index with byte offsets allowing to decompress 100 page sections at a time
- Approximately 16GB in size and 200MB for the index

### Index structure

- Byte offset
- Page ID
- Page Title

![](./Screenshots/photo5935959929573716216.jpg)

### Graph generation

- Each page represents a graph vertex

- Easy to create an edge list using the index

- - Unzip 100 pages
  - For each page, find the first hyperlink not in italic or parentheses
  - Place the start and end vertices separated by a tab character in a file

- Size of edge list should around the same size as the index since they both contain one line per page

- Must only be done once (unless using a different dump or language)


## Planification and work 
- Decompress XML pages using a Java library (By 10.05)
- Parse the XML to find the first valid hyperlink (By 10.05)
- Create graph and import to Neo4j (By 17.05)
- Analyse graph using Neo4j and aggregate interesting statistics (By 24.05)
- Finish project, complete report, add any additional features like visualisations (By 07.06)
- Finishing touches for project end date (10.06)

## Functionalities

## Techniques, algorithmes and tools
### Tools
- Java

- Apache Commons Compress API for decompression (Allows the use of an offset)

- Neo4j (Allows graph analysis and importation using an edge list)



## Conclusion
