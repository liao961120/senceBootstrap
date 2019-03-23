library(dplyr)

data <- readr::read_csv('pixnlp.dict.intersect.csv')
data <- data[, c('phrase_name', 'tag_CK', 'count_CK')]

cont_func_weight <- function(df, func_words) {
  weighted_vals <- vector('double', nrow(df))
  for (i in seq_along(df[[1]])) {
    weighted_vals[[i]] <- cont_func_weight_row(df[i,], func_words)
  }
  return(weighted_vals)
}

cont_func_weight_row <- function(df, func_words = c('Caa', 'Cab')) {
  func_word_idx <- df$tag_CK[[1]] %in% func_words
  
  func_words_fq <- as.integer(df$count_CK[[1]][func_word_idx])
  cont_words_fq <- as.integer(df$count_CK[[1]][!func_word_idx])
  
  # Add 1 to deal with freq = 0
  func_word_fq <- ifelse(length(func_words_fq) > 0,
                         sum(func_words_fq) + length(func_words_fq), 
                         1)
  cont_word_fq <- ifelse(length(cont_words_fq) > 0,
                         sum(cont_words_fq) + length(cont_words_fq),
                         1)

  #if (func_word_fq == 0 || cont_word_fq == 0) {
  #  func_word_fq <- func_word_fq + 1
  #  cont_word_fq <- cont_word_fq + 1
  #}
  
  # Deal with data sparsity
  return(round(log(cont_word_fq / func_word_fq), digits = 3))
}

func_words <- c('Caa', 'Cab', 'Cbab', "Cbaa", "Cbba", "Cbbb", "Cbca", "Cbcb", "Daa", "Dfa", "Dfb", "Di", "Dk", "Dab", "Dbaa", "Dbab", "Dbb", "Dbc", "Dc", "Dd", "Dg", "Dh", "Dj","Neu", "Nep", "Neqa", "Neqb", "Ng", "Nhaa", "Nhab", "Nhac", "Nhb", "Nhc", "I", paste0('P', stringr::str_pad(1:99, 2, pad = "0")), "Ta", "Tb", "Tc", "DE", "SHI")

data <- data %>% 
  mutate(tag_CK = strsplit(tag_CK, ', '),
         count_CK = strsplit(count_CK, ', ')) %>%
  mutate(weight = cont_func_weight(., func_words)) %>%
  arrange(weight)


saveRDS(data, 'wordlist_cont_func_weight.RDS')


#########################

# filter value
data <- readRDS('wordlist_cont_func_weight.RDS')

filtered <- data[data$weight < 0, c(1, 4)]

#readr::write_csv(filtered, 'stop_words.csv')
writeLines(filtered$phrase_name, 'stop_words.txt')
