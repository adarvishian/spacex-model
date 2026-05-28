import { YearSeries } from "../api";

type Row = {
  label: string;
  series: YearSeries;
  lineageKey: string;
};

type Props = {
  rows: Row[];
  onCellClick: (lineageKey: string) => void;
  formatValue: (v: number) => string;
  yearSlice?: number[];
};

export function FcfTable({ rows, onCellClick, formatValue, yearSlice }: Props) {
  if (rows.length === 0) return null;
  const years = yearSlice ?? rows[0].series.years.filter((y) => y % 5 === 0 || y === 2025);

  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            <th>Row</th>
            {years.map((y) => (
              <th key={y}>{y}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr
              key={row.label}
              className="clickable"
              onClick={() => onCellClick(row.lineageKey)}
            >
              <td>{row.label}</td>
              {years.map((y) => {
                const idx = row.series.years.indexOf(y);
                const val = idx >= 0 ? row.series.values[idx] : 0;
                return (
                  <td key={y} className="num">
                    {formatValue(val)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
