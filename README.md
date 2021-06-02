## Installation

To launch the application, clone the repository with the command:  
```commandline
    > git clone https://github.com/MaEgV/population-modeling
```
If you are interested in the development branch, run the following command:  
```commandline
    > git clone https://github.com/MaEgV/population-modeling -b develop
```
Next, we recommend setting up a virtual environment for the application. [See documentation](https://virtualenv.pypa.io/en/stable/installation.html)  
When you create and activate the environment, run:
```commandline
    > pip install -r requirements.txt
```
If you use the Pycharm IDE, you can connect the created environment to the application in the settings:
File -> Settings -> Project Interpreter -> Add -> (chose created env)  
Then your application is automatically configured for Django and you can run the server locally


### Setting database at local
 To run server properly, you need to create a database and migrate to her.  
To achieve this you need to create db you want(SQlite for example 'https://www.tutorialspoint.com/sqlite/sqlite_create_database.htm' ), and set it in DATABASES, located at 'server/settings.py'.
After this, you need to migrate your db to our models:
```commandline
    > python manage.py migrate
```
Now your db and server ready to run.

### Deploy Django server on heroku
Repository already have all needed for running django application on heroku. All you need is to create heroku repo for your project and push this repo there.  
Before pushing make sure DEBUG in 'server/setting.py' is False.
Also add your new server address to ALLOWED_HOSTS in 'server/setting.py'  
In our code we are using Heroku-Postgre('https://www.heroku.com/postgres'), choose a plan you will use. If you want to use another db, check 'Setting databases at local'.  
After pushing run migrate your db on heroku:
```commandline
    > heroku python manage.py migrate
```

***

### R Shiny app local using
To launch app.R you need to install R(https://www.r-project.org/). After installation, make sure R is in your Path.  
If you are going to use your server write you address to r_shiny_ui/config.json.  
After that you need to install shiny package, write in console
```commandline
    > R -e "install.packages("shiny")"
```
 When start a console in project root and write.
```commandline
   > R -e "shiny::runApp('r_shiny_ui/server.R')"
```
After what R print adress, and you can open application in your browser.

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
genealogical_tree = igraph.Graph(directed=True)  # create research-graph
first_bacteria = create_bacteria()  # create bacteria by suggested function
genealogical_tree.add_vertex(
		bacteria=first_bacteria, 
		generation=0)  # add first bacteria to graph
population = Population(genealogical_tree)  # Correct instance of Population class 
```

As you can see from the example, the jpgraph library is used for storing and manipulating the graph.
See the [documentation](https://igraph.org/python/).

The main manipulations with the population class are drawing and the possibility of development over time.  
Draw and iterate are responsible for this, respectively.

#### Draw
```Python
population.draw("filename.png")  # Draw a research as a tree and save pitcure at file
```
```Python
population.draw()  # Draw a research without saving
```
Implements the tree graph rendering mechanism.  

`population` - instance of the class that you want to display.   
`filename` - a string with the name of the file to save the image to. If the filename parameter is omitted, the image will be displayed by the standard image viewer on your device without saving it.

#### Iterate
```Python
selector = Selector(ExternalFactors())  # creating the initial parameters of the research and selectors
mutation_mode = NormalMutations()  # mutation mode for bacterias iterations

iterate(population, selector, mutation_mode)  # Iterate all bacterias in research
```
Function that implements a single time cycle of a population. This cycle consists in the sequential updating of the state of each bacterium, according to the mechanisms of selection and mutation.  

`population` - instance of the population class that you want to iterate.  
`selector` - implementation of the selection mechanism for each bacteria in population for this iteration.
`mutation_mode` - implementation of the evolving mechanism for each bacteria in population for this iteration.


### Bacteria
This class stores the state of a particular bacterium. The main parameters of the bacterium are the values stored in the additional Genome class. Parameters from Genome can change under the influence of mutational mechanisms. Based on the same parameters, the selection operator performs natural selection.  

```Python
genome = Genome(0.5, 0.5, 0.5)  # Genome of future bacteria
new_bacteria = Bacteria(genome)
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
selector = Selector(ExternalFactors())  # creating the initial parameters of the research and selectors
mutation_mode = NormalMutations()  # mutation mode for bacterias iterations

  iterate(bacteria, selector, mutation_mode)  # Iterate all bacterias in research
```
`max_life_time` - parameter that marks the maximum number of iterations that a bacterium can survive.
`p_for_death` - internal probability of dying during the next iteration. The selection operator can affect the resulting probability.
`p_for_reproduction` - internal probability of reproducting during the next iteration. The selection operator can affect the resulting probability.

### Selector
A class that implements a framework for building the logic of the selection operator.
```Python
external_factors = ExternalFactors()
have_to_die_func = default_have_to_die  # Callable[ext_factors: ExternalFactors, genome: Genome]
have_to_reproduct = default_have_to_reproduct

selector = Selector(external_factors, have_to_die_func, have_to_reproduct)  # creating the initial parameters of the research and selectors
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
## Using application
You can easily access our application on 'https://r-shiny-ui.herokuapp.com/'.

***
## Example
Consider a simple example of setting up a population and drawing the result of an evolution simulation:

```Python
from src.population_modeling import create_bacteria, create_population, NormalMutator, AbstractSelector,
    ExternalFactors,

iterate

first_bacteria = create_bacteria(p_for_death=0.1)  # creating first bacteria to start a research
population = create_population(first_bacteria)  # creating research

selector = Selector(ExternalFactors())  # creating the initial parameters of the research and selectors
mutation_mode = NormalMutations()  # mutation mode for bacterias iterations

for _ in range(10):
    iterate(population, selector, mutation_mode).draw()  # drawing a research without saving

```
![alt text](https://github.com/MaEgV/population-modeling/blob/develop/examples/population_image_example_res.gif)

***
## Authors
This project was implemented by students of Peter the Great St. Petersburg Polytechnic University:
* [Grishina Elizaveta](https://github.com/besperspektivnyak);
* [Marin Egor](https://github.com/MaEgV).  
Under the guidance of a teacher- [Dmitry Yakovlev] (https://github.com/JDima).
