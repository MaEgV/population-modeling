library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Population Modeling"),
  fluidRow(
    column(6, selectInput("selector_type", 
                       "Choose type of selector", 
                       c("Uniform Selector" = "uniform")),
           sliderInput("selector_mode", "Choose level of aggressiveness of a selector",
                       min = 0.1, max = 0.9, value = 0.45, step = 0.05), 
           selectInput("mutator_type", 
                       "Choose type of mutator", 
                       c("Normal Mutator" = "normal")),
           sliderInput("mutator_mode", "Choose level of variability of a mutator",
                       min = 0, max = 0.2, value = 0.1, step = 0.01), 
           numericInput("iter", "Number of iterartions", value = 3),
           actionButton("build", "Build"),
           actionButton('reset', "Reset")), 
    column(6, selectInput("indiv_type", 
                       "Choose type of individual", 
                       c("Bacteria" = "bacteria")),
           sliderInput("lifetime", "Maximum bacteria lifetime",
                      min = 0, max = 10, value = 3, step = 1),
           sliderInput("death", "Death probability",
                       min = 0, max = 1, value = 0.3, step = 0.1),
           sliderInput("reproduct", "Reproduction probability",
                       min = 0, max = 1, value = 0.3, step = 0.1),
           actionButton('add', "Add")),
    column(12,
           actionButton('load_pop', "Load population"),
           numericInput("load_pop_num", "Number of iterartions", value = 0),
           actionButton('load_res', "Load research"),
           numericInput("load_res_num", "Number of iterartions", value = 0),
           actionButton('save_pop', "Save population"),
           textInput('save_pop_name', 'Populaton name'),
           actionButton('save_res', "Save research"),
           textInput('save_res_name', 'Research name')),
    column(12, 
    textOutput('text'),
    tableOutput('table'),
    plotOutput('plot'))

    )
  )
)