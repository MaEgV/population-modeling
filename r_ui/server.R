library(shiny)
library(jsonlite)
library(httr)

server <- function(input, output) {
  
  click <- eventReactive(input$add, {
    runif(input$lifetime, input$reproduct)
  })
  
  output$text <- reactive({
    click()
    data <- structure(list(list(name = "lifetime", value = input$lifetime),
                          list( name = "p_for_death", value = input$death),
                          list(name = "p_for_reproduction",
                               value = input$reproduct)))
    
    json_data <- toJSON(data, pretty = TRUE, auto_unbox = TRUE)
    path <- 'url bla bla bla'
    res <- httr::POST(url = path, body = json_data, encode = "json")
    paste("Cock", input$death)
  })

}