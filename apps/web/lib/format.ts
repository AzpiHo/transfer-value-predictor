import type { Direction } from "@/lib/types";

export function formatEur(value: number): string {
  const formatted = new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "EUR",
    maximumFractionDigits: 0,
  }).format(Math.abs(value));
  if (value > 0) return `+${formatted}`;
  if (value < 0) return `−${formatted}`;
  return formatted;
}

export function directionLabel(direction: Direction): string {
  if (direction === "up") return "Rise";
  if (direction === "down") return "Fall";
  return "Flat";
}
