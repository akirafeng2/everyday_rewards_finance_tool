export interface EntryRow {
  id: string;
  itemName: string;
  cost: string;
  payer: string;
  repeats: string;
  weights: string[];
}

export const emptyEntryRow = (members: string[], defaults: Partial<EntryRow> = {}): EntryRow => ({
  id: `${Date.now()}-${Math.random()}`,
  itemName: "",
  cost: "",
  payer: members[0] ?? "",
  repeats: "Monthly",
  weights: members.map(() => ""),
  ...defaults,
});
