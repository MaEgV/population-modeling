library(shiny)
library(jsonlite)
library(httr)
library(data.table)


id <<- 0
results <<- data.frame(all=c(0, 0, 0), alive=c(0, 0, 0), dead=c(0, 0, 0))


server <- function() {
  path <- 'http://127.0.0.1:8000/population_research/research/'
  r <- GET(url = path)
  new_data = jsonlite::fromJSON(content(res, 'text'))
  new_data = jsonlite::fromJSON(new_data)
  id <<- new_data
  print(id)
}

server <- function(input, output) {
  
  observeEvent(input$add, {
    data_ <- structure(list(list("lifetime" = input$lifetime),
                          list( "p_for_death" = input$death),
                          list("p_for_reproduction" = input$reproduct),
                          list("type" = input$indiv_type)))
    
    json_data <- toJSON(data_, pretty = TRUE, auto_unbox = TRUE)
    path <- paste0('http://127.0.0.1:8000/population_research/research/', id, '/add/')
    res <- httr::POST(url = path, content_type_json(), body = json_data)
    
    new_data = jsonlite::fromJSON(content(res, 'text'))
    new_data = jsonlite::fromJSON(new_data)
    id <<- new_data
    
    print(id)
  })
  
  
  observeEvent(input$build, {
    print(input$selector_type, input$selector_mode)
     path <- paste0('http://127.0.0.1:8000/population_research/research/', id, 
    '/run/?s_t=',as.character(input$selector_type),'&s_m=', input$selector_mode,
    '&m_t=', input$mutator_type, '&m_m=', input$mutator_mode,
    '&n=', 3)
    res <- GET(url = path)
    results <<- jsonlite::fromJSON(content(res, 'text'))
    
    output$plot <- renderPlot({
      df<- data.frame(all=unlist(results[c('all')]), alive=unlist(results[c('alive')]), dead=unlist(results[c('dead')]))
      print(df)
      barplot(t(as.matrix(df)), beside=TRUE)
    })
  })


  observeEvent(input$reset, {
    path <- paste0('http://127.0.0.1:8000/population_research/research/', id, '/delete/')
    res <- GET(url = path)
    
  })
  
  observeEvent(input$load_pop, {
    path <- 'http://127.0.0.1:8000/population_research/research/db/populations/'
    res <- GET(url = path)
    new_data = fromJSON(rawToChar(res$content))
    output$table_1 <- DT::renderDataTable({data.frame(new_data)})
  })
  
  observeEvent(input$get_pop, {
    path <- paste0('http://127.0.0.1:8000/population_research/research/', input$load_pop_num)
    res <- GET(url = path)
    new_data = jsonlite::fromJSON(content(res, 'text'))
    new_data = jsonlite::fromJSON(new_data)
    id <<- new_data
    print(id)
  })
  
  observeEvent(input$load_res, {
    path <- 'http://127.0.0.1:8000/population_research/research/db/results/'
    res <- GET(url = path)
    new_data = fromJSON(rawToChar(res$content))
    output$table_1 <- DT::renderDataTable({data.frame(new_data)}) 
  })
  
  observeEvent(input$get_res, {
    path <- paste0('http://127.0.0.1:8000/population_research/research/', input$load_pop_num)
    res <- GET(url = path)
    new_data = jsonlite::fromJSON(content(res, 'text'))
    new_data = jsonlite::fromJSON(new_data)
    id <<- new_data
    print(id)
  })
  
  
  observeEvent(input$save_pop, {
    
    data_ <- structure(list(list("name" = input$save_pop_name)))
    
    json_data <- toJSON(data_, pretty = TRUE, auto_unbox = TRUE)
    path <- paste0('http://127.0.0.1:8000/population_research/research/', id, '/save/')
    res <- httr::POST(url = path, content_type_json(), body = json_data)
  })
  
  # observeEvent(input$save_res, {
  #   data_ <- structure(list(list("name" = input$save_res_name)))
  #   
  #   json_data <- toJSON(data_, pretty = TRUE, auto_unbox = TRUE)
  #   path <- paste0('http://127.0.0.1:8000/population_research/research/', id, '/add/')
  #   res <- httr::POST(url = path, content_type_json(), body = json_data)
  #   
  #   new_data = jsonlite::fromJSON(content(res, 'text'))
  #   new_data = jsonlite::fromJSON(new_data)
  #   id <<- new_data
  #   print(id) 
  # })
}