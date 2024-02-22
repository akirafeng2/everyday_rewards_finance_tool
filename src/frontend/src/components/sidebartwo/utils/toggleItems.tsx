class ToggleItems {
    private items: string[];
    private itemStates: { [key: string]: string};
    private activeItem: string;

    constructor(itemList: string[]) {
        this.items = itemList
        const stateArray = ["active"].concat(Array.from({ length: itemList.length-1 }, () => "inactive"))
        this.itemStates = itemList.reduce((result: { [key: string]: string}, key, index) => {
            result[key] = stateArray[index];
            return result;
        }, {})
        this.activeItem = itemList[0]
    }

    toggleItem(itemName: string): void {
        if (this.items.includes(itemName)) {
            this.itemStates[this.activeItem] = "inactive"
            this.itemStates[itemName] = "active"
            this.activeItem = itemName
        }
        else {
            console.log(`Value for item ${itemName} not in ${this.items}`)
        }
    }

    hoverItem(itemName: string): void {
        if (this.items.includes(itemName)) {
            if (this.itemStates[itemName] == "inactive") {
                this.itemStates[itemName] = "hover"
            }
            else if (this.itemStates[itemName] == "hover") {
                this.itemStates[itemName] = "inactive"
            }
        }
                else {
            console.log(`Value for item ${itemName} not in ${this.items}`)
        }
    }

    getCurrentStates(): { [key: string]: string} {
        return this.itemStates
    }
}

export default ToggleItems