##gathering data
library(dplyr)

setwd("~/repo/MaroonCapProject")

regression_results <- read.csv("clean/BIGGERWIN.csv") %>%
  mutate(sum = SMB + HML) %>%
  arrange(sum)
long_interest <- read.csv("clean/cleaned_ten_year_rate.csv")
train_dates <- read.csv("clean/train_data.csv")
test_dates <- read.csv("clean/test_data.csv")
price_data <- read.csv("raw/raw_data.csv")
market_return <- read.csv("clean/cleaned_data.csv") %>%
  select(Date, Market)

##paramaters

n = 0.1 #proportion of stocks that make up buy list and sell list


##functions
calculate_period_profits <- function(data_frame, buy_list, sell_list) {
  # Calculate profits for buy_list
  profit_df <- data_frame %>%
    filter(Stock %in% union(buy_list, sell_list)) %>%
    mutate(profit = case_when(
      Stock %in% buy_list ~ 1000 / start * (end - start),
      TRUE ~ 1000 / start * (start - end))
    ) %>%
    group_by(Date) %>%
    summarise(
      profit = sum(profit)
    )
}


##code
num_rows <- nrow(regression_results)
rows_to_extract <- ceiling(num_rows * n)  # Use ceiling to round up to ensure at least one row is included

# Extract the first 10% for the sell list
sell_list <- regression_results$STOCK[1:rows_to_extract]

# Extract the last 10% for the buy list
buy_list <- regression_results$STOCK[(num_rows - rows_to_extract + 1):num_rows]


above_av_months_df <- long_interest %>% filter(FEDFUNDS > mean(FEDFUNDS))
above_av_dates <- above_av_months_df$DATE

high_int_test <- price_data %>%
  filter(Date %in% test_dates$Date, Date %in% above_av_dates)

low_int_test <- price_data %>%
  filter(Date %in% test_dates$Date, !Date %in% above_av_dates)

high_int_train <- price_data %>%
  filter(Date %in% train_dates$Date, Date %in% above_av_dates)

low_int_train <- price_data %>%
  filter(Date %in% train_dates$Date, !Date %in% above_av_dates)

df <- calculate_period_profits(high_int_test, buy_list, sell_list)
df2 <- calculate_period_profits(low_int_test, buy_list, sell_list)
calculate_net_result(high_int_train, buy_list, sell_list)
calculate_net_result(low_int_train, buy_list, sell_list)
