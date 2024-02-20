class ToggleItems {
    private items: string[];
    private itemState: { [key: string]: string};
    private activeItem: string;

    constructor(itemList: string[]) {
        this.items = itemList
        const stateArray = ["active"].concat(Array.from({ length: itemList.length-1 }, () => "inactive"))
        this.itemState = itemList.reduce((result: { [key: string]: string}, key, index) => {
            result[key] = stateArray[index];
            return result;
        }, {})
        this.activeItem = itemList[0]
    }

    toggleItem(itemName: string): void {
        if (this.items.includes(itemName)) {
            this.itemState[this.activeItem] = "inactive"
            this.itemState[itemName] = "active"
            this.activeItem = itemName
        }
        else {
            console.log(`Value for item ${itemName} not in ${this.items}`)
        }
    }

    getCurrentStates(): { [key: string]: string} {
        return this.itemState
    }
}