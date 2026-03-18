export interface ArbitrageOpportunity {
  id: number;
  asset_symbol: string;
  cheapest_exchange_name: string;
  most_expensive_exchange_name: string;
  cheapest_price: string;
  highest_price: string;
  spread_absolute: string;
  spread_percent: string;
  observed_at: string;
}