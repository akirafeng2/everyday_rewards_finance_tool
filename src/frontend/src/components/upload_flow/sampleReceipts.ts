export interface ReceiptItem {
  id: string;
  itemName: string;
  cost: string;
}

export interface Receipt {
  id: string;
  date: string;
  items: ReceiptItem[];
}

// Placeholder until the receipt API returns the freshly imported receipts.
export const SAMPLE_RECEIPTS: Receipt[] = Array.from({ length: 10 }, (_, r) => ({
  id: `receipt-${r}`,
  date: "24 January 2024",
  items: Array.from({ length: 6 }, (_, i) => ({
    id: `receipt-${r}-item-${i}`,
    itemName: "Example of an item here",
    cost: "$75.67",
  })),
}));
