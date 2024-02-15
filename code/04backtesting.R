library(dplyr)

setwd("~/repo/MaroonCapProject")

regression_results <- read.csv("clean/BIGGERWIN.csv")
long_interest <- read.csv("clean/cleaned_ten_year_rate.csv")
train_dates <- read.csv("clean/train_data.csv")
test_dates <- read.csv("clean/test_data.csv")
price_data <- read.csv("raw/raw_data.csv")

price_data_test <- price_data %>%
  filter(Date %in% test_dates$Date)

price_data_train <- price_data %>%
  filter(Date %in% train_dates$Date)

ordered_results <- regression_results %>%
  mutate(sum = SMB + HML) %>%
  arrange(sum)

n = 0.1 #proportion of stocks that make up buy list and sell list

# Calculate the number of rows to extract
num_rows <- nrow(ordered_results)
rows_to_extract <- ceiling(num_rows * n)  # Use ceiling to round up to ensure at least one row is included

# Extract the first 10% for the sell list
sell_list <- ordered_results$STOCK[1:rows_to_extract]

# Extract the last 10% for the buy list
buy_list <- ordered_results$STOCK[(num_rows - rows_to_extract + 1):num_rows]

buy_profit_df <- price_data_test %>%
  filter(Stock %in% buy_list) %>%
  mutate(profit = 1000/start * (end - start))

profits = sum(buy_profit_df$profit)

sell_loss_df <- price_data_test %>%
  filter(Stock %in% sell_list) %>%
  mutate(loss = 1000/start * (start - end))

loss = sum(sell_loss_df$loss)

net = profits + loss