class ToggleItems {
  private items: string[];
  private itemStates: { [key: string]: string };

  constructor(itemList: string[], active_item: string) {
    this.items = itemList;
    const stateArray = Array.from({ length: itemList.length }, () => "inactive");
    this.itemStates = itemList.reduce(
      (result: { [key: string]: string }, key, index) => {
        result[key] = stateArray[index];
        return result;
      },
      {}
    );
    this.itemStates[active_item] = "active"
  }

  hoverItem(itemName: string): void {
    if (this.items.includes(itemName)) {
      if (this.itemStates[itemName] == "inactive") {
        this.itemStates[itemName] = "hover";
      } else if (this.itemStates[itemName] == "hover") {
        this.itemStates[itemName] = "inactive";
      }
    }
  }

  getCurrentStates(): { [key: string]: string } {
    return this.itemStates;
  }
}

export default ToggleItems;
