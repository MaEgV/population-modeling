# Population Modeling

***
## Installation

You must install the dependencies reflected in the file requirements.txt and put the source code of the package(the contents of the src directory) in a place available for import by your program.
The specified dependencies are installed from the console, using the following command:
`pip install -r requirements.txt`
***
## Glossary

* Bacterium-an instance of the Bacteria class. An entity that participates in natural selection. The variability of its parameters ensures the primitive behavior of this entity. The only possible actions are: dying and reproducing.
* Genome-an instance of the Genome class. The set of internal parameters of the bacterium;
* Population-an instance of the Population class. A collection of bacteria linked by a relationship of kinship. Such a collection forms a tree graph;
* Iteration-iteration functions for the Population and Bacteria classes. Means a discrete unit of evolution time. The population iteration should ensure that the population state is synchronized for all bacteria.
***

## Description
The package is based on three classes and their processing logic:
* Bacteria - a class that stores the state of the bacterium;
* Population - a class that stores a set of bacteria and a parent-child relationship on this set;
* Selector-a class that implements the mechanisms of natural selection within a population.


### Population
This class stores a graph of the bacteria in the population. The graph forms a tree, so the only attribute of the class is the genealogical tree field. It is also passed to initialize an instance of the class when it is created:  
```Python
    def __init__(self, genealogical_tree: igraph.Graph):
        self.genealogical_tree = genealogical_tree
```

As you can see from the example, the jpgraph library is used for storing and manipulating the graph.
See the [documentation](https://igraph.org/python/).

The main manipulations with the population class are drawing and the possibility of development over time.  
Draw and iterate are responsible for this, respectively.

#### Draw
```Python
draw(population: Population, filename: str = None) -> None
```
Implements the tree graph rendering mechanism.  

`population` - instance of the class that you want to display.   
`filename` - a string with the name of the file to save the image to. If the filename parameter is omitted, the image will be displayed by the standard image viewer on your device without saving it.

#### Iterate
```Python
iterate(population: Population, selector: Selector, mutation_mode: MutationalProcesses)
```
Function that implements a single time cycle of a bacterium, during which it can die or multiply.  

`population` - instance of the population class that you want to iterate.  
`selector` - implementation of the selection mechanism for each bacteria in population for this iteration.
`mutation_mode` - implementation of the evolving mechanism for each bacteria in population for this iteration.



**Пример использования**
======================
Рассмотрим простой пример настройки популяции и отрисовки результата симуляции эволюции:

```Python
from population_modeling import *

first_bacteria = create_bacteria(p_for_death=0.1)  # creating first bacteria to start a population
population = create_population(first_bacteria)  # creating population

selector = Selector(ExternalFactors())  # creating the initial parameters of the population and selector
mutation_mode = NormalMutations()  # mutation mode for bacterias iterations

for _ in range(10):
    draw(iterate(population, selector, mutation_mode))  # drawing a population without saving

```
![alt text](https://github.com/MaEgV/population-modeling/blob/population/examples/population_image_example_res.gif)
