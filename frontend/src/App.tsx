import React from "react";
import { fetchOpportunities } from "./api";
import type { ArbitrageOpportunity } from "./types";
import OpportunitiesTable from "./components/OpportunitiesTable";

function buildSignatureMap(rows: ArbitrageOpportunity[]): Map<number, string> {
  const map = new Map<number, string>();
  rows.forEach((row) => {
    map.set(
      row.id,
      [
        row.cheapest_price,
        row.highest_price,
        row.spread_absolute,
        row.spread_percent,
        row.observed_at,
      ].join("|")
    );
  });
  return map;
}

export default function App(): React.JSX.Element {
  const [rows, setRows] = React.useState<ArbitrageOpportunity[]>([]);
  const [loading, setLoading] = React.useState<boolean>(true);
  const [error, setError] = React.useState<string>("");
  const [flashingRowIds, setFlashingRowIds] = React.useState<Set<number>>(new Set());

  const previousSignatureMapRef = React.useRef<Map<number, string>>(new Map());

  const load = React.useCallback(async () => {
    try {
      const nextRows = await fetchOpportunities();
      const previousMap = previousSignatureMapRef.current;
      const nextMap = buildSignatureMap(nextRows);

      const changedIds = new Set<number>();
      nextRows.forEach((row) => {
        const prev = previousMap.get(row.id);
        const next = nextMap.get(row.id);
        if (prev && next && prev !== next) {
          changedIds.add(row.id);
        }
      });

      previousSignatureMapRef.current = nextMap;
      setRows(nextRows);
      setFlashingRowIds(changedIds);

      window.setTimeout(() => {
        setFlashingRowIds(new Set());
      }, 1200);

      setError("");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  React.useEffect(() => {
    void load();
    const intervalId = window.setInterval(() => {
      void load();
    }, 5000);

    return () => window.clearInterval(intervalId);
  }, [load]);

  const sortedRows = React.useMemo(() => {
    return [...rows].sort(
      (a, b) => Number(b.spread_percent) - Number(a.spread_percent)
    );
  }, [rows]);

  return (
    <main className="page">
      <header className="hero">
        <h1>TradeFlow</h1>
        <p>Multi-source crypto/stock arbitrage tracker</p>
      </header>

      <section className="summary-cards">
        <div className="card">
          <span className="label">Tracked rows</span>
          <strong>{rows.length}</strong>
        </div>
        <div className="card">
          <span className="label">Best spread</span>
          <strong>
            {sortedRows.length > 0 ? `${Number(sortedRows[0].spread_percent).toFixed(4)}%` : "—"}
          </strong>
        </div>
        <div className="card">
          <span className="label">Refresh cadence</span>
          <strong>5 seconds</strong>
        </div>
      </section>

      {loading && <p>Loading data…</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <OpportunitiesTable data={rows} flashingRowIds={flashingRowIds} />
      )}
    </main>
  );
}