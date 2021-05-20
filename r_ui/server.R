library(shiny)
library(jsonlite)
library(httr)

server <- function() {
  path <- 'http://127.0.0.1:8000/population_research/research/'
  r <-GET(url = path)
}

server <- function(input, output) {
  
  click <- eventReactive(input$add, {
    runif(input$lifetime, input$reproduct)
  })
  
  output$text <- reactive({
    click()
    data_ <- structure(list(list("lifetime" = input$lifetime),
                          list( "p_for_death" = input$death),
                          list("p_for_reproduction" = input$reproduct),
                          list("type" = input$indiv_type)))
    
    json_data <- toJSON(data_, pretty = TRUE, auto_unbox = TRUE)
    path <- 'http://127.0.0.1:8000/population_research/research/0/add/'
    res <- httr::POST(url = path, content_type_json(), body = json_data)
    paste("death ", input$death)
  })

}