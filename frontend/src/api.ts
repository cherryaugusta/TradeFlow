import type { ArbitrageOpportunity } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function fetchOpportunities(): Promise<ArbitrageOpportunity[]> {
  const response = await fetch(`${API_BASE_URL}/opportunities/`);

  if (!response.ok) {
    throw new Error(`Failed to fetch opportunities: ${response.status}`);
  }

  return (await response.json()) as ArbitrageOpportunity[];
}