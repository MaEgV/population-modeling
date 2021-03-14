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
This package is based on the following classes and the logic of working with them:
* Population - a class that stores a set of bacteria and a parent-child relationship on this set;
* Bacteria - a class that stores the state of the bacterium;
* Selector - a class that implements the mechanisms of natural selection within a population;
* MutationalProcesses - an abstract class that defines an interface for introducing variability into the evolution of a population.

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
iterate(population: Population, selector: Selector, mutation_mode: MutationalProcesses) -> Population
```
Function that implements a single time cycle of a population. This cycle consists in the sequential updating of the state of each bacterium, according to the mechanisms of selection and mutation.  

`population` - instance of the population class that you want to iterate.  
`selector` - implementation of the selection mechanism for each bacteria in population for this iteration.
`mutation_mode` - implementation of the evolving mechanism for each bacteria in population for this iteration.


### Bacteria
This class stores the state of a particular bacterium. The main parameters of the bacterium are the values stored in the additional Genome class. Parameters from Genome can change under the influence of mutational mechanisms. Based on the same parameters, the selection operator performs natural selection.  
```Python
    def __init__(self, genome: Genome):
        self.is_alive = True
        self.age = 0
        self.genome = genome
```
`genome` - instance of the Genome class with the initial parameters.
The main functions for working with this class are described below.

#### Iterate
Implementation of the logic of the passage of time, in which a bacterium can change, give offspring, die. A direct continuation of the method of the same name for the Population class, but only for individual bacteria.   
_It is located in another module to avoid name collisions_.
```Python
iterate(selector: Selector, mutation_mode: MutationalProcesses, bacteria: Bacteria) -> list
```
`bacteria` - instance of the bacteria class that you want to iterate.  
`selector` - implementation of the selection mechanism for this iteration.
`mutation_mode` - implementation of the evolving mechanism for this iteration.


#### Genome
Storage of the genetic parameters of the bacterium that will change and be inherited by descendants.
```Python
    def __init__(self, max_life_time: int, p_for_death: float, p_for_reproduction: float):
        self.max_life_time = max_life_time
        self.p_for_death = p_for_death
        self.p_for_reproduction = p_for_reproduction
```
`max_life_time` - parameter that marks the maximum number of iterations that a bacterium can survive.
`p_for_death` - internal probability of dying during the next iteration. The selection operator can affect the resulting probability.
`p_for_reproduction` - internal probability of reproducting during the next iteration. The selection operator can affect the resulting probability.

### Selector
A class that implements a framework for building the logic of the selection operator.
```Python
    def __init__(self,
                 external_factors: ExternalFactors,
                 have_to_die_func: Callable = default_have_to_die,
                 have_to_reproduct_func: Callable = default_have_to_reproduct
                 ):
        self.have_to_die_func = have_to_die_func
        self.have_to_reproduct_func = have_to_reproduct_func
        self.external_factors = external_factors
```
`external_factors` - a set of initial external environmental factors.  
`have_to_die_func` - a function that determines whether the bacteria should die based on the genome and external factors.  
`have_to_reproduct_func` - a function that determines whether the bacteria should multiply based on the genome and external factors.  

### MutationalProcesses
Abstract class that defines the logic of mutation processes for bacteria. For the program to work, you need to implement or take an existing implementation of methods of this class and pass the filled instance as a parameter to iterate at each iteration of the population.

***
## Documentation
See more information in [documentation](https://github.com/MaEgV/population-modeling/tree/develop/docs).

***

## Example
Consider a simple example of setting up a population and drawing the result of an evolution simulation:
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

***
## Authors
This project was implemented by students of Peter the Great St. Petersburg Polytechnic University:
* [Grishina Elizaveta](https://github.com/besperspektivnyak);
* [Marin Egor](https://github.com/MaEgV).  
Under the guidance of a teacher- [Dmitry Yakovlev] (https://github.com/JDima).
