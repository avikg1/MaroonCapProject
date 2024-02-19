##gathering data
library(dplyr)
library(lmtest)

setwd("~/repo/MaroonCapProject")

long_interest <- read.csv("clean/cleaned_ten_year_rate.csv")
train_dates <- read.csv("clean/train_data.csv")
test_dates <- read.csv("clean/test_data.csv")
price_data <- read.csv("raw/raw_data.csv")
market_return <- read.csv("clean/cleaned_data.csv") %>%
  select(Date, Market, Risk_Free)

##paramaters

n = 0.2 #proportion of stocks that make up buy list and sell list
HML_weight = 0.1
buy_threshold = 0.9

##functions

calculate_period_profits <- function(data_frame, buy_list, sell_list) {
  # Calculate profits for buy_list
  profit_df <- data_frame %>%
    filter(Stock %in% union(buy_list, sell_list)) %>%
    mutate(profit = case_when(
      Stock %in% buy_list & is_high_int  ~ 1000 / start * (end - start),
      Stock %in% buy_list & !is_high_int ~ 0,
      Stock %in% sell_list & !is_high_int ~ 1000 / start * (end - start),
      TRUE ~ 0
    )) %>%
    group_by(Date) %>%
    summarise(
      profit = sum(profit),
      return = profit / (1000 * length(buy_list))
    )
}

calculate_sharpe_ratio <- function(df, market) {
  merged_df <- merge(df, market, by = "Date")
  
  # Calculate excess returns for the portfolio
  merged_df$Excess_Return <- merged_df$return - merged_df$Risk_Free
  
  # Calculate Sharpe Ratio
  sharpe_ratio <- mean(merged_df$Excess_Return) / sd(merged_df$Excess_Return)
  
  return(sharpe_ratio)
}

calculate_alpha <- function(df, market) {
  
  # Merge df and market data frames on Date
  merged_df <- merge(df, market, by = "Date")
  
  # Calculate excess returns for both portfolio and market
  merged_df$Portfolio_Excess_Return <- merged_df$return - merged_df$Risk_Free
  merged_df$Market_Excess_Return <- merged_df$Market - merged_df$Risk_Free
  
  # Linear regression of Portfolio_Excess_Return on Market_Excess_Return
  fit <- lm(Portfolio_Excess_Return ~ Market_Excess_Return, data = merged_df)
  
  print(summary(fit))
  
  # Alpha is the intercept
  alpha <- coef(fit)[1]
  beta <- coef(fit)[2]
  
  return(list(alpha = alpha, beta = beta))
}

##code
regression_results <- read.csv("clean/BIGGESTWIN.csv") %>%
  mutate(sum = SMB_interaction*(1 - HML_weight)
         + HML_interaction * HML_weight) %>%
  arrange(sum)


# Calculate the number of rows to extract
num_rows <- nrow(regression_results)
rows_to_extract <- ceiling(num_rows * n)  # Use ceiling to round up to ensure at least one row is included

# Extract the first 10% for the sell list
sell_list <- regression_results$Stock[1:rows_to_extract]

# Extract the last 10% for the buy list
buy_list <- regression_results$Stock[(num_rows - rows_to_extract + 1):num_rows]

above_av_months_df <- long_interest %>% filter(FEDFUNDS > buy_threshold* mean(FEDFUNDS))
above_av_dates <- above_av_months_df$DATE

test_data <- price_data %>%
  filter(Date %in% test_dates$Date) %>%
  mutate(is_high_int = case_when(
    Date %in% above_av_dates ~ TRUE,
    TRUE ~ FALSE
  ))

train_data <- price_data %>%
  filter(Date %in% train_dates$Date) %>%
  mutate(is_high_int = case_when(
    Date %in% above_av_dates ~ TRUE,
    TRUE ~ FALSE
  ))

train_profits <- calculate_period_profits(train_data, buy_list, sell_list)
calculate_sharpe_ratio(train_profits, market_return)
calculate_alpha(train_profits, market_return)

write.csv(train_profits, "clean/train_profits.csv")

test_profits <- calculate_period_profits(test_data, buy_list, sell_list)
calculate_sharpe_ratio(test_profits, market_return)
calculate_alpha(test_profits, market_return)

write.csv(test_profits, "clean/test_profits.csv")


calculate_market_profits <- function(df, market) {
  
  # Merge df and market data frames on Date
  merged_df <- market %>%
    filter(Date %in% test_dates$Date)
  
  # Calculate excess returns for both portfolio and market
  merged_df$profit <- merged_df$Market*1000*length(buy_list)
  
  merged_df <- merged_df %>%
    select(Date, profit)
  
  return(merged_df)
}

write.csv(calculate_market_profits(test_dates, market_return), "clean/market_profits.csv")
