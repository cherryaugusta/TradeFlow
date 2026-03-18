import React from "react";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  getSortedRowModel,
  type SortingState,
  useReactTable,
} from "@tanstack/react-table";
import type { ArbitrageOpportunity } from "../types";

type Props = {
  data: ArbitrageOpportunity[];
  flashingRowIds: Set<number>;
};

const columnHelper = createColumnHelper<ArbitrageOpportunity>();

const columns = [
  columnHelper.accessor("asset_symbol", {
    header: "Asset",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("cheapest_exchange_name", {
    header: "Buy @",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("most_expensive_exchange_name", {
    header: "Sell @",
    cell: (info) => info.getValue(),
  }),
  columnHelper.accessor("cheapest_price", {
    header: "Cheapest",
    cell: (info) => Number(info.getValue()).toFixed(4),
  }),
  columnHelper.accessor("highest_price", {
    header: "Highest",
    cell: (info) => Number(info.getValue()).toFixed(4),
  }),
  columnHelper.accessor("spread_absolute", {
    header: "Spread Abs",
    cell: (info) => Number(info.getValue()).toFixed(4),
  }),
  columnHelper.accessor("spread_percent", {
    header: "Spread %",
    cell: (info) => `${Number(info.getValue()).toFixed(4)}%`,
  }),
  columnHelper.accessor("observed_at", {
    header: "Observed",
    cell: (info) => new Date(info.getValue()).toLocaleTimeString(),
  }),
];

export default function OpportunitiesTable({ data, flashingRowIds }: Props): React.JSX.Element {
  const [sorting, setSorting] = React.useState<SortingState>([
    { id: "spread_percent", desc: true },
  ]);

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="table-wrap">
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  style={{ cursor: "pointer" }}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                  {{
                    asc: " ▲",
                    desc: " ▼",
                  }[header.column.getIsSorted() as string] ?? null}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => {
            const rowId = row.original.id;
            const isFlashing = flashingRowIds.has(rowId);

            return (
              <tr key={row.id} className={isFlashing ? "flash-row" : ""}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}