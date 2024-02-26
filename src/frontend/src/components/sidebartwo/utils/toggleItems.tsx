class ToggleItems {
  private items: string[];
  private itemStates: { [key: string]: string };
  private activeItem: string;

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
    this.activeItem = active_item;
    this.itemStates[active_item] = "active"
  }

  hoverItem(itemName: string): void {
    if (this.items.includes(itemName)) {
      if (this.itemStates[itemName] == "inactive") {
        this.itemStates[itemName] = "hover";
      } else if (this.itemStates[itemName] == "hover") {
        this.itemStates[itemName] = "inactive";
      }
    } else {
      console.log(`Value for item ${itemName} not in ${this.items}`);
    }
  }

  getCurrentStates(): { [key: string]: string } {
    return this.itemStates;
  }
}

export default ToggleItems;
