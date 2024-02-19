library(dplyr)
library(ggplot2)
library(magrittr)

setwd("~/repo/MaroonCapProject")

#R^2 plots

model <- read.csv("clean/BIGGESTWIN.csv") %>% rename("model" = R_squared)
classic <- read.csv("clean/classic.csv") %>% rename("classic" = R_squared)
SMB <- read.csv("clean/SMB_WIN.csv") %>% rename("SMB" = R_squared)
HML <- read.csv("clean/HML_WIN.csv") %>% rename("HML" = R_squared)


model_vs_classic <- model %>%
  left_join(classic, join_by(Stock)) %>%
  select(Stock, classic, model) %>%
  mutate(difference = model - classic)

d1 <- ggplot(model_vs_classic, aes(y = difference)) +
  geom_boxplot() +
  labs(x = "improvement over classic Fama-French model")

model_vs_SMB <- model %>%
  left_join(SMB, join_by(Stock)) %>%
  select(Stock, SMB, model) %>%
  mutate(difference = model - SMB) 

d2 <- ggplot(model_vs_SMB, aes(y = difference)) +
  geom_boxplot() +
  labs(x = "improvement over SMB and SMB interaction")

model_vs_HML <- model %>%
  left_join(HML, join_by(Stock)) %>%
  select(Stock, HML, model) %>%
  mutate(difference = model - HML)

d3 <- ggplot(model_vs_HML, aes(y = difference)) +
  geom_boxplot() +
  labs(x = "improvement over HML and HML interaction")

ggsave("release/dif_classic.png", plot = d1)
ggsave("release/dif_SMB.png", plot = d2)
ggsave("release/dif_HML.png", plot = d3)


#cumulative PNL

train_profits <- read.csv("clean/train_profits.csv") %>%
  mutate(cumulative_pnl = cumsum(profit),
         Date = as.Date(Date))

pnl1 <- ggplot(train_profits, aes(x = Date, y = cumulative_pnl)) +
  geom_line(color = "blue") +  # You can change the color as needed
  theme_minimal() +
  labs(title = "Cumulative P&L (Train Data)", x = "Date", y = "Cumulative PnL") +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red")


# Load the datasets
test_profits <- read.csv("clean/test_profits.csv")
market_profits <- read.csv("clean/market_profits.csv")
# Assuming the 'Date' column is in the format 'yyyy-mm-dd' in both datasets
test_profits$Date <- as.Date(test_profits$Date, format="%Y-%m-%d")
market_profits$Date <- as.Date(market_profits$Date, format="%Y-%m-%d")

# Calculate the cumulative sum of PnL for both datasets
test_profits$Cumulative_Test_PnL <- cumsum(test_profits$profit)
market_profits$Cumulative_Market_PnL <- cumsum(market_profits$profit)

# Merge both datasets by 'Date' column
combined_data <- merge(test_profits, market_profits, by="Date")

pnl2 <- ggplot() +
  geom_line(data = combined_data, aes(x = Date, y = Cumulative_Test_PnL, color = "Test Profits")) +
  geom_line(data = combined_data, aes(x = Date, y = Cumulative_Market_PnL, color = "Market Profits")) +
  theme_minimal() +
  labs(title = "Cumulative PnL Comparison", x = "Date", y = "Cumulative PnL") +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  scale_color_manual(values = c("Test Profits" = "blue", "Market Profits" = "green")) +
  guides(color = guide_legend(title = "Legend"))

ggsave("release/pnl_train.png", plot = pnl1)
ggsave("release/pnl_test.png", plot = pnl2)


